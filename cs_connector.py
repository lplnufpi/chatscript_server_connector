import socket


class CSConnection(object):
    def __init__(self, user, botname='harry', ip='localhost', port=1024):
        self.user = user
        self.ip = ip
        self.port = port
        self.botname = botname

    def send(self, message):
        msg = '%s\u0000%s\u0000%s\u0000' % (self.user, self.botname, message)
        msg = str.encode(msg)

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect((self.ip, self.port))
        tcp.send(msg)
        while True:
            chunk = tcp.recv(64)
            if chunk == b'':
                break
            msg = chunk.decode("utf-8")
        tcp.close()
        return msg


if __name__ == '__main__':
    conn = CSConnection('jp')
    msg = conn.send('scare')
    print('>>>> {}'.format(msg))