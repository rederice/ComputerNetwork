import socket
import sys
import random
ACK = "RECVGET"
FSH = "FLUSH"
FIN = "fin"
FINACK = "finack"

class UdpAgent(object):
	def __init__(self, s_ip, s_port, drop):
		self.get_cnt = 0
		self.drop_cnt = 0
		self.threshold = float(drop)
		self.flag = 0
		self.server = (s_ip, int(s_port))
	def tcpagent(self, a_ip, a_port):
		recvSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		recvSock.bind((a_ip, int(a_port)))
		recvSock.setblocking(0)
		# recvSock.settimeout(1)

		sendSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sendSock.setblocking(0)
		# sendSock.settimeout(1)
		while True:
			# get client request
			try:
				if self.flag == 0:
					recvData, (remoteHost, remotePort) = recvSock.recvfrom(1024)
					tmp = recvData.split(b'@',1)
					num = tmp[0].decode('utf-8')
					header = tmp[1]
					if num == "-1" and header.decode('utf-8') == FIN:
						print("get\tfin")
					else:
						print("get\tdata\t#",num)
					self.get_cnt += 1

					R = random.random()
					if R > self.threshold or (num == "-1" and header.decode('utf-8') == FIN):
						sendDataLen = sendSock.sendto(recvData, self.server)
						self.flag = 1
						if num == "-1" and header.decode('utf-8') == FIN:
							print("fwd\tfin")
						else:
							print("fwd\tdata\t# {},\tloss rate = {:.4f}".format(num, self.drop_cnt/self.get_cnt))
					elif R <= self.threshold:
						self.drop_cnt += 1
						print("drop\tdata\t#",num)
					# print("[%s:%s] get connect" % (remoteHost, remotePort))

				elif self.flag == 1:
					recvData1, (remoteHost1, remotePort1) = sendSock.recvfrom(1024)
					tmp = recvData1.split(b'@',1)
					num = tmp[0].decode('utf-8')
					header = tmp[1]
					if num == "-1" and header.decode('utf-8') == FINACK:
						print("get\tfinack")
					elif header == FSH:
						self.flag = 0
						continue
					else:
						print("get\tack\t#",num)
					sendDataLen = recvSock.sendto(recvData1, (remoteHost, remotePort))
					self.flag = 0
					if num == "-1" and header.decode('utf-8') == FINACK:
						print("fwd\tfinack")
					else:
						print("fwd\tack\t#",num)
					# print("[%s:%s] send connect" % (remoteHost1, remotePort1))
			except Exception as e:
				pass
		recvSock.close()
		sendSock.close()

if __name__ == "__main__":
	udpagent = UdpAgent(sys.argv[3],sys.argv[4],sys.argv[5])
	udpagent.tcpagent(sys.argv[1],sys.argv[2])