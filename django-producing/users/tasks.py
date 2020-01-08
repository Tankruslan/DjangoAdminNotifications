import secrets
import json
import sys
from loguru import logger
from celery import shared_task
from .models import CustomUser

logger.add(sys.stderr, format="{time} {level} {message}", level="DEBUG")

""" Saves user's token to cache """
# from django.core.cache import cache


# @shared_task
# def generate_and_save_token(username):
#     token = secrets.token_urlsafe()
#     cache.set(username, token)
#     return None


""" Publishes data in redis """
# import redis
#
#
# @shared_task
# def generate_and_send_token(username):
#     user = CustomUser.objects.get(user__username=username)
#     user_id = user.id
#     auth_user_id = user.user.id
#     token = secrets.token_urlsafe()
#     # use 'localhost' if you are out of docker, or 'redis' if you are in docker
#     r = redis.StrictRedis(host='redis', port=6379)
#     data = [auth_user_id, user_id, token]
#     r.publish('user_tokens_get', json.dumps(data))
#     logger.debug('Sent %r' % json.dumps(data))


""" Publishes data in RabbitMQ """
import pika


@shared_task
def generate_and_send_token(username):
    user = CustomUser.objects.get(user__username=username)
    user_id = user.id
    auth_user_id = user.user.id
    # connecting to a broker
    connection = pika.BlockingConnection(
        # use 'localhost' if you are out of docker, or 'rabbitmq' if you are in docker
        pika.ConnectionParameters(host='rabbitmq')
    )
    channel = connection.channel()

    # creating a queue
    channel.queue_declare(queue='user_token_queue', durable=True)

    token = secrets.token_urlsafe()
    data = [auth_user_id, user_id, token]

    # send task to a queue
    channel.basic_publish(
        exchange='',
        routing_key='user_token_queue',
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )
    logger.debug('Sent %r' % json.dumps(data))
    connection.close()
