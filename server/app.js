// Imports the Google Cloud client library
const { PubSub } = require('@google-cloud/pubsub');

const url = 'http://localhost:5002';

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
const topicChannel = 'topics';
const suggestionChannel = 'suggestions';
const voteChannel = 'vote';

const topicSub = pubsub.subscription('topics-sub');
const suggestionSub = pubsub.subscription('suggestions-sub');

const topicHandler = message => {
  console.log(`Topic: ${message.data}:`);
  message.ack();
  postToBot('topic', message.data);
};

const suggestionHandler = message => {
  console.log(`Suggestion: ${message.data}:`);
  message.ack();
  postToBot('suggestion', message.data);
};

// Listen for new messages until timeout is hit
topicSub.on(`message`, topicHandler);
suggestionSub.on(`message`, suggestionHandler);

const postToBot = (endpoint, message) => {
  axios.post(`${url}/${endpoint}s`, {
    [endpoint]: message,
  })
  .then((response) => {
    console.log(response);
  })
  .catch((error) => {
    console.log(error);
  });
}
