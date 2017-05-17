import redis
import json
import argparse
import time
import random

r = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="worker process for parsing pdfs")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("-r", "--redis_host", default="redis", type=str)
    parser.add_argument("-k", "--redis_port", default=6379, type=int)
    args = parser.parse_args()

    r = redis.StrictRedis(args.redis_host,args.redis_port)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe('pdfs')
    #for item in pubsub.listen():
    while True:
        message = p.get_message()
        if message:
            print(message)
            try:
                message['data'] = message['data'].decode('utf-8')
                data = json.loads(str(message['data']))
                result_data = {'id': data['id'], 'status':'processing'}
                r.set(data['id'], json.dumps(result_data).encode('utf-8'))
                print("Working on document %s..." % data['id'])
                time.sleep(random.randint(0,3))
                print("Example text recovered from document %s!" % data['id'])
                result_data = {'id': data['id'], 'status':'completed', 'text': data['id']}
                r.setex(data['id'], 3600, json.dumps(result_data).encode('utf-8'))
            except Exception as e:
                print("Bad data %s, %s"%(message,e))
        time.sleep(0.01)