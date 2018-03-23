# try to connect to servers using key an get location
import socket
socket.setdefaulttimeout(15)
 
import paramiko
import sys
import threading
import os
import time
 
ipaddresses = []
f=open('lab3-servers','r')
#f=open('lab-servers','r')
#f=open('BnR-server-2change','r')
#f=open('BnR-2-finish','r')
fgood = open('log-lab3-servers.txt', 'a')
fbad = open ('log-lab3-servers.txt', 'a')
fbad.write( "=========== start =====  " + time.ctime() + "\n" )
fgood.write( "=========== start =====  " + time.ctime() + "\n" )
ipaddresses = f.read().splitlines()
#print ipaddresses
#ipaddresses = ['16.59.60.171',  '16.59.60.59', '16.60.184.128']
user = 'root'
passwd = '222'
passwd = 'Xy6stqZ'
key = '/opt/aries/PowerStatus/lsa_chaos.dsa'

#passwd = 'Trustno1'
 
def trylogin(ipaddress):
    global user,passwd
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ipaddress , username=user , password=passwd , key_filename=key )
        #print "-inner ssh\n"
    except paramiko.AuthenticationException:
        fbad.write ("Failed password " + ipaddress + " \n")  
        #print  "[-] Authentication Exception! ..." + ipaddress 
        sys.exit(1)      
    except paramiko.SSHException:
        fbad.write ("Failed " + ipaddress + " \n")
        #print "[-] SSH Exception! ..." + ipaddress 
        sys.exit(1)
    except socket.error:
        fbad.write ("Failed - not linux " + ipaddress + " \n")
        #print "[-] Socket error! probebly not linux machine ...." + ipaddress 
        sys.exit(1)
    #check if the servers have old mount
    #command = "echo "+ipaddress+";grep 'isr.hp.com:'  /etc/fstab | grep '^[^#]' ;  echo '2change =' $?  ; echo $HOSTNAME" 
    #command = "echo "+ipaddress+";zdump -v /etc/localtime | grep 2016 | grep 'Sun Oct 30' > /dev/null ;  echo '2change =' $?  ; echo $HOSTNAME"
    command = "echo " + ipaddress + " ; dmidecode -t1 | grep Ser"
    #command = "echo "+ipaddress+";zdump -v /etc/localtime | grep 2015 | grep 'Sat Oct 30'  ;  echo '2change =' $?  ; echo $HOSTNAME" 
    # if "2change = 0" there is a change to do
    
    #print command
    stdin, stdout, stderr = ssh.exec_command(command )
    serveroutput = stdout.read()
    #print server 
    print serveroutput
    out = ipaddress + " connect "
    #fgood.write(ipaddress + " connect \n")
    #fgood.write(serveroutput)
    
    if "2change = 1" in serveroutput :
       print ipaddress + "----to change"
       out = out + " changing >>>>>"
       command = "echo "+ipaddress+";  echo $HOSTNAME "
       #command = "echo "+ipaddress+";zdump -v /etc/localtime | grep 2016 | grep 'Sun Oct 30'"
       #command = "cd /tmp ; wget -e use_proxy=no 16.60.185.230/timezone.sh; wget -e use_proxy=no 16.60.185.230/Jerusalem; cd /tmp; chmod u+x timezone.sh ; /tmp/timezone.sh"
       stdin, stdout, stderr = ssh.exec_command(command )
       command2output = stdout.read()
       print command2output
    else:
       print ipaddress + "----- is ok"
       out = out + " -is good"
    if "1" == "1":
        #print "nead to change" + ipaddress
        #out = out + " nead to change \n "
        #active the scripts to change the mount"
        #command = "echo $HOSTNAME ; dmidecode -t1 | grep Ser;  uptime"
        #command = "cd /tmp ; cat /etc/profile.d/proxy.sh "
        #command = "cd /tmp ; wget -e use_proxy=no 16.60.185.230/BnR-change-resolv.sh ; chmod u+x /tmp/BnR-change-resolv.sh ; /tmp/BnR-change-resolv.sh "
        print "++++++"
        #stdin, stdout, stderr = ssh.exec_command(command )
        #command2output = stdout.read()
        #print "c2o " + str(command2output)
        #out = out + command2output
    else: 
        out = out + " no change neaded \n"
    fgood.write(out + " \n")
    print out
        
 
try:
    count=0
    while count<len(ipaddresses):
            for i in xrange(10):
                    print "thead loop" 
                    #print count
                    print "count " + str(count) +  " active threds " + str (threading.active_count())
                    threading.Thread(target=trylogin,args=(str(ipaddresses[count]),)).start()
                    while  (threading.active_count() > 200) :
                       #print threading.active_count()
                       time.sleep(0.03)
                    count+=1

except Exception, e:
        print '[-] General Exception'

# wait for the loop to finish
while  (threading.active_count() > 1) :
    print "active threds " + str (threading.active_count())
    time.sleep(0.7)

fbad.write( "=========== STOP =====  " + time.ctime() + "\n" )
fgood.write( "=========== STOP =====  " + time.ctime() + "\n" )
 
