const bodyParser = require('body-parser');
const express = require('express');
const app = express();

connectedClients = [];
currentTopic = 'IC Hack 2019'
currentSuggestions = [];
currentVotes = [];

app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.send('Welcome to the Emotivote server!');
});

app.post('/topic', (req, res) => {
  currentTopic = req.body.topic;
  res.send(`Current topic being discussed: ${currentTopic}`);
});

const port = process.env.IP || 3000;
app.listen(port, () => {
  console.log(`Emotivote server running on port ${port}`);
});
