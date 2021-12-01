var Client = require('bitcore-wallet-client');
var utils = require('./cli-utils');
var FileStorage = require('./filestorage');

  


utils.getClient( { mustExist: true }, function (client) {

    var txpid = '921f9cfc-8a7b-4ad9-952d-396e9c0c771b'
    client.getTxProposals({}, function(err, txps) {
      utils.die(err);
	  console.log(txps);
      var txp = utils.findOneTxProposal(txps, txpid);
      
	  client.signTxProposal(txp, function(err, tx) {
        utils.die(err);
        console.log('Transaction signed by you.');
      });
	  
	  client.broadcastTxProposal(txp, function(err, txp) {
      utils.die(err);
      console.log('Transaction Broadcasted: TXID: ' + txp.txid);
    });
    });
	


});