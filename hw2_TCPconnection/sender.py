import socket
import sys
import time
import os
import pdb
ACK = "RECVGET"

class UdpClient(object):
	def __init__(self, ff, ip, port):
		self.cnt = 0
		self.window = 1
		self.threshold = 16
		self.f_index = 0
		self.send_max = 0
		self.file = []
		self.agent = (ip, int(port))
		subtitle = os.path.splitext(ff)[-1]
		tmp = bytes(str(self.f_index)+"@"+subtitle, encoding='utf-8')
		self.file.append(tmp)
		self.f_index += 1
		f = open(ff,"rb")
		tmp = f.read(1000)
		while(tmp):
			self.file.append(bytes(str(self.f_index)+"@", encoding='utf-8') + tmp)
			tmp = f.read(1000)
			self.f_index += 1
	def tcpclient(self):
		clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		clientSock.setblocking(0)
		# clientSock.settimeout(1e-5)
		previous_time = time.time()
		send_cnt = self.cnt
		for i in range(self.window):
			if send_cnt < self.f_index:
				sendDataLen = clientSock.sendto(self.file[send_cnt], self.agent)
				# print("->i=",i," send_cnt=",send_cnt," send_max=",self.send_max)
				if self.send_max == send_cnt:
					if i == self.window-1:
						print("send\tdata\t#",send_cnt,",\twinSize = ",self.window)
					else:
						print("send\tdata\t#",send_cnt)
					send_cnt += 1
					self.send_max += 1
				elif self.send_max > send_cnt:
					if i == self.window-1:
						print("resnd\tdata\t#",send_cnt,",\twinSize = ",self.window)
					else:
						print("resnd\tdata\t#",send_cnt)
					send_cnt += 1

		time.sleep(0.3)
		# while time.time()-previous_time < 0.95:
		for i in range(self.window):
			try:
				recvData, (remoteHost, remotePort) = clientSock.recvfrom(1024)
			except socket.error as e:
				_threshold = self.window//2
				if _threshold > 1:	self.threshold = _threshold
				else: self.threshold = 1
				self.window = 1
				print("time\tout,\t\tthreshold = ",self.threshold)
				break
			recvData = recvData.decode()
			ack = recvData.split('@',1)

			print("recv\tack\t#",ack[0])
			if int(ack[0]) == self.cnt and ack[1] == ACK:
				self.cnt += 1
				# print("-->i=",i," cnt=",self.cnt," send_cnt=",send_cnt)
				if i == self.window-1 and send_cnt == self.cnt:
					if self.window < self.threshold:
						self.window *= 2
					elif self.window >= self.threshold:
						self.window += 1
			else:
				if i == self.window-1:
					_threshold = self.window//2
					if _threshold > 1:	self.threshold = _threshold
					else: self.threshold = 1
					self.window = 1

		clientSock.close()

	def tcpfinal(self):
		clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# clientSock.setblocking(0)
		clientSock.settimeout(1e-3)
		if self.cnt == self.f_index:
			sendDataLen = clientSock.sendto("-1@fin".encode(), self.agent)
			print("send\tfin")
			while True:
				try:
					recvData, (remoteHost, remotePort) = clientSock.recvfrom(1024)
					recvData = recvData.decode()
					ack = recvData.split('@',1)
					if int(ack[0]) == -1 and ack[1] == "finack":
						self.cnt += 1
						print("recv\tfinack")
						return
				except Exception as e:
					pass
			

if __name__ == "__main__":
	udpClient = UdpClient(sys.argv[1],sys.argv[2],sys.argv[3])
	while udpClient.cnt < udpClient.f_index:
		udpClient.tcpclient()
	udpClient.tcpfinal()