const bodyParser = require('body-parser');
const express = require('express');
const app = express();

// Imports the Google Cloud client library
const { PubSub } = require('@google-cloud/pubsub');

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

// Creates a client
const projectId = 'huddle72';
const pubsub = new PubSub({ projectId });
const topics = 'topics';
const suggestions = 'suggestions';
const voteChannel = 'vote';

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.get('/', (req, res) => {
  res.json({ payload: 'Welcome to the Emotivote server!' });
});

app.get('/topic', (req, res) => {
  res.json({ topic: currentTopic });
});

app.post('/topic', async (req, res) => {
  try {
    const { topic } = req.body;
    if (topic) {
      currentTopic = topic;
      console.log(`Current topic being discussed: ${currentTopic}`);

      const data = JSON.stringify({ payload: currentTopic });
      const dataBuffer = Buffer.from(data);
      const messageId = await pubsub.topic(voteChannel).publish(dataBuffer);
      console.log(`Message ${messageId} published.`);

      res.json({ topic: currentTopic });
    }
  } catch(err) {
    console.log(err);
  }
});

app.get('/suggestions', (req, res) => {
  res.json({ suggestions: currentSuggestions });
});

app.post('/suggestions', async (req, res) => {
  const { suggestion } = req.body;
  if (suggestion) {
    currentSuggestions = [...currentSuggestions, suggestion];
    console.log(`Current suggestions: ${currentSuggestions}`);
    res.json({ suggestions: currentSuggestions });
  }
});

app.get('/votes/video', (req, res) => {
  res.json({ votes: currentVotes });
})

app.post('/votes/video', (req, res) => {
  let votes = req.body.votes;
  currentVotes = [currentVotes, ...votes];
  console.log(`Current votes: ${currentVotes}`);
  res.json({ votes: currentVotes });
});

app.get('/votes/speech', (req, res) => {
  res.json({ votes: currentVotes });
})

app.post('/votes/speech', (req, res) => {
  res.json({ votes: currentVotes });
});

const port = process.env.IP || 3000;
app.listen(port, async () => {
  console.log(`Emotivote server running on port ${port}`);
});
