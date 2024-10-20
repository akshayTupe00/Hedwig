import pika
import requests
import uuid

class ExchangeReceiver(object):
    def __init__(self, username, password, host, port, exchange, exchange_type, service, service_name):
        self.service_worker = service
        self.service_name = service_name
        self.exchange = exchange

        credentials = pika.PlainCredentials(username, password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,
                                                                       port=port,
                                                                       credentials=credentials))

        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange, exchange_type=exchange_type)

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=self.exchange, queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=self.on_request, auto_ack=True)

        print("Awaiting requests from [x] " + self.exchange + " [x]")
        channel.start_consuming()

    def on_request(self, ch, method, props, body):
        service_instance = self.service_worker()

        response, task_type = service_instance.call(body)

        print('Processed request:', task_type)

class ExchangeProducer(object):
    def __init__(self, username, password, host, port, service_name):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.service_name = service_name

    def call(self, exchange, exchange_type, payload):
        credentials = pika.PlainCredentials(self.username, self.password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host,
                                                                       port=self.port,
                                                                       credentials=credentials))
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)

        corr_id = str(uuid.uuid4())

        channel.basic_publish(exchange=exchange, routing_key='', body=payload)
        connection.close()


def send_message_to_exchange():
    username = "guest"
    password = "guest"
    host = "localhost"
    port = 5672
    exchange = "scraper_exchange"
    exchange_type = "direct"

    # Initialize the producer
    producer = ExchangeProducer(
        username, password, host, port, "ExampleService"
    )

    # Send a message to the exchange
    producer.call(exchange, exchange_type, payload)

    print(f"Message sent to {exchange}")
