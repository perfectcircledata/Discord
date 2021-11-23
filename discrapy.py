import json
import requests
from datetime import datetime
from dateutil import parser
import creds
import pytz

# https://discord.com/developers/docs/topics/rate-limits
# https://discord.com/developers/docs/resources/channel#get-channel-messages

DAUTH = creds.login['DAUTH']
CHANNEL_ID = creds.login['CHANNEL_ID']
LIMIT = 100

def get_messages(channel_id, dauth, limit=100, before=None):
    headers = {}
    headers['authorization'] = dauth
    headers['limit'] = str(limit)

    if before:
        headers['before'] = before.isoformat()
 
    r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers)
 
    # I 'think' you can call the request object's json method to convert a json payload
    # to a python dict - BUT - if I'm wrong you can use the json.loads method just fine.
    # return json.loads(r.text)
    return r.json()

def loop(before=pytz.utc.localize(datetime.now())):
    # get initial query, call defaults to most recent messages (per Guy)
    results = get_messages(CHANNEL_ID, DAUTH, limit=LIMIT, before=before)
 
    # loop through messages
    for message in results:
        print(json.dumps(message))
        
        # as we loop, we'll also look for the earliest timestamp and store as 'before'
        timestamp = parser.parse(message['timestamp'])
        # print(timestamp, before)
        if timestamp < before: 
            before = timestamp
 
    # basically we'll keep invoking the loop until we get a payload with no messages
    if len(results):
        loop(before=before) # <- this is the recursion
 
    return

loop()
