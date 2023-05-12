import os
import pika
import worker
from dotenv import load_dotenv
import json

# .env 로드
load_dotenv("../.env")
ip = os.environ.get("ip")
port = os.environ.get("port")
vhost = os.environ.get("vhost")
id = os.environ.get("id")
pw = os.environ.get("pw")
queue = os.environ.get("queue")


class Consumer:
    def __init__(self, _ip, _port, _vhost, _id, _pw, _queue):
        self.ip = _ip
        self.port = _port
        self.vhost = _vhost
        self.cred = pika.PlainCredentials(_id, _pw)
        self.queue = _queue
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.ip, self.port, self.vhost, self.cred)
        )

        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=Consumer.callback
        )

    def callback(channel, method_frame, header_frame, body):
        print(f"Received Message...", end=" ")

        # binary message를 utf-8로 decoding
        message = body.decode("utf-8", errors="ignore")
        # 디코딩한 message를 json으로 load
        message_json = json.loads(message)
        # print(type(message))
        # worker 호출
        worker.worker(message_json)

        # worker 작업이 끝난 후에 브로커로 ACK 전달
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

        print("Done")

    def run(self):
        print("Consumer is starting...")

        # 컨슈머 실행
        self.channel.start_consuming()


# 컨슈머 객체 생성 및 실행
consumer = Consumer(ip, port, vhost, id, pw, queue)
consumer.run()
