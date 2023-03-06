const http = require('http');
const WebSocket = require('ws');
const { randomUUID } = require('crypto');

const PORT = 4007
const server = http.createServer();
const wss = new WebSocket.WebSocketServer({noServer: true});

var live = false;
var liveFilename = "asdfasdf";
var sceneObjs = [];

var sendToAll = (socket, self, message) => {
    socket.forEach(client => {
        if (client !== self)
            client.send(message);
    });
}

var sendToSelf = (socket, message) => {
    socket.send(message);
}

wss.on('connection', (ws, req) => {

    ws.connectionID = randomUUID();
    console.log(`new_connection id=${ws.connectionID}`);

    ws.send(JSON.stringify({
        msg: "liveSession",
        data: {
            live: live,
            filename: liveFilename,
            object: sceneObjs,
        }
    }));

    ws.on('message', message => {
        // console.log(`message id=${ws.connectionID} data=${message}`);

        let incoming = JSON.parse(message);
        //console.log(incoming.msg)

        let outgoing = ""
        switch (incoming.msg){
            case "isActiveSession":
                outgoing = JSON.stringify({
                    msg: "isActiveSession",
                    data: {
                        live: live,
                        filename: liveFilename,
                        object: sceneObjs
                    }
                })
                sendToSelf(ws, outgoing);
                break;
            case "terminateSession":
                live = false;
                liveFilename = "";
                sceneObjs = [];

                outgoing = JSON.stringify({
                    msg: "terminateSession",
                    data: {}
                });
                sendToAll(wss.clients, ws, outgoing);
                sendToSelf(ws, outgoing);
                break;
            case "setLiveSession":
                live = incoming.data.live;
                liveFilename = incoming.data.filename;
                break;
            case "setSessionObjects":
                sceneObjs = incoming.data.objects;
                break;
            case "updateObject":
                outgoing = {
                    msg: "updateObject",
                    data: incoming.data
                }

                if (live){
                    sendToAll(wss.clients, ws, JSON.stringify(outgoing)); 
                }
                break;
            //Includes arm and hand position and state
            case "robotFDBK":
                //console.log(live)
                //console.log(incoming.data)
                //console.log("Current Position:")
                outgoing = {
                    msg: incoming.msg,
                    data: incoming.data
                }
                console.log(outgoing)

                sendToAll(wss.clients, ws, JSON.stringify(outgoing));

                break;



            case "dashboardData":
                //console.log(`message id=${ws.connectionID} data=${message}`);
                outgoing = {
                    msg: incoming.msg,
                    data: incoming.data

                }
                //console.log(outgoing)

                sendToAll(wss.clients, ws, (outgoing))


                break;
            case "dashboardCMD":
                //console.log(`message id=${ws.connectionID} data=${message}`);
                outgoing = {
                    msg: "dashboardCMD",
                    data: incoming.data
                }

                    sendToAll(wss.clients, ws, JSON.stringify(outgoing))

    
                break;
            case "Casual Test":
		        console.log(`correct message`);
                console.log(`message id=${ws.connectionID} data=${message}`);
                outgoing = {
                    msg: message['msg'],
                    data: "message recieved"
                }
                if (live){
                    sendToAll(wss.clients, ws, JSON.stringify(outgoing))
                }
        
                break;
                
            
            
            default:
		        console.log(JSON.parse(message));
                sendToAll(wss.clients, ws, message);
        }
    });

    ws.on('close', message => {
        console.log(`closed connection id=${ws.connectionID} data=${message}`);
        live = false
        liveFilename = ""
    });
});

server.on('upgrade', (req, socket, head) => {
    wss.handleUpgrade(req, socket, head, ws => wss.emit('connection', ws, req));
});

server.listen(PORT, () => console.log(`socket server listening on ws://localhost:${PORT}`));
