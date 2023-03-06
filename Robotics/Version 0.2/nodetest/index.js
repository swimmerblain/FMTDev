const express = require('express');
const https = require('https');
const fs = require('fs');
const app = express();

const PORT = 4006;

https.createServer({
    cert: fs.readFileSync('certs/myCA.pem'),
    key: fs.readFileSync('certs/myCA.key'),
    passphrase: "1111"
}, app).listen(PORT, function (req, res) {console.log(`Listening on port ${PORT}`)})


app.get("/", (req, res) => {
    res.send("yoooo")
})

app.get("/about", (req, res) => {
    res.send("about")
})

//app.listen(PORT, () => {
//    console.log(`listening on port ${PORT}`)
//})

