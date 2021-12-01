var Client = require('bitcore-wallet-client');
var utils = require('./cli-utils');
var FileStorage = require('./filestorage');

  


utils.getClient( { mustExist: true }, function (client) {

    var txpid = '6723b6ae-30f0-4dd1-aee6-145fa2a6216b'
    client.getTxProposals({}, function(err, txps) {
      utils.die(err);
      var txp = utils.findOneTxProposal(txps, txpid);
      
	  
	  /*client.signTxProposal(txp, function(err, tx) {
        utils.die(err);
        console.log('Transaction signed by you.');
		client.broadcastTxProposal(txp, function(err, txp) {
			utils.die(err);
			console.log('Transaction Broadcasted: TXID: ' + txp.txid);
		});
      });*/
	  
	  
	  client.removeTxProposal(txp, function(err) {
		utils.die(err);
		console.log('Transaction removed.');
	  });
	  
    });
	


});