import socket
import sys
ACK = "@RECVGET"
FSH = "@FLUSH"

class UdpServer(object):
    def __init__(self):
        self.buffer_size = 32
        self.buffer_ = []

    def flush(self):
        for i in range(len(self.buffer_)):
            self.file.write(self.buffer_[i])
            self.file.flush()
        self.buffer_ = []

    def tcpServer(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((ip, int(port)))
        # sock.settimeout(1e-9)
        sock.setblocking(0)
        cnt = 0

        print("---Server ready to Receive---")
        while True:
            try:
                recvData, (remoteHost, remotePort) = sock.recvfrom(1024)
                # print("[%s:%s] connect" % (remoteHost, remotePort))
                
                tmp = recvData.split(b'@',1)
                num = tmp[0].decode()
                ll = tmp[1]

                if int(num) == 0:
                    self.file = open("result"+ll.decode(),"wb")

                if int(num) == -1 and ll.decode() == "fin":
                    print("recv\tfin")
                    sendDataLen = sock.sendto("-1@finack".encode(), (remoteHost, remotePort))
                    print("send\tfinack")
                    self.flush()
                    print("flush")
                    break

                print("recv\tdata\t#",num)

                if int(num) == cnt+1:
                    if len(self.buffer_) == self.buffer_size:
                        sendDataLen = sock.sendto((str(cnt)+FSH).encode(), (remoteHost, remotePort))
                        self.flush()
                        print("drop\tdata\t#",num)
                        print("flush")
                        continue
                    self.buffer_.append(ll)
                    cnt += 1

                sendDataLen = sock.sendto((str(cnt)+ACK).encode(), (remoteHost, remotePort))
                print("send\tack\t#",cnt)
            
            except Exception as e:
                pass
        sock.close()
        self.file.close()
        print("---End of Connection---")

if __name__ == "__main__":
    udpServer = UdpServer()
    udpServer.tcpServer(sys.argv[1],sys.argv[2])