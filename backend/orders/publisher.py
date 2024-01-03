import logging
import pika
import json
from django.conf import settings

logger = logging.getLogger('django')

url = settings.AMQP_URL
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params)  # Connect to Broker
channel = connection.channel()  # start a channel
channel.queue_declare(queue='create_invoice')  # Declare a queue


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='create_invoice',
                          body=json.dumps(body), properties=properties)
