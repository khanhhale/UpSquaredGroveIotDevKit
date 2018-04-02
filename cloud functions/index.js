/**
 * Triggered from a message on a Cloud Pub/Sub topic.
 *
 * @param {!Object} event The Cloud Functions event.
 * @param {!Function} The callback function.
 */
const monitoring = require('@google-cloud/monitoring');
const client = new monitoring.MetricServiceClient();
// Your Google Cloud Platform project ID
const projectId = "cloud-iot-testing-185623";


exports.subscribe = (event, callback) => {
  // The Cloud Pub/Sub Message object.
  const pubsubMessage = event.data;
  //const metricType = "custom.googleapis.com/cloudiot/thsensors"; // for temperature and humidity
  //const metricType = "custom.googleapis.com/cloudiot/lightsensors"; //for light sensor
  const metricType = "custom.googleapis.com/cloudiot/rotarysensors"; //for rotary sensor
  //attributes
  // We're just going to log the message to prove that
  // it worked.
  console.log(Buffer.from(pubsubMessage.data, 'base64').toString());

  var pat = /^(.*)[:]\s\((.+)\)/gi;
  var str = Buffer.from(pubsubMessage.data, 'base64').toString();
  var fstr = pat.exec(str);
  var dataPoints = fstr[2].split(",");  
  var dataPointsDesc = fstr[1].split(",");
  // Don't forget to call the callback.
  
for(dsize = 0;dsize < dataPoints.length;dsize++)
{   
  var dpDesc = dataPointsDesc[dsize];
   
  const dataPoint = {
  interval: {
    endTime: {
      seconds: Date.now() / 1000,
    },
  },
  value: {
    doubleValue: parseFloat(dataPoints[dsize]),
  },
};

const timeSeriesData = {
  metric: {
    type: metricType,
    labels: {
      dpDesc: dataPointsDesc[dsize],
    },
  },
  resource: {
    type: 'global',
    labels: {
      'project_id': projectId
    },
  },
  points: [dataPoint],
};

const request = {
  name: client.projectPath(projectId) + "/metricDescriptors/" + metricType,
  timeSeries: [timeSeriesData],
};

// Writes time series data
client
  .createTimeSeries(request)
  .then(results => {
    console.log(`Done writing time series data.`, results[0]);
  })
  .catch(err => {
    console.error('ERROR:', err);
  });
}  
  callback();
};
