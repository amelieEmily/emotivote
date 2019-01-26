FROM ubuntu

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y \
    python3 \
    python3-pip \
    alsa-base \
    alsa-utils \
    portaudio19-dev

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS /usr/src/app/credentials.json

CMD ["python3", "speech.py"]
