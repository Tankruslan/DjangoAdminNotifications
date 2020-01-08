import sys
import json
import psycopg2
import redis  # use this instead of pika
import pika  # use this instead of redis
from loguru import logger

logger.add(sys.stderr, format="{time} {level} {message}", level="DEBUG")

""" Getting data from Redis """


# def get_data_from_redis():
#     # use 'localhost' if you are out of docker, or 'redis' if you are in docker
#     r = redis.StrictRedis(host='redis', port=6379)
#     p = r.pubsub()
#     p.subscribe('user_tokens_get')
#     for message in p.listen():
#         if not isinstance(message['data'], int):
#             unpack_data = json.loads(message['data'])
#             user_id = unpack_data[0]
#             token_val = unpack_data[1]
#             _SQL = "UPDATE users_profile SET token = '{0}' WHERE user_id = {1}"
#             """
#             DATABASE SETTINGS:
#             localhost: user: 'postgres', password: 'ruslan',
#                   database: 'my_postgres_db', host: 'localhost'
#             docker: user: 'docker-postgres', password: 'docker-postgres-psw',
#                   database: 'docker-postgres-db', host: 'postgres'
#             """
#             conn = psycopg2.connect(user='docker-postgres',
#                                     password='docker-postgres-psw',
#                                     host='postgres',
#                                     port='5432',
#                                     database='docker-postgres-db',)
#             cur = conn.cursor()
#             cur.execute(_SQL.format(token_val, user_id))
#             conn.commit()
#             conn.close()
#             logger.debug('Received and saved to db %r' % unpack_data)


""" Getting data from RabbitMQ """


connection = pika.BlockingConnection(
    # use 'localhost' if you are out of docker, or 'rabbitmq' if you are in docker
    pika.ConnectionParameters(host='rabbitmq')
)
channel = connection.channel()

channel.queue_declare(queue='user_token_queue', durable=True)


def take_and_save_token(ch, method, properties, body):
    unpack_data = json.loads(body)
    auth_user_id = unpack_data[0]
    user_id = unpack_data[1]
    token_val = unpack_data[2]
    _SQL = ("UPDATE users_profile SET token = '{0}' WHERE user_id = {1}; "
            "UPDATE auth_user SET is_active = True WHERE id = {2}")
    """
    DATABASE SETTINGS:
        localhost: user: 'postgres', password: 'ruslan', 
              database: 'my_postgres_db', host: 'localhost'
        docker: user: 'docker-postgres', password: 'docker-postgres-psw', 
              database: 'docker-postgres-db', host: 'postgres'
    """
    conn = psycopg2.connect(user='docker-postgres',
                            password='docker-postgres-psw',
                            host='postgres',
                            port='5432',
                            database='docker-postgres-db',
                            )
    cur = conn.cursor()
    cur.execute(_SQL.format(token_val, user_id, auth_user_id))
    conn.commit()
    conn.close()
    ch.basic_ack(delivery_tag=method.delivery_tag)
    logger.debug('Received and saved to db %r' % unpack_data)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='user_token_queue',
                      on_message_callback=take_and_save_token)


if __name__ == "__main__":
    channel.start_consuming()  # use this instead of redis
    # get_data_from_redis()  # use this instead of rabbit
