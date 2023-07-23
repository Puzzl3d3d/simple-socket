# simple-socket
Python module for a simple server+client functionality for the `socket` module!

This can be used to make messaging services (like in the example folder), multiplayer games, and more!

## Server setup:

First, copy over the simpleSocket class and all the modules into your own server file. 
Then you can bind 3 different events for each client:

`onRecieve(client_socket, data)` --> When a client socket sends a message to the server

`onConnect(client_socket)` --> When a new client connects to the server

`onDisconnect(client_socket)` --> When a client disconnects from the server

## Client setup

Like the server, copy over the simpleSocket class and all the modules into your client file.
Then there are 2 events to bind:

`onRecieve(data)` --> When the client recieves a message from the server

`onConnect()` --> Called once, when the client first connects to the server.

## Initalisation

If you want more customisation over your setup, there are 4 arguments to parse into the __init__ function

`simpleSocket(ip=string (defaults to connected network ip), port=int (defaults to 1), auto_convert=bool (defaults to False), debug=bool (defaults to True))`

### ip
The server IP

On the server itself, this value usually does not need to be changed, as it automatically hosts it on your own ip.

### port
The port of the program

### auto_convert
When enabled, it treats all incoming data from the client/server as a JSON string, and automatically converts it using `json.loads`

This setting is recommended, but enabling it isn't required as you can instead use the `convert` keyword argument for a case-by-case approach.

Without `auto_convert`, you will also need to manually convert all incoming data, but you can use the built in `fromJSON(jsonString)` function to do this.

## Sending data

Sending data from the client to the server or vice-versa goes as follows:

### Server
There are 2 options, sending data to only one client

`toClient(client_socket, data, convert=bool)`

or "broadcasting" across every client 

`allClients(data, convert=bool)`

### Client
For the client, you would use `toServer(data, convert=bool)`

### Conversion
As stated above in the `auto_convert` specification, the `convert=bool` keyword argument of the sending data functions can be used instead of treating every piece of data as JSON, instead going case-by-case

## Other functions

### fromJSON(jsonString)
Converts any jsonString into a dictionary.

Sometimes the recieve function can pick up multiple packets of data at the same time if the client sends them too fast. This *would* cause an error, but in the function, if more than one json tavle is detected, it will return a list of each json string identified. 
#### Disclaimer:
This function isnt foolproof. If the client sends a message that contains the string "}{", it will think there is more than one json table inside the message, so it would be unsuccessful. This shouldn't happen though, so it isn't a massive issue. I plan to fix this, but for now I don't think it is too important.

### toJSON(data)
Converts any data into a JSON string

### getSocketFromAddress(client_address)
Client addresses are stored in the `simpleSocket.clients` dictionary when the client first connects. Most of the time this isn't needed, but the client address stores the ip and port from the connecting client.

This function returns the client_socket from that client address by looking it up in the dictionary.

### getAddressFromSocket(client_socket)
Reverse of the `getSocketFromAddress` function.

### makeThread(*args, **kwargs)
Makes and starts a thread for parallel scripting using the `threading` module.

Parses all arguments into the `threading.Thread` function

## Client only:

### getSocket()
Returns the `client_socket`

### getServerIP()
Returns the ip of the server (from the __init__ function)

### getServerPort()
Returns the port of the server (from the __init__ function)

## Server only:

### getPublicIP() (Server)
Returns the public ipv4 of the server. Used in the client for connecting to the server
