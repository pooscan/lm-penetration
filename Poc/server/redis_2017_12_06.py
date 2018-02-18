import socket

class RedisPOC():
    appName     = ''
    appVersion  = ''
    vulType     = ''
    desc        = '''
                redis未授权访问
                '''
    def verify(host, port=6379):
        result = {}
        #info
        payload = "\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a"
        s = socket.socket()
        socket.setdefaulttimeout(20)
        try:
            print(host)
            s.connect((host, port))
            s.send(payload)
            recvdata = s.recv(1024)
            # repr(recvdata)
            print(recvdata )
            if recvdata and 'redis_version' in recvdata:
                result['VerifyInfo']  = {}
                result['URL'] = host
                result['Port'] = port
                result['Data'] = recvdata
        except:
            print("bb")
            pass
        s.close()
        return result