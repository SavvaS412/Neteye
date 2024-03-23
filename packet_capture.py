import scapy.all as scapy
from time import sleep
from datetime import datetime

from detection import detect_dos_attacks, detect_scanning, NetworkScan, PortScanUDP, PortScanXMAS, PortScanNULL
from network_utils import get_interface_name, get_ip
from file_utils import save_capture, get_setting, PACKET_CAPTURE_WINDOW

def print_packet(packet):
    print(packet.summary())

def get_statistics(capture, ip):
    data_received = 0
    data_sent = 0
    for packet in capture:
        if packet.haslayer(scapy.IP):
            if packet[scapy.IP].dst == ip:
                data_received += len(packet)
            else:
                data_sent += len(packet)

    return data_sent + data_received, data_received, data_sent

def check_dos_attack(packet, dos_packets_by_ip, dos_packet_count, dos_target_ip):
    if scapy.IP in packet and packet[scapy.IP].dst in dos_target_ip:
        if packet[scapy.IP].src not in dos_packets_by_ip.keys():
            dos_packets_by_ip[packet[scapy.IP].src] = 0
        dos_packets_by_ip[packet[scapy.IP].src] += 1
        dos_packet_count += 1
    return dos_packets_by_ip, dos_packet_count

def check_network_scanning(packet, network_scanning_packets_by_ip):
    if scapy.ICMP in packet and packet[scapy.ICMP].type == 8:
        if scapy.IP in packet and packet[scapy.IP].src != get_ip() and packet[scapy.IP].dst != get_ip(): 
            if packet[scapy.IP].src not in network_scanning_packets_by_ip.keys():
                network_scanning_packets_by_ip[packet[scapy.IP].src] = [packet[scapy.IP].dst]
            else:
                if packet[scapy.IP].dst not in network_scanning_packets_by_ip[packet[scapy.IP].src]:
                    network_scanning_packets_by_ip[packet[scapy.IP].src].append([packet[scapy.IP].dst])
    return network_scanning_packets_by_ip

def check_port_scanning_udp(packet, port_scanning_udp_by_ip):
    if scapy.UDP in packet and packet[scapy.UDP].len == 8 and scapy.IP in packet:
        if packet[scapy.IP].src not in port_scanning_udp_by_ip.keys():
            port_scanning_udp_by_ip[packet[scapy.IP].src] = [packet[scapy.UDP].dport]
        else:
            if packet[scapy.UDP].dport not in port_scanning_udp_by_ip[packet[scapy.IP].src]:
                port_scanning_udp_by_ip[packet[scapy.IP].src].append(packet[scapy.UDP].dport)
    return port_scanning_udp_by_ip

def check_port_scanning_xmas(packet, port_scanning_xmas_by_ip):
    if packet[scapy.TCP].flags == 0x29:
        if packet[scapy.IP].src not in port_scanning_xmas_by_ip.keys():
            port_scanning_xmas_by_ip[packet[scapy.IP].src] = [packet[scapy.TCP].dport]
        else:
            if packet[scapy.TCP].dport not in port_scanning_xmas_by_ip[packet[scapy.IP].src]:
                port_scanning_xmas_by_ip[packet[scapy.IP].src].append(packet[scapy.TCP].dport)
    return port_scanning_xmas_by_ip

def check_port_scanning_null(packet, port_scanning_null_by_ip):
    if packet[scapy.TCP].flags == 0x0:
        if packet[scapy.IP].src not in port_scanning_null_by_ip.keys():
            port_scanning_null_by_ip[packet[scapy.IP].src] = [packet[scapy.TCP].dport]
        else:
            if packet[scapy.TCP].dport not in port_scanning_null_by_ip[packet[scapy.IP].src]:
                port_scanning_null_by_ip[packet[scapy.IP].src].append(packet[scapy.TCP].dport)
    return port_scanning_null_by_ip

def capture(window_size=get_setting(PACKET_CAPTURE_WINDOW)):       
    global interface_name 
    interface_name = get_interface_name()        
    dos_avg_packets_per_second = 0
    first_iteration = True
    dos_target_ip = [get_ip()]
    while True:
        dos_packet_count = 0                # packets that ip.dst == me
        dos_packets_by_ip = dict()
        network_scanning_packets_by_ip = dict()
        port_scanning_udp_by_ip = dict()
        port_scanning_xmas_by_ip = dict()
        port_scanning_null_by_ip = dict()

        def packet_callback(packet):
            nonlocal dos_packet_count, dos_packets_by_ip, network_scanning_packets_by_ip, port_scanning_udp_by_ip, port_scanning_xmas_by_ip, port_scanning_null_by_ip

            dos_packets_by_ip, dos_packet_count = check_dos_attack(packet, dos_packets_by_ip, dos_packet_count, dos_target_ip)
            
            network_scanning_packets_by_ip = check_network_scanning(packet, network_scanning_packets_by_ip)

            port_scanning_udp_by_ip = check_port_scanning_udp(packet, port_scanning_udp_by_ip)

            if scapy.TCP in packet:
                port_scanning_xmas_by_ip = check_port_scanning_xmas(packet, port_scanning_xmas_by_ip)
                port_scanning_null_by_ip = check_port_scanning_null(packet, port_scanning_null_by_ip)

        capture = scapy.sniff(iface=interface_name, prn=packet_callback, timeout=window_size)
        print()
        print(capture)
        print()

        save_capture(capture)

        data_total, data_received, data_sent = get_statistics(capture, get_ip())
        print("Data Total:" + str(int(data_total/1000)) + "kb")
        print("Data Recieved:" + str(int(data_received/1000)) + "kb")
        print("Data Sent:" + str(int(data_sent/1000)) + "kb")
        print()

        dos_packets_per_second = dos_packet_count / window_size

        if first_iteration:
            dos_avg_packets_per_second = dos_packets_per_second

        else:
            detect_dos_attacks(dos_packets_per_second, dos_avg_packets_per_second, dos_packets_by_ip, window_size)
            detect_scanning(network_scanning_packets_by_ip, NetworkScan())
            detect_scanning(port_scanning_udp_by_ip, PortScanUDP())
            detect_scanning(port_scanning_xmas_by_ip, PortScanXMAS())
            detect_scanning(port_scanning_null_by_ip, PortScanNULL())

        first_iteration = False

        dos_avg_packets_per_second = (dos_packets_per_second + dos_avg_packets_per_second) / 2

        sleep(window_size)

def main():
    capture()

if __name__ == '__main__':
    main()
