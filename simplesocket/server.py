import socket, os, json, threading

hostname = socket.gethostname()
server_ip = socket.gethostbyname(hostname)

clients = {}
threads = []

# Variables
auto_convert_data = False

# Private methods
def _onNewSocket(client_socket):
    pass
def _onDataRecieve(client_socket, data):
    print(clients[client_socket][0],"sent data:",data)
    pass
def _startRecieving(client_socket):
    while True:
        try:
            data = client_socket.recv(1024 * 20).decode()

            if data:

                if auto_convert_data:
                    data = fromJSON(data)

                _onDataRecieve(client_socket, data)
        except ConnectionResetError:
            print(clients.get(client_socket, "Client"),"disconnected")
            if clients.get(client_socket): clients.pop(client_socket)
            break
def _listenForClients():
        while True:
            print("Waiting for client to connect")
            client_socket, client_address = server_socket.accept()
            print(f"Connected with {client_address[0]}:{client_address[1]}")
            clients[client_socket] = client_address
            _onNewSocket(client_socket)
            makeThread(target=_startRecieving, daemon=True, args=(client_socket,))

# Bind / Decorator functions
def bindNewSocket(func):
    global _onNewSocket
    _onNewSocket = func
def bindRecieve(func):
    global _onDataRecieve
    _onDataRecieve = func

# Public functions
def fromJSON(json_string):
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
            print("Could not convert JSON:",json_string)
    
    return data if len(data) > 1 else data[0]
def toJSON(data):
    try:
        return json.dumps(data)
    except:
        print("Could not convert data:",data)
def toClient(client_socket, data, convert=False):
    if convert or not isinstance(data, str):
        data = toJSON(data)
    
    client_socket.send(data.encode())
def allClients(data, convert=False):
    if convert or not isinstance(data, str):
        data = toJSON(data)

    for client_socket in clients.keys():
        toClient(client_socket, data, convert=False)
def getSocketFromAddress(client_address):
    try:
        return list(clients.keys())[list(clients.values()).index(client_address)]
    except:
        return None
def getAddressFromSocket(client_socket):
    return clients.get(client_socket, None)
def makeThread(*args, **kwargs):
    thread = threading.Thread(*args, **kwargs)
    threads.append(thread)
    thread.start()
    return thread
def joinThreads():
    for thread in threads:
        thread.join()

def init(ip=server_ip, port=1000, debug=True):
    global server_socket

    if not debug: 
        global print
        def print(*args): return
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((ip, port))

    server_socket.listen(1)

    print(f"Server listening on {ip}:{port}")

    # Start listening for client connections
    makeThread(target=_listenForClients, daemon=True).join()

    return server_socket

class simpleSocket:
    def __init__(self, *args, ip=server_ip, port=1000, auto_convert=False, debug=True):
        self.clients = {}
        self.threads = []

        # Variables
        self.auto_convert = auto_convert

        if debug: 
            self.print = print
        else:
            self.print = lambda *args: 0

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.bind((ip, port))

        self.server_socket.listen(1)

        self.print(f"Server listening on {ip}:{port}")

        # Start listening for client connections
        self.makeThread(target=self._listenForClients, daemon=True).join()

    # Private methods
    def _onNewSocket(self, client_socket):
        pass
    def _onDataRecieve(self, client_socket, data):
        self.print(self.clients[client_socket][0],"sent data:",data)
        pass
    def _startRecieving(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024 * 20).decode()

                if data:

                    if self.auto_convert:
                        data = self.fromJSON(data)

                    self._onDataRecieve(client_socket, data)
            except ConnectionResetError:
                print(self.clients.get(client_socket, "Client"),"disconnected")
                if self.clients.get(client_socket): self.clients.pop(client_socket)
                break
    def _listenForClients(self):
            while True:
                self.print("Waiting for client to connect")
                client_socket, client_address = self.server_socket.accept()
                self.print(f"Connected with {client_address[0]}:{client_address[1]}")
                self.clients[client_socket] = client_address
                self._onNewSocket(client_socket)
                self.makeThread(target=self._startRecieving, daemon=True, args=(client_socket,))

    # Bind / Decorator functions
    def bindNewSocket(self, func):
        self._onNewSocket = func
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
                print("Could not convert JSON:",json_string)
        
        return data if len(data) > 1 else data[0]
    def toJSON(self, data):
        try:
            return json.dumps(data)
        except:
            print("Could not convert data:",data)
    def toClient(self, client_socket, data, convert=False):
        if convert or not isinstance(data, str):
            data = self.toJSON(data)
        
        client_socket.send(data.encode())
    def allClients(self, data, convert=False):
        if convert or not isinstance(data, str):
            data = self.toJSON(data)

        for client_socket in self.clients.keys():
            self.toClient(client_socket, data, convert=False)
    def getSocketFromAddress(self, client_address):
        try:
            return list(self.clients.keys())[list(self.clients.values()).index(client_address)]
        except:
            return None
    def getAddressFromSocket(self, client_socket):
        return self.clients.get(client_socket, None)
    def makeThread(self, *args, **kwargs):
        thread = threading.Thread(*args, **kwargs)
        self.threads.append(thread)
        thread.start()
        return thread


if __name__ == "__main__":
    init()