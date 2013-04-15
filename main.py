import cshldap

import asyncore, socket, time
import threading

HOST = 'drinkjs.csh.rit.edu'
PORT = 4242

class drinkshell():
	def __init__(self):
		ldap = cshldap.CSHLDAP('ldap://ldap.csh.rit.edu')
		usernameldap = ldap.conn.whoami_s()
		index = usernameldap.find(',')
		username = usernameldap[len('dn:uid='): index]
		results = ldap.search('dc=csh,dc=rit,dc=edu', "uid=" + username)
		ibuttonlist = results[0][1]["ibutton"]
		self.ibutton = 0
		if (len(ibuttonlist) > 1):
			print ("You have this many ibuttons " + str(len(ibuttonlist)))
			for i,ibuttons in enumerate(ibuttonlist):
				print (str(i) + " " + ibuttons)
			choice = input("Which do you want to use?")
			self.ibutton = ibuttonlist[choice]
			print("You chose " + self.ibutton)
		else:
			self.ibutton = ibuttonlist[0]
			print("Your ibutton is " + self. ibutton)

class drinksocket(asyncore.dispatcher):
	def __init__(self):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect((HOST, PORT))
		self.ds = drinkshell()
		#self.send('ibutton ' + self.ds.ibutton + '\n')
		self.buffer = 'ibutton ' + self.ds.ibutton + '\n'
		self.handle_write()
	
	def handle_connect(self):
		pass

	def handle_clonse(self):
		self.close()

	def handle_read(self):
		buffer = self.recv(8192)
		print(buffer)
		def writable(self):
			return (len(self.buffer) > 0)
	
	def handle_write(self):
		sent = self.send(self.buffer)
		self.buffer = self.buffer[sent:]



drinksock = drinksocket()
asyncore.loop(120)
