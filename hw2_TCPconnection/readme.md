# TCP connection

language : Python

## details

1. Using UDP socket to implement TCP
### Reliable Transmission
```
Data & Ack
Timeout & Retransmission (Go-Back-N)
Sequence Number
```
### Congestion Control
```
Slow Start
Packet Loss / Timeout
Buffer Handling
```
2. Execute in the following order:
### Agent:
```
python agent.py $AGENT_IP $AGENT_PORT $RECV_IP $RECV_PORT $DROP_RATE
```
### Receiver:
```
python receiver.py $RECV_IP $RECV_PORT
```
### Sender:
```
python sender.py $SEND_FILE_PATH $AGENT_IP $AGENT_PORT
```
3. File will be sent from sender.py path to
```
result.xxx
```
in the same directory of receiver.py
