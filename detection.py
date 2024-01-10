from scanning import Rule
from enum import Enum

MINIMAL_PPS_RANGE = 10
LOW_PPS_RANGE = 25
MEDIUM_LOW_PPS_RANGE = 50
MEDIUM_HIGH_PPS_RANGE = 100
HIGH_PPS_RANGE = 500
ULTRA_PPS_RANGE = 1000
MAXIMUM_PPS_RANGE = 5000

class Action(Enum):
    LESS_EQUAL = -2
    LESS = -1
    EQUAL = 0
    GREATER = 1
    GREATER_EQUAL = 2

class Parameter(Enum):
    DATA_TOTAL = 1
    DATA_RECIEVED = 2
    DATA_SENT = 3
    DATA_PER_SECOND_TOTAL = 4
    DATA_PER_SECOND_RECIEVED = 5
    DATA_PER_SECOND_SENT = 6
    PACKET_LOSS = 7
    LATENCY = 8
    #...
    
def calculate_dynamic_threshold(avg_packets_per_second : float) -> float:
    if avg_packets_per_second <= MINIMAL_PPS_RANGE:
        threshold_factor = 100
    elif avg_packets_per_second <= LOW_PPS_RANGE:
        threshold_factor = 90
    elif avg_packets_per_second <= MEDIUM_LOW_PPS_RANGE:
        threshold_factor = 75
    elif avg_packets_per_second <= MEDIUM_HIGH_PPS_RANGE:
        threshold_factor = 55
    elif avg_packets_per_second <= HIGH_PPS_RANGE:
        threshold_factor = 35
    elif avg_packets_per_second <= ULTRA_PPS_RANGE:
        threshold_factor = 10
    elif avg_packets_per_second <= MAXIMUM_PPS_RANGE:
        threshold_factor = 5
    else:
        threshold_factor = 3

    dynamic_threshold = threshold_factor * avg_packets_per_second
    return dynamic_threshold

def detect_ddos(packets_per_second : float, avg_packets_per_second : float):
    dynamic_threshold = calculate_dynamic_threshold(avg_packets_per_second)

    print(f"Packets per second: {packets_per_second:.2f}")
    print(f"Dynamic Threshold: {dynamic_threshold:.2f}")

    if packets_per_second > dynamic_threshold:
        print("Possible DDoS attack detected!")
        #notify_ddos()

def check_statement(parameter : int, action : Action, amount : int) -> bool:
    match action:
        case Action.LESS_EQUAL:
            statement = parameter <= amount

        case Action.LESS:
            statement = parameter < amount

        case Action.EQUAL:
            statement = parameter == amount

        case Action.GREATER:
            statement = parameter > amount
        
        case Action.GREATER_EQUAL:
            statement = parameter >= amount

        case _:
            statement = False

    return statement 

def detect_rules(rules : list[Rule]):
    for rule in rules:
        try:
            statement = check_statement(rule.parameter, Action(rule.action), rule.amount)
        except ValueError as e:
            print(f"ERR: unknown rule action in rule '{rule.name}' -", e)
            statement = False

        if statement:
            print("Notification:", rule.name)

        else:
            print("No Notification:", rule.name)

if __name__ == '__main__':
    detect_rules([Rule("test greater", 1, 150, 100), Rule("test wrong", 1, 15, 100), Rule("test equal", 0, 15, 15), Rule("test less", -1, 15, 100), Rule("test less wrong", -1, 15, 15), Rule("test less equal", -2, 15, 15), Rule("test error", 3, 15, 100)])