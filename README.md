# NetEye NMS

# Web GUI
**Before working on parts that include the use of Flask, activate the corresponding enviroment:**
On Windows:
```
> .venv\Scripts\activate
```
On macOS/Linux:
```
$ . .venv/bin/activate
```

## Installation
On Windows:
```
> mkdir myproject
> cd myproject
> py -3 -m venv .venv
```
On macOS/Linux:
```
$ mkdir myproject
$ cd myproject
$ python3 -m venv .venv
```

# Detection
## DoS:
**DoS (Denial Of Service) has 2 parameters.**
* Threshold - the value that's multiplied by the dynamic threshold that the program calculates to determine whether a DoS attack is happening or not. Unstable networks require a higher Threshold value to avoid false-positives. The more stable the network is, a lower threshold will result in a better acurracy.
  *Usually between 0.5 and 1, should be lower than DDoS Threshold.*
* Target - the target IPs that the algorithm checks if a DoS attack was made **to** them. 

