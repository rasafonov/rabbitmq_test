import pika
import json


def cons():

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
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

    def callback(ch, method, properties, body):

        body = body.decode()
        data = json.loads(body)
        channel.basic_publish(exchange='exchange_two',
                              routing_key='{}.{}.{}'.format(data['e'], data['f'], data['num']),
                              body=body)

    channel.basic_consume(queue='messages', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    cons()
