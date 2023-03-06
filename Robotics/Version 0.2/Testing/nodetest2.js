/*const https = require('https');

https.get('https://ab1.bot/?inst=regulatory-pink-basilisk&gridPortal=home', (resp) => {
  let data = '';

  // A chunk of data has been received.
  resp.on('data', (chunk) => {
    data += chunk;
  });

  // The whole response has been received. Print out the result.
  resp.on('end', () => {
    console.log(data)
    //console.log(JSON.parse(data).explanation);
  });

}).on("error", (err) => {
  console.log("Error: " + err.message);
//});
*/
const https = require('https');
var request = require('request');

request.put(
    //First parameter API to make post request
    'https://reqres.in/api/users/2',

    //Second parameter Data which has to be sent to API
    { json: {
        "name": "morpheus",
        "job": "zion resident"
      }
    },
    
    //Thrid parameter Callack function  
    function (error, response, body) {
        if (!error && response.statusCode == 200) {
            console.log(body);
            console.log(response.statusCode);
        }
    }
);
