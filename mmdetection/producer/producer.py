import argparse
import os
import pika
from dotenv import load_dotenv

import json

# .env 로드
load_dotenv("../.env")
ip = os.environ.get("ip")
port = os.environ.get("port")
vhost = os.environ.get("vhost")
id = os.environ.get("id")
pw = os.environ.get("pw")
exchange = os.environ.get("exchange")
routing_key = os.environ.get("routing_key")
queue = os.environ.get("queue")


# 브로커로 메세지 전송하는 함수
def push(message1, message2, priority=0):
    # RabbitMQ 브로커 연결
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(ip, port, vhost, pika.PlainCredentials(id, pw))
    )

    # 채널 및 큐 생성
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True, arguments={"x-max-priority": 1})

    # 메세지 묶어 보내기
    messages = {"message1": message1, "message2": message2}
    body = json.dumps(messages)

    # 큐로 메시지 전송 (utf-8 encoding)
    channel.basic_publish(
        exchange=exchange,
        routing_key=routing_key,
        body=body.encode("utf-8"),
        properties=pika.BasicProperties(priority=priority),
    )

    print(f"[x] Sent Success")

    # 연결 종료
    connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", type=str, required=True)
    parser.add_argument("--mmcfg", "-m", type=str, required=True)
    parser.add_argument("--priority", "-p", type=int, default=0, required=False)
    args = parser.parse_args()

    # 전송할 파일 로드
    with open(args.config, "r") as f:
        config = f.read()
    # 전송할 mmdetection config 파일 로드
    with open(args.mmcfg, "r") as f:
        mmcfg = f.read()

    # RabbitMQ 브로커로 전송
    push(config, mmcfg, args.priority)
