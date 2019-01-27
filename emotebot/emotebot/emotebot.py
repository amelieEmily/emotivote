#!/usr/bin/env python
#  -*- coding: utf-8 -*-

# 3rd party imports ------------------------------------------------------------
# Flask help can be found here:
# http://flask.pocoo.org/
from flask import Flask, request
from webexteamssdk import WebexTeamsAPI, Webhook
import urllib.request
import urllib.parse
import json
import re
import requests
# local imports ----------------------------------------------------------------
from helpers import (read_yaml_data,
                     get_ngrok_url,
                     find_webhook_by_name,
                     delete_webhook, create_webhook)

flask_app = Flask(__name__)
teams_api = None

peteRoomId = 'Y2lzY29zcGFyazovL3VzL1JPT00vMmEyZGIyNTAtYTFlYi0zMjYyLWFjY2UtYjgyYTk2OGQ1ZWM1'
spaceRoomId = 'Y2lzY29zcGFyazovL3VzL1JPT00vZjg0MmFkMDAtMjE2YS0xMWU5LWI1MzQtOTliYTM4NmI4NTU2'
# Create a python decorator which tells Flask to execute this method when the "/teamswebhook" uri is hit
# and the HTTP method is a "POST" request.
@flask_app.route('/teamswebhook', methods=['POST'])
def teamswebhook():

    # Only execute this section of code when a POST request is sent, as a POST indicates when a message
    # has been sent and therefore needs processing.
    if request.method == 'POST':
        json_data = request.get_json()
        print("\n")
        print("WEBHOOK POST RECEIVED:")
        print(json_data)
        print("\n")

        # Pass the JSON data so that it can get parsed by the Webhook class
        webhook_obj = Webhook(json_data)

        # Obtain information about the request data such as room, message, the person it came from
        # and person's email address.
        room = teams_api.rooms.get(webhook_obj.data.roomId)
        message = teams_api.messages.get(webhook_obj.data.id)
        person = teams_api.people.get(message.personId)
        email = person.emails[0]

        print("NEW MESSAGE IN ROOM '{}'".format(room.title))
        print("FROM '{}'".format(person.displayName))
        print("MESSAGE '{}'\n".format(message.text))

        # Message was sent by the bot, do not respond.
        # At the moment there is no way to filter this out, there will be in the future
        me = teams_api.people.me()
        if message.personId == me.id:
            return 'OK'
        else:
            teams_api.messages.create(spaceRoomId, text='Hello, ' + person.displayName + '.')
            if 'thoughts' in message.text or 'feeling' in message.text or 'think' in message.text:
                teams_api.messages.create(spaceRoomId, text='Checking votes..')
                contents = urllib.request.urlopen('http://server:3000/votes/')
                teams_api.messages.create(spaceRoomId, text='Here\'s how people feel about the suggestion:')
                data = json.loads(contents.read().decode())
                print(data)
                average = 0
                i = 0
                for score in data['votes']:
                    teams_api.messages.create(spaceRoomId, text='One person has a score of ' + ("%.2f" % round(float(score),2)) + '!')
                    average += float(score)
                    i += 1
                average /= i
                percentage = average + 10
                percentage *= 5
                teams_api.messages.create(spaceRoomId, text='The average score is ' + str("%.2f" % round(float(average),2)) + '!')
                teams_api.messages.create(spaceRoomId, text='The happiness percentage is ' + str("%.2f" % round(float(percentage),2)) + '%!')
            else:
                teams_api.messages.create(spaceRoomId, text='Say what?')
    else:
        print('received none post request, not handled!')

@flask_app.route('/topic', methods=['POST'])
def topic():
    if request.method == 'POST':
        data = request.json
        print("\n")
        print("TOPIC POST RECEIVED:")
        print(data)
        print("\n")
        teams_api.messages.create(spaceRoomId, text='The topic being discussed is ' + data['topic'] + '.')
    else:
        print('received none post request, not handled!')

@flask_app.route('/suggestion', methods=['POST'])
def suggestion():
    if request.method == 'POST':
        data = request.json
        print("\n")
        print("SUGGESTION POST RECEIVED:")
        print(data)
        print("\n")
        teams_api.messages.create(spaceRoomId, text='The suggestion is ' + data['suggestion'] + '.')
    else:
        print('received none post request, not handled!')


if __name__ == '__main__':

    # Read the configuration that contains the bot access token
    config = read_yaml_data('/opt/config/config.yaml')['emotebot']
    teams_api = WebexTeamsAPI(access_token=config['teams_access_token'])

    # Get some required NGrok information
    ngrok_url = get_ngrok_url()

    # Define the name of webhook
    webhook_name = 'emotebot-wb-hook'

    # Find any existing webhooks with this name and if this already exists then delete it
    dev_webhook = find_webhook_by_name(teams_api, webhook_name)
    if dev_webhook:
        delete_webhook(teams_api, dev_webhook)

    # Create a new teams webhook with the name defined above
    create_webhook(teams_api, webhook_name, ngrok_url + '/teamswebhook')

    # Host flask web server on port 5000
    flask_app.run(host='0.0.0.0', port=5000)
