//var Client = require('bitcore-wallet-client');
//var utils = require('./cli-utils');
//var FileStorage = require('./filestorage');
//const fetch = require('node-fetch');
const fetch = require('sync-fetch')

let token;
var obAuth = function() {};

function send(user,pass,key) {
    var urlbase;
    var urlvariable;
    urlbase="https://obp-apisandbox.bancohipotecario.com.sv/"
    urlvariable = "my/logins/direct";
    var ItemJSON;
    return fetch(urlbase+urlvariable, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'DirectLogin username='+user+', password='+pass+', consumer_key='+key
      },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      //body: JSON.stringify(data) // body data type must match "Content-Type" header
    }).json()
    ;    
  }

  obAuth.auth = function(){
    var user = 'gabat2000@gmail.com'
    var pass = '123456789!'
    var key = '1q1v1b1cpwka2otruxkz5egqexryrksxabrxg5ef'
    let ttt = send(user, pass, key);
    console.log(ttt);
    return ttt;
}
module.exports = obAuth;
