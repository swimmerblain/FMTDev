const http = require('http')

const server = http.createServer(function(request, response) {
    console.dir(request.param)

    if (request.method == 'POST') {
        console.log('POST')
        var body = ''
        request.on('data', function(data){
            body += data
            console.log('partial body: ' + body)
        })
        request.on('end', function() {
            console.log('body: ', body)
            response.writeHead(200, {'content': 'testcontent'})
            response.end('post received')
        })

    }
    else {
        console.log('GET')
    }
})

const port = 3000
const host = '10.5.100.78'
server.listen(port, host)
console.log('listening on http://${host}:${port}')
