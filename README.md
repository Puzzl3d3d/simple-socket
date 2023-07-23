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

`simpleSocket(ip=string, port=int, auto_convert=bool, debug=bool)`

### ip
The server IP

On the server itself, this value usually does not need to be changed, as it automatically hosts it on your own ip.

### port
The port of the program

### auto_convert
When enabled, it treats all incoming data from the client/server as a JSON string, and automatically converts it using `json.loads`

This setting is recommended, but enabling it isn't required

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
As stated above in the `auto_convert` specificatiion, the `convert=bool` keyword argument of the sending data functions can be used instead of treating every piece of incoming data as JSON, instead going case-by-case
