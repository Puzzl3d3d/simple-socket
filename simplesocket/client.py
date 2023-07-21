import socket, os, json, threading

hostname = socket.gethostname()
client_ip = socket.gethostbyname(hostname)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class simpleSocket:
    def __init__(self, *args, ip=client_ip, port=1, auto_convert=False, debug=True):
        global client_socket

        self.hostname = socket.gethostname()
        self.client_ip = socket.gethostbyname(self.hostname)

        self.ip = ip
        self.port = port

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Variables
        self.auto_convert = auto_convert

        self.threads = []

        if debug: 
            self.print = print
        else:
            self.print = lambda *args: 0
    def init(self):
        # Connect to the server
        while True:
            try:
                client_socket.connect((self.ip, self.port))
                self.print('Connected to {}:{}'.format(self.ip, self.port))
                break
            except Exception as error:
                self.print(f"Could not connect to server: {error} | This may be because the server hasn't started yet\nRetrying...")

        self.makeThread(target=self._onConnect, daemon=True)
        self.makeThread(target=self._startRecieving, daemon=True).join()

    def _onConnect(self):
        # Example function
        while True:
            data = input("Send message to server: ")

            self.toServer(data, convert=False)
    def _onDataRecieve(self, data):
        self.print("Server sent data:",data)
        pass
    def _startRecieving(self):
        while True:
            try:
                data = client_socket.recv(1024 * 20).decode()

                if data:

                    if self.auto_convert:
                        data = self.fromJSON(data)

                    try:
                        self._onDataRecieve(data)
                    except Exception as error:
                        print("Could not handle data recieved:",data,"|",error)
            except (ConnectionResetError, ConnectionAbortedError):
                self.print("Disconnected from server, retry connection")
                return
    # Bind / Decorator functions
    def bindConnect(self, func):
        self._onConnect = func
    def bindRecieve(self, func):
        self._onDataRecieve = func

    # Public functions
    def fromJSON(self, json_string):
        json_string = json_string.split("}{")
                
        if len(json_string) > 1:
            for i in range(0, len(json_string), 1):
                json_string[i] = "{"+json_string[i]+"}"
            json_string[0] = json_string[0][1:]
            json_string[-1] = json_string[-1][0:-1]

        data = []

        for json_string in json_string:
            try:
                data.append(json.loads(json_string))
            except json.decoder.JSONDecodeError:
                self.print("Could not convert JSON:",json_string)
        
        return data if len(data) > 1 else data[0]
    def toJSON(self, data):
        try:
            return json.dumps(data)
        except:
            self.print("Could not convert data:",data)
    def toServer(self, data, convert=False):
        if convert or not isinstance(data, str):
            data = self.toJSON(data)
        
        client_socket.send(data.encode())
    def getSocket(self):
        return client_socket
    def getServerIP(self):
        return self.ip
    def getServerPort(self):
        return self.port
    def makeThread(self, *args, **kwargs):
        thread = threading.Thread(*args, **kwargs)
        self.threads.append(thread)
        thread.start()
        return thread

if __name__ == "__main__":
    client = simpleSocket()

    client.init()
