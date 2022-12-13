import pika
import sys
import requests

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost', port='5672', credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

for i in range(0,7) :

    channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=str(i),
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ))
    print(" [x] Sent %r" % i)

connection.close()
