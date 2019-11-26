import socket


class CSConnection(object):
    """Class to connect and send messages to ChatScript Server."""

    def __init__(self, user, botname='harry', ip='localhost', port=1024):
        """Init the connection.

        Args:
            user (str): Username that will be sended in every message.
            botname (str): Chatbot that will be used. Default 'harry'.
            ip (str): IP address to ChatScript server. Default
                'localhost'.
            port (int): Port number to ChatScript server. Default
                '1024'.
        """
        self.user = user
        self.ip = ip
        self.port = port
        self.botname = botname

    def send(self, message):
        """This method is used to send message to the bot.

        Args:
            message (str): Message to send.

        Returns:
            str: Returned message from the bot.
        """
        msg = '%s\u0000%s\u0000%s\u0000' % (self.user, self.botname, message)
        msg = str.encode(msg)

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect((self.ip, self.port))
        tcp.send(msg)
        while True:
            chunk = tcp.recv(2048)
            if chunk == b'':
                break
            msg = chunk.decode("utf-8")
        tcp.close()
        return msg


if __name__ == '__main__':
    conn = CSConnection('username')
    msg = conn.send('Hello')
    print('>>>> {}'.format(msg))