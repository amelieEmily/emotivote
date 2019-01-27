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

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.get('/', (req, res) => {
  res.json({ payload: 'Welcome to the Emotivote server!' });
});

app.get('/topic', (req, res) => {
  res.json({ topic: currentTopic });
});

app.post('/topic', (req, res) => {
  const { topic } = req.body;
  currentTopic = topic;
  console.log(`Current topic being discussed: ${currentTopic}`);
  res.json({ topic: currentTopic });
});

app.get('/suggestions', (req, res) => {
  res.json({ suggestions: currentSuggestions });
});

app.post('/suggestions', (req, res) => {
  const { suggestion } = req.body;
  if (suggestion) {
    currentSuggestions = [...currentSuggestions, suggestion];
    console.log(`Current suggestions: ${currentSuggestions}`);
    res.json({ suggestions: currentSuggestions });
  }
});

app.get('/votes', (req, res) => {
  res.json({ votes: currentVotes });
})

app.post('/votes', (req, res) => {
  let votes = req.body.votes;
  currentVotes = [currentVotes, ...votes];
  console.log(`Current votes: ${currentVotes}`);
  res.json({ votes: currentVotes });
});

const port = process.env.IP || 3000;
app.listen(port, () => {
  console.log(`Emotivote server running on port ${port}`);
});
