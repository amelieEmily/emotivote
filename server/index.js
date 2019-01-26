const bodyParser = require('body-parser');
const express = require('express');
const app = express();

connectedClients = [];
currentTopic = 'IC Hack 2019'
currentSuggestions = [];
currentVotes = [
  {
    positive: 0.5,
    negative: 0.3,
    neutral: 0.2
  },
  {
    positive: 0.7,
    negative: 0.3,
    neutral: 0
  },
  {
    positive: 0.35,
    negative: 0.25,
    neutral: 0.4
  },
]

app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.send('Welcome to the Emotivote server!');
});

app.get('/topic', (req, res) => {
  res.json({ topic: currentTopic });
});

app.post('/topic', (req, res) => {
  const { topic } = req.body;
  currentTopic = topic;
  let response = `Current topic being discussed: ${currentTopic}`;
  console.log(response);
  res.send(response);
});

app.get('/suggestions', (req, res) => {
  res.json({ suggestions: currentSuggestions });
});

app.post('/suggestions', (req, res) => {
  const { suggestion } = req.body;
  if (suggestion) {
    currentSuggestions = [currentSuggestions, suggestion];
    console.log(`Current suggestions: ${currentSuggestions}`);
    res.send(`New suggestion created: ${suggestion}`);
  }
});

app.post('/votes', (req, res) => {
  let votes = req.body.votes;
  currentVotes = [currentVotes, ...votes];
  res.send(`New vote registered: ${votes}`);
});

app.get('/votes', (req, res) => {
  res.json({ votes: currentVotes });
})

const port = process.env.IP || 3000;
app.listen(port, () => {
  console.log(`Emotivote server running on port ${port}`);
});
