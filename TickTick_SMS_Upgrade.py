import logging
from decouple import config
from ticktick.oauth2 import OAuth2        # OAuth2 Manager
from ticktick.api import TickTickClient   # Main Interface
import sms_platform
import datetime
import time
import pytz
from keep_alive import keep_alive

def time_in_range(start, current):
    """Returns whether current is in the range [start, end]"""
    return start == current

def main():
  logging.basicConfig(level=logging.INFO)
  
  
  auth_client = OAuth2(client_id=config('client_id'),
                       client_secret=config('client_secret'),
                       redirect_uri=config('redirect_uri'))
  
  logging.info("Client Authentication Acquired")
  
  
  client = TickTickClient(config('user'), config('password'), auth_client)
  
  logging.info("Client Connection Successfull")
  
  logging.info("Getting All Tasks")
  all_tasks = client.state['tasks']
  
  logging.info("Getting Current Formatted Time")
  formated_time = datetime.datetime.now().utcnow()
  
  formated_time = datetime.datetime.strftime(formated_time,"%Y%m%d-%H%M")
  formated_time = datetime.datetime.strptime(formated_time,"%Y%m%d-%H%M")
  print (formated_time)
  

  logging.info("Sending Messages: ")
  print ("\n")
  for task in all_tasks:
      
      title = task['title']
      try:
          due_date = task['dueDate']
          due_date = due_date[0:len(due_date)-12]
          due_date_convert = datetime.datetime.strptime(due_date, '%Y-%m-%dT%H:%M')
          print(due_date_convert)
        
      except KeyError:
          due_date_convert = None
          logging.error("Task: \"" + title + "\" does not have due date, skipping...")
  
      if due_date_convert is not None and time_in_range(due_date_convert,formated_time):
          logging.info ("Task: \"" + title + "\" past due date (" + str(due_date_convert) + ") - SENDING MESSAGE")
          phone_num = config("phone_number")
          message_formatted = "TTN - \""+title+"\" DUE"
  
          try:
              sms_platform.send_sms_via_email(
                  number=phone_num,
                  message=message_formatted,
                  subject=""
              )
              logging.info ("TTN - MESSAGE SENT")
          except Exception as e: 
              logging.error("Unable to Send Message")
              print(e)
          
      print("\n")

  


while True:
  main()
  keep_alive()
  time.sleep(50)
