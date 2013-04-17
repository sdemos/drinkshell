import cshldap
import sys
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
        commands = {
                    "help"        : self.help_com,
                    "ibutton"     : self.ibutton_com,
                    "machine"     : self.machine_com,
                    "drop"        : self.drop_com,
                    "rand"        : self.stat_com,
                    "temp"        : self.temp_com,
                    "getbalance"  : self.getbalance_com,
                    "addcredits"  : self.addcreds_com,
                    "sendcredits" : self.sendcreds_com
                   }
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
        self.commands = {
                         "help"        : self.help_com,
                         "ibutton"     : self.ibutton_com,
                         "machine"     : self.machine_com,
                         "drop"        : self.drop_com,
                         "rand"        : self.stat_com,
                         "temp"        : self.temp_com,
                         "getbalance"  : self.getbalance_com,
                         "addcredits"  : self.addcreds_com,
                         "sendcredits" : self.sendcreds_com,
                         "quit"        : self.quit_com
                        }
        self.machines = {
                         "d" : "d",
                         "l" : "ld",
                         "s" : "s"
                        }
        #self.send('ibutton ' + self.ds.ibutton + '\n')
        self.buffer = 'ibutton ' + self.ds.ibutton + '\n'
        self.handle_write()
        self.mainloop()

    def mainloop(self):
        while True:
            command = raw_input('drink # ')
            comsplit = command.split()
            #print comsplit
            #print self.commands
            if comsplit[0] not in self.commands:
                print(comsplit[0], 'not a valid command. use help list valid commands')
                continue
            paynus = self.commands[comsplit[0]](comsplit[1:])
            if paynus == None: continue
            print(paynus)
            #self.buffer = self.ds.commands[comsplit[0]](comsplit[1:])
            #self.handle_write()

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        buffer = self.recv(8192)
        print(buffer)
        def writable(self):
            return (len(self.buffer) > 0)
    
    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

    def help_com(self, args):
        print("help:")
        print("help\n     prints commands for drinkshell")
        print("drop <slot index> [delay]\n     drops a drink")
        print("temp\n     prints the temperature for the drink machines")
        print("machine <alias>\n     sets the machine that is being referenced.\n     possible machines: d[rink] | (l[ittledrink] | ld[rink]) | s[nack]")
        print("quit\n     closes drinkshell")
        print("getbalance [user]\n     returns your current drink credit balance")
        print("stat [slot index]\n     prints the current status of the drink machines")
        print("rand [delay]\n     might drop a random drink. I don't actually know if this is implemented")
        print("addcredits and sendcredits(maybe?) should only print if you are an admin")

    def machine_com(self, args):
        if (not len(args) == 1) or args[0][0] not in self.machines:
            print("USAGE: machine <alias>\n     possible machines: d[rink] | (l[ittledrink] | ld[rink]) | s[nack]")
            return
        return "machine " + self.machines[args[0][0]] + "\n"

    def drop_com(self, args):
        if not(len(args) == 1 or len(args) == 2):
            print("USAGE: drop <slot index> [delay]")
            return
        pass

    def stat_com(self, args):
        pass

    def temp_com(self, args):
        pass

    def getbalance_com(self, args):
        pass

    def addcreds_com(self, args):
        pass

    def sendcreds_com(self, args):
        pass

    def quit_com(self, args):
        self.handle_close()
        sys.exit()

drinksock = drinksocket()
asyncore.loop(120)
