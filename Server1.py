# task to implimplement
# 1.Join
# 2.chat
# 3.message
# 4.leave
# 5.Disconnect


import socket
from threading import Thread
from threading import Lock
import random
import sys,os

#to enable thread lock for one client at a time
threadLock = Lock()

def join(conn_msg,conn):
    #to lock the thread for the joined client
    threadLock.acquire()
    #Searching and identifying the acknowledgement received from the client for the JOIN CHATROOM and end of line 
    gname = conn_msg.find('JOIN_CHATROOM:'.encode('utf-8'))+14
    gname_end = conn_msg.find('\n'.encode('utf-8'))
    groupname = conn_msg[gname:gname_end]
    #Searching and identifying the client name in the acknowledgement received from the client
    cname = conn_msg.find('CLIENT_NAME'.encode('utf-8'))+13
    cname_end = conn_msg.find(' '.encode('utf-8'),cname)
    clientname = conn_msg[cname:cname_end]
    rID = 0
    print(groupname)
    #assigning room IDs to the connected clients
    if (groupname.decode('utf-8')) == 'room1' :
        g1_clients.append(clThread.socket)
        rID = 1001
    elif groupname == 'room2' :
       g2_clients.append(clThread.socket)
       rID = 1002
	#sending ackowledgement
    response = "JOINED_CHATROOM: ".encode('utf-8') + groupname+ "\n".encode('utf-8')
    response += "SERVER_IP: ".encode('utf-8') + host.encode('utf-8') + "\n".encode('utf-8')
    response += "PORT:".encode('utf-8') + str(port).encode('utf-8') + "\n".encode('utf-8')
    response += "ROOM_REF: ".encode('utf-8') + str(rID).encode('utf-8') +'\n'.encode('utf-8')
    response += "JOIN_ID: ".encode('utf-8') + str(clThread.uid).encode('utf-8') + "\n".encode('utf-8')
    conn.send(response)
    grpmessage = "CHAT:".encode('utf-8') + str(rID).encode('utf-8') + "\n".encode('utf-8')
    grpmessage += "CLIENT_NAME:".encode('utf-8') + clientname + "\n".encode('utf-8') 
    grpmessage += "MESSAGE:".encode('utf-8') + clientname + "\n".encode('utf-8') 
    grpmessage += "CLIENT_ID:".encode('utf-8') + str(clThread.uid).encode('utf-8') +"\n".encode('utf-8')
    grpmessage += "JOINED_GROUP".encode('utf-8') +"\n".encode('utf-8')
    if (groupname.decode('utf-8')) == 'room1':
        for x in range(len(g1_clients)):
            g1_clients[x].send(grpmessage)
    elif (groupname.decode('utf-8')) == 'room2':
        for x in range(len(g2_clients)):
            g2_clients[x].send(grpmessage)
    threadLock.release()
    return groupname,clientname,rID

def chat(conn_msg,conn):
    threadLock.acquire()
    chat_msg_start = conn_msg.find('MESSAGE:'.encode('utf-8')) + 9
    chat_msg_end = conn_msg.find('\n\n'.encode('utf-8'),chat_msg_start)
    chat_msg = conn_msg[chat_msg_start:chat_msg_end]
    
    grp_start = conn_msg.find('CHAT:'.encode('utf-8')) + 6 
    grp_end = conn_msg.find('\n'.encode('utf-8'), grp_start)
    
    group_name = conn_msg[grp_start:grp_end]
    client_msg = "CHAT: ".encode('utf-8') + str(clThread.roomID).encode('utf-8') + "\n".encode('utf-8')
    client_msg += "CLIENT_NAME: ".encode('utf-8') +str(clThread.clientname).encode('utf-8') + "\n".encode('utf-8')
    client_msg += "MESSAGE: ".encode('utf-8') + str(chat_msg).encode('utf-8')
    if (group_name.decode('utf-8')) == 'room1':
        for x in range(len(g1_clients)):
            g1_clients[x].send(client_msg)
    elif group_name == 'room2':
        for x in g2_clients:
            g2_clients[x].send(client_msg)
    threadLock.release()

