import sys
import random
import json
import logging
import datetime
import base64
import io
from PIL import Image
from flask import Flask, request, jsonify
from modules.cloudevent import CloudEventService
from modules.mqtt import MQTTClient
from modules.detect import ObjectDetection

print(sys.argv)
if(len(sys.argv) < 2):
    print('Missing argument: please inform the broker address, port and topic')
    exit()

#broker_address = "mosquitto"
broker_address = str(sys.argv[1])
broker_port = int(sys.argv[2])
topic = str(sys.argv[3])

source = "edge-service"
message_type = "edge-service-message"
data = { "edge-service": "edge-service-data" }
client_id = f'python-mqtt-{random.randint(0, 1000)}'

#broker_address = "192.168.1.195"
#broker_port = 1883
#topic = "mytopic-response"

app = Flask(__name__)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

object_detection = ObjectDetection()

# Route to test image detection
@app.route("/detect", methods=["POST"])
def detect():
    image_file = request.files['image']
    image = Image.open(image_file)

    result = object_detection.detect(image)

    return jsonify(result)


@app.route("/", methods=["POST"])
def home():

    cloud_event = CloudEventService()
    event = cloud_event.receive_message(request)

    mqtt_client.publish(json.dumps(event.data))
    
    # Process event

    # app.logger.info(
    #    f"Found {event['id']} from {event['source']} with type "
    #    f"{event['type']} and specversion {event['specversion']}"
    #)

    now = datetime.datetime.now()
    sent_datetime = datetime.datetime.strptime(event.data['timestamp'], "%Y-%m-%dT%H:%M:%S.%f")
    latency = str(now - sent_datetime)

    app.logger.info(
        f"Event Priority: {event.data['priority']} | "
        # f"Data Content: {event.data['message']} bytes | "
        f"Data Length: {len(event.data['image'])} bytes | "
        # f"Sent time: {sent_datetime} -"
        # f"Now: {now} -"
        f"Latency: {latency}"
    )

    #base64_message = event.data['image']
    #base64_bytes = base64_message.encode('ascii')
    #image_bytes = base64.b64decode(base64_bytes)
    #image = Image.open(io.BytesIO(image_bytes))

    # Detect
    #object_detection.detect(image)

    # Return 204 - No-content
    return "", 204

if __name__ == "__main__":
    mqtt_client = MQTTClient(client_id=client_id, broker=broker_address, port=broker_port, topic=topic)
    mqtt_client.connect_mqtt()
    app.logger.info("Starting up server...")
    app.run(host='0.0.0.0', port=8080)