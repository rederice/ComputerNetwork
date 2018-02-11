import socket
# import ConfigParser
# configParser = ConfigParser.RawConfigParser()   
# configFilePath = r'config'
# configParser.read(configFilePath)

def recur(stri,index,array,ans):
	if stri[index:].isdigit() == False:
		return
	if len(array) == 3:
		if len(stri)-index >=2 and stri[index]=='0':
			return
		if int(stri[index:]) < 256:
			sss = (array[0]+'.'+array[1]+'.'+array[2]+'.'+stri[index:])
			ans.append(sss)
	else:
		for i in range(index,len(stri)-1):
			if(int(stri[index:i+1])) < 256:
				if i-index == 0 or stri[index]!='0':
					array.append(stri[index:i+1])
					recur(stri,i+1,array,ans)
					array.pop()
	return

host="irc.freenode.net"
port=6667
# channel = configParser.get('config', 'CHAN')
f = open('./config', 'r')
channel = f.read().split('=')[1].strip('\r\n').strip('\'')
IRCsocket = socket.socket()
IRCsocket.connect((host,port))
msg = "USER RBT "+host+" "+"rbt :"+"ABC\n"
IRCsocket.send(bytes(msg))
msg = "NICK ROBOT_21\n"
IRCsocket.send(bytes(msg))
msg = "JOIN "+channel+"\n"
IRCsocket.send(bytes(msg))
msg = "PRIVMSG "+channel+" :"+"Hello! I am robot.\n"
IRCsocket.send(bytes(msg))

while(True):
	MSG = IRCsocket.recv(4096)
	content = MSG.decode("utf-8")
	content = content.split(':')
	s = content[len(content)-1]
	word = content[len(content)-1].split(' ')
	sss = ""
	if word[0] == "@repeat":
		sss = s[8:len(s)]
	elif word[0] == "@convert":
		if (word[1].strip()).isdigit():
			sss = hex(int(word[1]))
		elif word[1][0:2] == "0x":
			sss = str(int(word[1], 16))
		else:
			continue
	elif word[0] == "@ip":
		sss = word[1].strip()
		if sss.isdigit() == False:
			continue
		array = []
		ans = []
		if len(word[1]) > 12 or len(word[1]) < 4:
			msg = "PRIVMSG "+channel+" :0\n"
			IRCsocket.send(bytes(msg))
			continue
		recur(sss, 0, array, ans)
		msg = "PRIVMSG "+channel+" :"+str(len(ans))+"\n"
		IRCsocket.send(bytes(msg))
		for i in range(len(ans)):
			msg = "PRIVMSG "+channel+" :"+ans[i]+"\n"
			IRCsocket.send(bytes(msg))
		continue
	elif word[0].strip() == "@help":
		msg = "PRIVMSG "+channel+" :@repeat <Message>\n"
		IRCsocket.send(bytes(msg))
		msg = "PRIVMSG "+channel+" :@convert <Number>\n"
		IRCsocket.send(bytes(msg))
		msg = "PRIVMSG "+channel+" :@ip <String>\n"
		IRCsocket.send(bytes(msg))
		continue
	msg = "PRIVMSG "+channel+" :"+sss+"\n"
	IRCsocket.send(bytes(msg))
