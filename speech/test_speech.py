import time, logging
from datetime import datetime
import threading, collections, queue, os, os.path
from halo import Halo
from google.cloud import speech
from vad_audio import VADAudio
from df import DialogflowClient

def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'en-US'  # a BCP-47 language ta
    df_client = DialogflowClient()

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
    spinner = Halo(spinner='line')
    requests = []
    
    for frame in frames:
        if frame is not None:
            spinner.start()
            requests.append(speech.types.StreamingRecognizeRequest(audio_content=frame))
        else:
            spinner.stop()
            responses = client.streaming_recognize(streaming_config, requests)
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
                        if "ideas" in entities:
                            print("Ideas: " + entities["ideas"])
            requests = []
            
if __name__ == '__main__':
    main()
