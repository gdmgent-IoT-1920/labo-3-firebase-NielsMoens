from sense_hat import SenseHat
import threading
import firebase_admin
from firebase_admin import credentials, firestore
import time

#const
COLLECTION = 'raspberryPi'
DOCUMENT = 'y4VFQEqTZTvBf6O0pIzV'

# firebase
cred = credentials.Certificate("/home/pi/code/week5/demoproject/pi/config/iotlabo3-firebase-adminsdk-o5w1i-405d897fbe.json")
firebase_admin.initialize_app(cred)

# connect to firestore
db = firestore.client()

# sensehat 
sense = SenseHat()
sense.set_imu_config(False, False, False)
sense.clear()

def get_set_value():
    # get value
    t = round(sense.get_temperature())
    p = round(sense.get_pressure())
    h = round(sense.get_humidity())

    # SET VALUES IN FB
    pi_ref.update(
        {'enviroment': 
            {
                't' : t,
                'p' : p,
                'h' : h
            }
        },
        )
    sense.show_message(str(t), text_colour=[255, 100, 100])
    sense.show_message(str(p), text_colour=[255, 100, 100])
    sense.show_message(str(h), text_colour=[255, 100, 100])
    print("tempature=", t, "pressure=", p, "humidity=", h)
    return [t, p, h]

# http://yaab-arduino.blogspot.com/2016/08/automatic-orientation-of-sense-hat-display.html 
def auto_rotate_display():
  # read sensors data to detect orientation
  x = round(sense.get_accelerometer_raw()['x'], 0)
  y = round(sense.get_accelerometer_raw()['y'], 0)

  rot = 0
  if x == -1:
    rot=90
  elif y == -1:
    rot=180
  elif x == 1:
    rot=270
  # rotate the display according to the orientation
  sense.set_rotation(rot)

# connect firestore
db = firestore.client()
pi_ref = db.collection(COLLECTION).document(DOCUMENT)

# app
while True:
    auto_rotate_display()
    get_set_value()
    time.sleep(1)
