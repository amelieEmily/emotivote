# emotivote
Emotivote is an anonymous voting system based on sentiment analysis of speech and video over conference calls, allowing you to easily understand how your team might be feeling about various suggestions brought up during your meetings to help make better decisions.

Emotivote first uses Google Cloud Speech and Dialogflow to identify 'topic' and 'suggestion' keywords from meeting conversations. Afterwards, Microsoft Azure's Face API is used to perform facial analysis of all participants in the meeting and determine a negative/positive score of how they feel about the ideas being suggested. Emotivote manifests itself in the form of a chat bot on Cisco's Webex Meetings, which communicates with a Node.js backend, that your team can communicate with to obtain a real-time, aggregated sentiment score on suggestions from all participants. The chat bot also keeps track of all the topics and suggestions being discussed.

## Inspiration
Remember when your team couldn't decide on what to build for ICHack19? Or when your team can never seem to come to a decision from meetings and thus wastes a lot of time?

Fret not, we faced that exact same problem too and decided to come up with Emotivote to aid your team in making better decisions; Emotivote is an anonymous voting system based on sentiment analysis of speech and video over conference calls, allowing you to easily understand how your team might be feeling about various suggestions to help make better decisions.

Emotivote currently integrates with Cisco Webex and uses Natural Language Understanding to recognize topics/suggestions from meeting conversations and allows your team to keep track of all topics and suggestions being discussed. It manifests in the form of a chat bot your team can communicate with to obtain a real-time aggregated sentiment score on ideas and suggestions from all members in the conference call.

## How we built it
Emotivote has 3 core components: frontend client, backend server, and Cisco Webex chat bot. 

The frontend clients perform three functions: facial emotion analysis, conversational emotion analysis and keyword extraction from speech to identify 'topics' and 'suggestions'. 

Facial emotion analysis works as such: when a member makes a suggestion, users' webcam are activated through openCV and captures image frames while the members are discussing. Their faces are analysed for their depicted emotions using the Microsoft Face API. Based on this analysis, we generate a sentiment score and send it to the backend server using Google Cloud PubSub.

Conversational emotion detection uses Natural Language Processing technology to extract the sentiment from provided speech. Once a suggestion has been made, subsequent comments are analyzed using Google's Cloud Language API to provide a sentiment score towards the suggestion for each user. These scores are then sent to the backend via Google Cloud PubSub.

Keyword extraction from speech is done in two parts. A Speech-to-Text (Google Cloud Speech) client transcribes meeting conversations into text for analysis; speech is streamed to the API by polling with Voice Activation Detection technology (WebRTCVAD). This same transcribed text is used for conversational emotion detection. To extract 'topics' and 'suggestions', we used a Natural Language Understanding client (Dialogflow) to extract intents and entities from the text. Through careful design of these entities and intents, we can reliably determine the topics and suggestions being discussed and considered.

The backend, built in Node.js, acts as the central controller and dictates the flow of data throughout the system. It extensively uses Google Cloud PubSub to communicate with the other components and clients. To summarize the overall flow that the backend is responsible for: Upon extraction of 'topics' and 'suggestions' from speech, it triggers client machines to start capturing and analyzing video frames to determine how users are feeling. The backend then aggregates the results from every client and updates the Webex bot with the final sentiment score. 

Using the webexteamssdk API provided by Cisco, a webhook via Python flask enables us to constantly listen to messages published to our chat bot, Emote. The webhook allows Emote to send GET request to the Node.js server to query for the final voting results for individual suggestions. The chat bot server runs in a Docker container, also allowing the Node.js server to send a POST request to it, sending information about the 'topic' and 'suggestion' being discussed.

## Challenges we ran into

As seen, this project comprises of various units. Each of us started working on different units of the architecture and we had to eventually integrate all of them together; communication was vital so that data could flow between the different components seamlessly and enable the functionality of the system. We initially used HTTP requests as our main communication method, but realized that using a publish-subscribe model would be much more efficient and less prone to errors. We also faced some initial issues with setting up and customizing the Webex chat bot. There were also a lot of final bug fixes and tweaks to make so that everything runs smoothly.

## Accomplishments that we're proud of
- Creating something that we personally find useful.  We have all experienced insanely dragged out meetings to discuss project ideas but could never come to a firm decision. Emotivote can help us extract everyone's sentiments more effectively and conclude our meetings in shorter time period.
- Explore and integrate different technologies into an end-to-end product.
- Coming up with our own system architecture and making the system work smoothly

## What we learned
Each team member worked on a different component of Emotivote and learned different technologies along the way. These technologies include: Microsoft Face API, Docker, Google Cloud PubSub, and Django. We also managed to put our knowledge of software architecture and software integration to practice.

## What's next for Emotivote
Right now, Emotivote is based on Webex. It can be later be integrated with other digital meeting rooms such as Hangouts and Skype. It can also work hand-in-hand with a previous project of ours that extract actionable information and tasks from meetings conversations: Huddle.
