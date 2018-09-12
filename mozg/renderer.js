// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
var AWS = require('aws-sdk');

AWS.config.update({region: 'eu-central-1'});
AWS.config.update({accessKeyId: process.env.AWS_wiankor_1, secretAccessKey: process.env.AWS_wiankor_2});

var success = $("#success");
var fail = $("#fail");

// Create an SQS service object
var sqs = new AWS.SQS({apiVersion: '2012-11-05'});

function sendNrOfCycles(queue) {
  var nrOfCycles = $("#nrOfCycles").val();
  var params = {
   MessageBody: "nrOfCycles="+nrOfCycles,
   QueueUrl: queue
  };
  sqs.sendMessage(params, function(err, data) {
    if (err) {
      fail.removeClass('hidden').text('Nie można wysłac wiadomosci do SQS: ' + queue)
    } else {
      success.removeClass('hidden').text('Wiadomosc wyslana do SQS.')
    }
  });
}

$("#motorSend").on("click", function (e) {
  e.preventDefault();
  sendNrOfCycles("https://sqs.eu-central-1.amazonaws.com/719069272797/wiankor-silnik");
  sendNrOfCycles("https://sqs.eu-central-1.amazonaws.com/719069272797/wiankor-silnik-odwrocony");

  return false;
});
