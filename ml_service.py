import json
import time

import redis

import settings


# TODO
db = redis.StrictRedis(host=settings.REDIS_IP,
                       port=settings.REDIS_PORT,
                       db=settings.REDIS_DB_ID)


def classify_process():
    # TODO
    while True:
        # TODO
        queue = db.lrange(settings.REDIS_QUEUE,
                          settings.REDIS_DB_ID,
                          1)
        print(queue)

        # TODO
        for q in queue:
            # TODO
            q = json.loads(q.decode("utf-8"))

            print(q)

            # TODO
            imageID = q["id"]

            # RUN ML MODEL...
            output = 'Resuelto: {}'.format(q['text'])

            # TODO
            db.set(imageID, json.dumps(output))

            # TODO
            db.ltrim(settings.REDIS_QUEUE, 1, -1)

        # sleep for a small amount
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    classify_process()
