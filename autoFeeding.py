from gpiozero import DistanceSensor, Servo
from time import sleep
from signal import pause
import smtplib


sensor = DistanceSensor(echo=17, trigger=4, max_distance=2.0, threshold_distance=0.2)
servo = Servo(21)

total_seconds = 0
servo.max()

sender = "autofeedingEmail"
receiver = "receiverEmail"
app_password = "autofeeding app password"

subject = "AutoFeeding"
body = "Hello! Your pet has been fed :3."

message = f"Subject: {subject}\n\n{body}"

def open_door():
    print("Opening door")
    servo.mid()
    sleep(1)

def close_door():
    print("Closing door")
    servo.max()

    sleep(1)

def timer_event():
    total_seconds = 1 * 1 * 10
    while total_seconds:
        hrs = total_seconds // 3600
        mins = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        print(f"? Time left: {hrs:02d}:{mins:02d}:{secs:02d}", end='\r')
        sleep(1)
        total_seconds -= 1

    print("\n? Timer finished!")
    
def send_message():
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, app_password)
    server.sendmail(sender, receiver, message)
    print("Message sent to your email")
    server.quit()
    
def door_logic():
    print("Object detected!")
    send_message()
    open_door()
    sleep(1)
    close_door()
    timer_event()
    

sensor.when_in_range = door_logic

print("Monitoring distance... Press Ctrl+C to exit.")

try:
    while True:
        print(f"Distance: {sensor.distance * 100:.1f} cm ", end="\r")
        sleep(0.1)
        
except KeyboardInterrupt:
    print("Exiting")
