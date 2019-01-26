import time, logging
from datetime import datetime
import threading, collections, queue, os, os.path
from google.cloud import speech
from vad_audio import VADAudio
from df import DialogflowClient
import requests

def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'en-US'  # a BCP-47 language ta
    df_client = DialogflowClient()
    url = "http://localhost:3000"

    client = speech.SpeechClient()
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code)
    streaming_config = speech.types.StreamingRecognitionConfig(
        config=config,
        single_utterance=True)

    # Start audio with VAD
    vad_audio = VADAudio(aggressiveness=3)
    print("Listening (ctrl-C to exit)...")
    frames = vad_audio.vad_collector()

    # Stream from microphone to CloudSpeech using VAD
    stream = []
    
    for frame in frames:
        if frame is not None:
            stream.append(speech.types.StreamingRecognizeRequest(audio_content=frame))
        else:
            responses = client.streaming_recognize(streaming_config, stream)
            for response in responses:
                for result in response.results:
                    alternatives = result.alternatives
                    for alternative in alternatives:
                        transcript = alternative.transcript
                        print("Transcript: " + transcript)
                        intent, entities = df_client.detect_intent(transcript)
                        print("Intent: " + intent)
                        if "topic" in entities:
                            print("Topic: " + entities["topic"])
                            try:
                                endpoint = url + "/topic"
                                query = dict()
                                query["topic"] = entities["topic"]
                                response = requests.request("POST", endpoint, json=query)
                            except requests.exceptions.RequestException as e:
                                logging.error(e)
                        if "ideas" in entities:
                            print("Ideas: " + entities["ideas"])
                            try:
                                endpoint = url + "/suggestions"
                                query = dict()
                                query["suggestion"] = entities["ideas"]
                                response = requests.request("POST", endpoint, json=query)
                            except requests.exceptions.RequestException as e:
                                logging.error(e)
            stream = []
            
if __name__ == '__main__':
    main()
