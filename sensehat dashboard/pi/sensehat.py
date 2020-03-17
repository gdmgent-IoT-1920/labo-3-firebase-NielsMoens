from sense_hat import SenseHat
import firebase_admin
from firebase_admin import credentials, firestore

#const
COLLECTION = 'raspberryPi'
DOCUMENT = 'y4VFQEqTZTvBf6O0pIzV'

# firebase
cred = credentials.Certificate("./config/iotlabo3-firebase-adminsdk-o5w1i-405d897fbe.json")
firebase_admin.initialize_app(cred)

# sensehat 
sense = SenseHat()
sense.set_imu_config(False, False, False)
sense.clear()

def update_sensehat(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        doc_readable = doc.to_dict()

        h = doc_readable['matrix']['color']['value']
        firebaseStatus = doc_readable['matrix']['isOn']

        rgb = tuple(int(h[i:i+2], 16) for i in (0,2,4))
        
        if firebaseStatus == True :
            sense.clear(rgb)
        else :
            sense.clear()
# connect firestore
db = firestore.client()
pi_ref = db.collection(COLLECTION).document(DOCUMENT)
pi_watch = pi_ref.on_snapshot(update_sensehat)

# app
while True:
    pass
