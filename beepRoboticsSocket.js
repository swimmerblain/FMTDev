const http = require('http');
const WebSocket = require('ws');
const { randomUUID } = require('crypto');

const PORT = 4007
const server = http.createServer();
const wss = new WebSocket.WebSocketServer({noServer: true});

var live = false;
var liveFilename = "";
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
            case "currentArmPosition":
                //console.log(live)
                //console.log(incoming.data)
                //console.log("Current Position:")
                outgoing = {
                    msg: "curArmPosition",
                    data: incoming.data
                }
                if (live){
                    sendToAll(wss.clients, ws, JSON.stringify(outgoing));
                }
                break;
            case "ArmPosition":
                //console.log("new Position:")
                //console.log(incoming.data)
                outgoing = {
                    msg: "newArmPosition",
                    data: incoming.data
                }
                if (live){
                    sendToAll(wss.clients, ws, JSON.stringify(outgoing))
                }
                break;
            case "handPos":
                //console.log(incoming.data)
                outgoing = {
                    msg: "newHandPos",
                    data: incoming.data
                }
                if (live){
                    sendToAll(wss.clients, ws, JSON.stringify(outgoing))
                }
                break;
            case "currentHandPos":
                //console.log(incoming.data)
                outgoing = {
                    msg: "curHandPos",
                    data: incoming.data
                }
                if (live){
                    sendToAll(wss.clients, ws, JSON.stringify(outgoing))
                }
                break;
			case "pushButton":
                //console.log(incoming.data)
                outgoing = {
                    msg: "pushButton",
                    data: incoming.data
                }
                if (live){
                    sendToAll(wss.clients, ws, JSON.stringify(outgoing))
                }
                break;
            default:
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
