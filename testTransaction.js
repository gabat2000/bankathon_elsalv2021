var Client = require('bitcore-wallet-client');
var utils = require('./cli-utils');
var FileStorage = require('./filestorage');

  
function send(client, address, amount, fee, note) { 
  var amount, feePerKb;
  try {
    feePerKb = utils.parseAmount(fee);
	amount = utils.parseAmount(amount);
  } catch (ex) {
    utils.die(ex);
  }

  console.log(feePerKb);
  client.createTxProposal({
    outputs: [{
      toAddress: address,
      amount: amount,
    }],
    message: note,
    feePerKb: feePerKb,
  }, function(err, txp) {
    utils.die(err);
    client.publishTxProposal({
      txp: txp
    }, function(err, txp) {
      utils.die(err);
      console.log(' * Tx created: ID %s [%s] RequiredSignatures:', txp.id, txp.status, txp.requiredSignatures);
	  client.signTxProposal(txp, function(err, tx) {
        utils.die(err);
        console.log('Transaction signed by you.');
		client.broadcastTxProposal(txp, function(err, txp) {
			utils.die(err);
			console.log('Transaction Broadcasted: TXID: ' + txp.txid);
		});
      });
    });
  });
};


utils.getClient( {
  mustExist: true
}, function(client) {
	
  var addr = 'mhS4RnMqMARWFoYd3XV4QpbE3kNYhX2qVy'
  var amount = '0.0001btc'
  var fee = '0.00001btc'
  var note = 'Test Tx'

  send(client, addr, amount, fee, note);
  
});