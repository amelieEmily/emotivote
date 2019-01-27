// Imports the Google Cloud client library
const express = require('express');
const { PubSub } = require('@google-cloud/pubsub');
const axios = require('axios');

const app = express();

const url = 'http://192.168.99.100:5002';

currentTopic = 'IC Hack 2019'
currentSuggestion = '';
currentVotes = [];

// Creates a client
const projectId = 'huddle72';
const pubsub = new PubSub({ projectId });
const voteChannel = 'vote';

const topicSub = pubsub.subscription('topics-sub');
const suggestionSub = pubsub.subscription('suggestions-sub');
const voteSub = pubsub.subscription('vote-sub');

console.log('Server ready!');

const topicHandler = message => {
  console.log(`Topic: ${message.data}`);
  message.ack();
  currentTopic = message.data;
  postToBot('topic', message.data);
};

const suggestionHandler = async message => {
  console.log(`Suggestion: ${message.data}`);
  message.ack();
  currentSuggestion = message.data;
  postToBot('suggestion', currentSuggestion);
  currentVotes = [];

  data = JSON.stringify({ suggestion: currentSuggestion });
  const dataBuffer = Buffer.from(data);
  const messageId = await pubsub.topic(voteChannel).publish(dataBuffer);
  console.log(`Message ${messageId} published.`);
};

const voteHandler = message => {
  console.log(`Vote results: ${message.data}`);
  message.ack();
  currentVotes = [...currentVotes, message.data.toString()];
};

const postToBot = (endpoint, message) => {
  axios.post(`${url}/${endpoint}`, {
    [endpoint]: message.toString(),
  })
  .then((response) => {
    console.log(response);
  })
  .catch((error) => {
    console.log(error.message);
  });
}

topicSub.on(`message`, topicHandler);
suggestionSub.on(`message`, suggestionHandler);
voteSub.on(`message`, voteHandler);

app.get('/votes', (req, res) => {
  res.json({ votes: currentVotes });
});

const port = 3000;
app.listen(port, () => {
  console.log(`Express server running on port ${port}`);
});
