//var Client = require('bitcore-wallet-client');
//var utils = require('./cli-utils');
//var FileStorage = require('./filestorage');
//const fetch = require('node-fetch');
const fetch = require('sync-fetch')
var obAuth = require('./obAuth');

function send(token,datosBanco) {
    var urlbase;
    var urlvariable;
    urlbase="https://obp-apisandbox.bancohipotecario.com.sv/"
    urlvariable = "obp/v4.0.0/banks";
    var ItemJSON;
    return fetch(urlbase+urlvariable, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'DirectLogin token='+token
      },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: datosBanco // body data type must match "Content-Type" header
    }).json();
  }
var datosBanco = '{"id":"tl2.es","short_name":"Test2Tl ","full_name":"Test2Tla","logo":"logo","website":"www.opentla.com","bank_routings":[{"scheme":"Bank_ID","address":"tl2.es"}],"attributes":[{"name":"ACCOUNT_MANAGEMENT_FEE","value":"5000000"}]}';
var token = obAuth.auth()
var resp = send(token['token'],datosBanco);
console.log(resp);