def check_msg(msg):
    if (msg.find('JOIN_CHATROOM'.encode('utf-8'))+1):
        return(1)	
    elif (msg.find('LEAVE_CHATROOM'.encode('utf-8'))+1):
        return(2)
    elif (msg.find('DISCONNECT'.encode('utf-8'))+1):
        return(3)
    elif (msg.find('CHAT:'.encode('utf-8'))+1):
        return(4)
    elif (msg.find('KILL_SERVICE'.encode('utf-8'))+1):
        os._exit(1)
    elif (msg.find('HELO'.encode('utf-8'))+1):
        return(5)
    else:
        return(6)

def resp(msg,socket):
    msg_start = msg.find('HELO:'.encode('utf-8')) + 5
    msg_end = msg.find('\n'.encode('utf-8'),msg_start)
    
    chat_msg = msg[msg_start:msg_end]
    
    response = "HELO: ".encode('utf-8') + chat_msg + "\n".encode('utf-8')
    response += "IP: ".encode('utf-8') + str(clThread.ip).encode('utf-8') + "\n".encode('utf-8')
    response += "PORT: ".encode('utf-8') + str(clThread.port).encode('utf-8') + "\n".encode('utf-8')
    response += "StudentID: ".encode('utf-8') + "17311910".encode('utf-8') + "\n".encode('utf-8')
    
    socket.send(response)
    
    
def leave(conn_msg,conn):
    threadLock.acquire()
    grp_start = conn_msg.find('LEAVE_CHATROOM:'.encode('utf-8')) + 16
    grp_end = conn_msg.find('\n'.encode('utf-8'), grp_start) 
    
    group_name = conn_msg[grp_start:grp_end]
    
    response = "LEFT_CHATROOM".encode('utf-8') + group_name + "\n".encode('utf-8')
    response += "JOIN_ID".encode('utf-8') + str(clThread.uid).encode('utf-8')
    
    grpmessage = "CLIENT_NAME:".encode('utf-8') + str(clThread.clientname).encode('utf-8') + "\n".encode('utf-8')
    grpmessage += "CLIENT_ID:".encode('utf-8') + str(clThread.uid).encode('utf-8') +"\n".encode('utf-8')
    grpmessage += "LEFT GROUP".encode('utf-8')
    print(group_name)
    if (group_name.decode('utf-8')) == 'room1':
        i = g1_clients.index(clThread.socket)
        del g1_clients[i]
        for x in g1_clients:
            g1_clients[x].send(client_msg)
    elif (group_name.decode('utf-8')) == 'room2':
        i = g2_clients.index(clThread.socket)
        del g2_clients[i]
        for x in g2_clients:
            g2_clients[x].send(client_msg)
    conn.send(response)
    threadLock.release()

#creating threads for clients   
class client_threads(Thread):
#initilizing the client thread.
	def __init__(self,ip,port,socket):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.chatroom =[] 
		self.socket = socket
		self.uid = random.randint(1000,2000)
		self.roomname = ''
		self.clientname = ''
		self.roomID = ''
	def run(self):
		while True:
			conn_msg = conn.recv(1024)
			print(conn_msg)
			cflag = check_msg(conn_msg)
			if cflag == 1 : self.roomname,self.clientname,self.roomID = join(conn_msg,conn)
			elif cflag == 2 : leave(conn_msg,conn)
			elif cflag == 3 : return(0)
			elif cflag == 4 : chat(conn_msg,conn)
			elif cflag == 5 : resp(conn_msg,conn)
			else : print('Error code. Wait for more')
			self.chatroom.append(self.roomname)
			print('Total clients in group g1: ')
			print(len(g1_clients))
			print('Total clients in group g2: ')
			print(len(g2_clients))


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
port = 5555
#Bind socket to local host and port
try:
    server.bind((host, port))
except socket.error as msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()     

thread_count = [] 
g1_clients = []
g2_clients = []
print('Server started')
print("Host name: ",host)
print("Port number: ", port)

#Start listening on socket
while True:
    server.listen(5)
    (conn,(ip,port)) = server.accept()
    print("Connected to ",ip)
    clThread = client_threads(ip,port,conn)
    clThread.start()
    thread_count.append(clThread)
    
    
    