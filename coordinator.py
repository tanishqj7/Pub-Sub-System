import redis
import json
import time

r = redis.Redis()

invitations_stream = "invitations"
guest_invites_stream = "guest_invites"
responses_stream = "responses"
summary_stream = "summary"

guest_names = ["Alice", "Bob", "Charlie"]
response_count = {}

def listen_for_invitations():
    print("Coordinator waiting for invitations...")
    last_id = '0'
    while True:
        entries = r.xread({invitations_stream: last_id}, block=0, count=1)
        if entries:
            _, messages = entries[0]
            for msg_id, msg in messages:
                last_id = msg_id
                data = json.loads(msg[b'data'].decode())
                print(f"Coordinator received invitation: {data}")
                for guest in guest_names:
                    r.xadd(guest_invites_stream, {'data': json.dumps({'invitation': data, 'guest': guest})})
                response_count[data['event_id']] = 0

def listen_for_responses():
    print("Coordinator waiting for responses...")
    last_id = '0'
    guest_summary = {}
    while True:
        entries = r.xread({responses_stream: last_id}, block=0, count=1)
        if entries:
            _, messages = entries[0]
            for msg_id, msg in messages:
                last_id = msg_id
                data = json.loads(msg[b'data'].decode())
                eid = data['event_id']
                guest_summary.setdefault(eid, []).append({data['guest']: data['response']})
                # guest_summary.setdefault(eid, []).append({data['guest']: data['response']})

                if eid not in response_count:
                    response_count[eid] = 0  # Ensure it's initialized
                response_count[eid] += 1

                if response_count[eid] == len(guest_names):
                    r.xadd(summary_stream, {'data': json.dumps({'event_id': eid, 'summary': guest_summary[eid]})})
                    print(f"Coordinator sent summary to host for event {eid}")

if __name__ == "__main__":
    from threading import Thread
    Thread(target=listen_for_invitations).start()
    Thread(target=listen_for_responses).start()
