import redis
import json
import random
import time
import os

GUEST_NAME = os.getenv("GUEST_NAME", "Alice")
r = redis.Redis()

def respond(invite):
    event_id = invite['event_id']
    decision = random.choice(["Yes", "No", "Maybe"])
    print(f"{GUEST_NAME} received invite for event {event_id}, replying: {decision}")
    r.xadd("responses", {'data': json.dumps({
        'event_id': event_id,
        'guest': GUEST_NAME,
        'response': decision
    })})

def listen():
    last_id = '0'
    print(f"{GUEST_NAME} waiting for invitations...")
    while True:
        entries = r.xread({'guest_invites': last_id}, block=0, count=1)
        if entries:
            _, messages = entries[0]
            for msg_id, msg in messages:
                last_id = msg_id
                data = json.loads(msg[b'data'].decode())
                if data['guest'] == GUEST_NAME:
                    respond(data['invitation'])

if __name__ == "__main__":
    listen()
