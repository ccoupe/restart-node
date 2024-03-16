import paho.mqtt.client as mqtt
import json
import time
import json
import argparse
import warnings
import sys
import subprocess
from lib.Settings import Settings
import random


def on_connect(client, userdata, flags, rc):
    print("Mqtt: "+mqtt.connack_string(rc))

def on_subscribe(client, userdata, mid, granted_qos):
  print("on subscribe:")
  
def on_disconnect(client, userdata, rc):
    if rc != 0:
      while True:
        tm = random.randint(30,90)
        print(f"mqtt disconnect: {rc}, attempting reconnect in {tm} seconds")
        time.sleep(tm)
        try:
          client.reconnect()
          # if success, break out of the loop
          break
        except OSError as e:
          continue

def on_message(client, userdata, message):
    global settings
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    topic = message.topic
    dt = json.loads(str(message.payload.decode("utf-8")))
     
    if topic == settings.sub_topic:
      if dt['cmd'] == 'reboot':
        #print("is",settings.host_name,"in the list", dt['nodes'])
        nodes = dt['nodes']
        if settings.host_name in nodes:
          print("Rebooting", settings.host_name)
          client.publish(settings.pub_topic, json.dumps(settings.pub_rb_payload))
          client.loop()
          time.sleep(1)
          # give time so publish can run.
          # no return from the following
          subprocess.call(settings.reboot)
          #subprocess.call('/usr/sbin/reboot')
          
def initialise_mqtt_clients(cname):
    client= mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, cname, False)      #don't use clean session
    client.on_connect = on_connect        #attach function to callback
    client.on_message = on_message        #attach function to callback
    client.on_disconnect = on_disconnect  
    client.run_flag=False
    client.running_loop=False
    #client.subscribe_flag=False
    #client.on_subscribe = on_subscribe
    client.bad_connection_flag=False
    client.connected_flag=False
    client.disconnect_flag=False
    return client

def main(argList=None):
  global subscribe_list, settings, client
  ap = argparse.ArgumentParser()
  ap.add_argument("-c", "--conf", required=True, type=str,
    help="path and name of the json configuration file")
  
  args = vars(ap.parse_args())  
  settings = Settings(args['conf'])
  #settings.display()
  # At startup (via systemd i.e. boot) we publish a message. I'm alive
  # It is required we run as root (wheel for some)
  client = initialise_mqtt_clients(settings.mqtt_client_name)
  client.connect(settings.mqtt_server, settings.mqtt_port)
  
  # we subscribe to the control topic, publish and wait for messages
  sub = settings.sub_topic
  r = client.subscribe(sub, 1)
  print(f"Subscribed to {sub}")
  client.publish(settings.pub_topic,json.dumps(settings.pub_st_payload))
  while True:
    client.loop()
    #time.sleep(5 * 60)
    
if __name__ == '__main__':
  sys.exit(main())

   
