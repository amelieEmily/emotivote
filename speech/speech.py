import time, logging
from datetime import datetime
import threading, collections, queue, os, os.path
from google.cloud import speech, pubsub
from vad_audio import VADAudio
from df import DialogflowClient
from sentiment import LanguageClient
import logmmse
import numpy as np
import requests

def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'en-US'  # a BCP-47 language ta
    df_client = DialogflowClient()
    lang_client = LanguageClient()
    url = "http://localhost:3000"

    client = speech.SpeechClient()
    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path("huddle72", "topics")
    suggest_path = publisher.topic_path("huddle72", "suggestions")
    vote_path = publisher.topic_path("huddle72", "vote")
    intent_life = 0
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code)

    # Start audio with VAD
    vad_audio = VADAudio(aggressiveness=3)
    print("Listening (ctrl-C to exit)...")
    frames = vad_audio.vad_collector()

    audio = b''
    
    for frame in frames:
        if frame is not None:
            audio += frame
        else:
            # Execute noise reduction and speech enhancement for better recognition
            numpydata = np.fromstring(audio, dtype=np.int16)
            denoised_audio = logmmse.logmmse(numpydata, 16000, initial_noise=3)
            audio = speech.types.RecognitionAudio(content=denoised_audio.tobytes())
            response = client.recognize(config, audio)
            for result in response.results:
                # The first alternative is the most likely one for this portion.
                transcript = result.alternatives[0].transcript
                print("Transcript: " + transcript)
                intent, entities = df_client.detect_intent(transcript)
                if intent == "Default Fallback Intent" and intent_life > 0:
                    intent_life -= 1
                    sentiment = str(lang_client.client.analyze_sentiment(document=lang_client.request(transcript)).document_sentiment.score)
                    print("Sentiment: " + str(sentiment))
                    publisher.publish(vote_path, sentiment.encode('utf-8'))
                else:
                    print("Intent: " + intent)
                    if "topic" in entities and len(entities["topic"]):
                        intent_life = 0
                        print("Topic: " + entities["topic"])
                        publisher.publish(topic_path, entities["topic"].encode('utf-8'))
                    if "ideas" in entities and len(entities["ideas"]):
                        intent_life = 3
                        print("Ideas: " + entities["ideas"])
                        publisher.publish(suggest_path, entities["ideas"].encode('utf-8'))

            audio = b''
            
if __name__ == '__main__':
    main()
