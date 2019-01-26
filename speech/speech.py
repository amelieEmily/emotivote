import time, logging
from datetime import datetime
import threading, collections, queue, os, os.path
from google.cloud import speech
from vad_audio import VADAudio
from df import DialogflowClient
import logmmse
import numpy as np
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
            audio = b''
            
if __name__ == '__main__':
    main()
