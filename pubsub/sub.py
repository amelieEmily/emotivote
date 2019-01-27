from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("huddle72", "suggestions")

topic = publisher.create_topic(topic_path)

print('Topic created: {}'.format(topic))