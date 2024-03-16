import paho.mqtt.client as mqtt
import json
import time
import json
import argparse
import warnings
import sys
import subprocess
from lib.Settings import Settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import socket

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: "+mqtt.connack_string(rc))

def initialise_mqtt_clients(cname):
    client= mqtt.Client(cname,False) #don't use clean session
    client.on_connect= on_connect        #attach function to callback
    #client.on_message=on_message        #attach function to callback
    client.topic_ack=[]
    client.run_flag=False
    client.running_loop=False
    client.subscribe_flag=False
    client.bad_connection_flag=False
    client.connected_flag=False
    client.disconnect_flag=False
    return client
    
    
def send_email(addr, subj, errlns):
  global settings
  with open('missing.txt', 'w') as f:
    for line in errlns:
      f.write("%s\n" % line)
  # https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/
  # instance of MIMEMultipart
  msg = MIMEMultipart()
  # storing the senders email address  
  msg['From'] = addr
    
  # storing the receivers email address 
  msg['To'] = addr
    
  # storing the subject 
  msg['Subject'] = subj
    
  # string to store the body of the mail
  body = '\n'.join(errlns)
  
  # attach the body with the msg instance
  msg.attach(MIMEText(body, 'plain'))
  
  # creates SMTP session
  s = smtplib.SMTP(settings.smtp_svr, settings.smtp_port)
  
  # talk to server
  s.ehlo()
  
  # Authentication - none
  # Converts the Multipart msg into a string
  text = msg.as_string()
    
  # sending the mail
  s.sendmail(addr, addr, text)
    
  # terminating the session
  s.quit()
  
# from https://stackoverflow.com/questions/2953462/pinging-servers-in-python
def ping_server(server: str, port: int, timeout=3):
    """ping server"""
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, port))
    except OSError as error:
        return False
    else:
        s.close()
        return True

def ping(host):
    """
    Returns True if host responds to a ping request
      false if it doesn't (timeout most likely)
    """
    import subprocess, platform

    # Ping parameters as function of OS
    ping_str = "-n 1 -q" if  platform.system().lower()=="windows" else "-c 1"
    args = "ping " + " " + ping_str + " " + host
    need_sh = False if  platform.system().lower()=="windows" else True

    # Ping
    return subprocess.call(args, shell=need_sh) == 0

def main(argList=None):
  global subscribe_list, settings, client
  ap = argparse.ArgumentParser()
  loglevels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
  ap.add_argument("-c", "--conf", required=True, type=str,
    help="path and name of the json configuration file")
  #ap.add_argument("-s", "--syslog", action = 'store_true',
  #  default=False, help="use syslog")
  
  args = vars(ap.parse_args())  
  settings = Settings(args['conf'])
  #settings.display()
  client = initialise_mqtt_clients(settings.mqtt_client_name)
  client.connect(settings.mqtt_server, settings.mqtt_port)
  
  # subscribe 
  client.subscribe(
  
  if ping("192.168.1.99"):
    print("OK")
  else:
    print("Fail")
    
    
if __name__ == '__main__':
  sys.exit(main())

   
