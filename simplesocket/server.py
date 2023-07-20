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
            print(clients[client_socket],"disconnected")
            clients.pop(client_socket)
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

if __name__ == "__main__":
    init()