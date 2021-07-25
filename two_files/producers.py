import pika
import json


def prod():

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange='exchange_one',
                             exchange_type='direct',
                             durable=True,
                             auto_delete=False)

    channel.exchange_declare(exchange='exchange_two',
                             exchange_type='direct',
                             durable=True,
                             auto_delete=False)

    channel.queue_declare(queue='messages', durable=True)
    channel.queue_bind(queue='messages', exchange='exchange_one', routing_key='A.B.C.D.12')

    channel.queue_declare(queue='change_messages', durable=True)
    channel.queue_bind(queue='change_messages', exchange='exchange_two', routing_key='E.F.12')

    message = json.dumps({'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E',
                          'f': 'F', 'num': 12, 'data': 'some_usefull_data'})

    channel.basic_publish(exchange='exchange_one',
                          routing_key="A.B.C.D.12",
                          body=message,
                          properties=pika.BasicProperties(delivery_mode=2,))

    channel.basic_publish(exchange='exchange_two',
                          routing_key="E.F.12",
                          body=message,
                          properties=pika.BasicProperties(delivery_mode=2,))

    connection.close()


if __name__ == '__main__':
    prod()

