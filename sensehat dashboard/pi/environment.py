from sense_hat import SenseHat
import threading
import firebase_admin
from firebase_admin import credentials, firestore
import time


# firebase
cred = credentials.Certificate("/home/pi/code/week5/demoproject/pi/config/iotlabo3-firebase-adminsdk-o5w1i-405d897fbe.json")
firebase_admin.initialize_app(cred)

# connect to firestore
db = firestore.client()

# sensehat 
sense = SenseHat()
sense.set_imu_config(False, False, False)
sense.clear()

while True:
    data = {
        u'temp': sense.get_temperature(),
        u'hum': sense.get_humidity(),
    }
    db.collection(u'raspberryPi').document(u'y4VFQEqTZTvBf6O0pIzV').set(data)
    time.sleep(60)
print(data)