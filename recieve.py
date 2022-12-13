import pika
import time
import pandas
import requests


data = pandas.read_excel("scanrio.xlsx")

datadic = data.to_dict(orient='records')


credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost', port='5672', credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):

    print(" [x] Received %r" % body.decode())
    
    endpoint = "http://localhost:8000/qostest/mysite/"

    get_responce = requests.post(
        url=endpoint, json=datadic[int(body.decode())])

    print(get_responce.status_code, get_responce.json())

    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
