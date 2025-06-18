import redis
import json
import time
import uuid

r = redis.Redis()

def send_invitation():
    event_id = str(uuid.uuid4())[:8]
    event_name = "AI Workshop"
    print(f"Host sending invitation for event '{event_name}' with ID {event_id}")
    r.xadd("invitations", {'data': json.dumps({'event_id': event_id, 'event_name': event_name})})
    return event_id

def wait_for_summary(event_id):
    last_id = '0'
    print("Host waiting for summary...")
    while True:
        entries = r.xread({'summary': last_id}, block=0, count=1)
        if entries:
            _, messages = entries[0]
            for msg_id, msg in messages:
                last_id = msg_id
                data = json.loads(msg[b'data'].decode())
                if data['event_id'] == event_id:
                    print(f"Final Guest Summary for Event '{event_id}':")
                    for entry in data['summary']:
                        for name, resp in entry.items():
                            print(f"  {name}: {resp}")
                    return

if __name__ == "__main__":
    eid = send_invitation()
    wait_for_summary(eid)
