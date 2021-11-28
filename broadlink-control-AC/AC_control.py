import broadlink
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


TURN_OFF= "2600bc01703a0d100c2d0c100d100c100d100c110c100d100d0f0d100d100c100d2c0d100c100e0f0c110c100d100c100e2b0d2c0d2c0d100c100d2c0d100c110c100d100c100e0f0c100d100d100c100d100c100d100d100c100d100c110c100d100c100d100c110c100d100c100d100d100c100d100c100d2c0d2c0d100c100d100d100c100d000147703b0c100d2c0d100c110c100d100c100d100c110d0f0d100c100d100c2d0c100d100d100c100d100c110c100d2c0d2c0d2c0c110c100d2c0d100c100d100c100d100d100c100d100c100d100d100c100d100c100d100c110c2d0c100d2c0d100c100d100c100d2c0d2c0d100c2d0d100c100d100c100d100c110c100d100c100d2c0e2b0d2c0d2c0d2c0d2c0e0f0c2d0d0f0d100c2d0c100d2c0d100d100c100d100c100d100c110c100d100c100d100c110c100d2c0d2c0d2c0d100c100d100c110c100d100c100d100c100d2c0d2c0d2c0d100c110c100d100c100d100d100c100d100c100d100c110c100d100c100d100c2d0c100d100d100c100d100c100d2c0d100d100c100d100c110c100d100c100d100d100c100d100c100d100d100c100d100c2d0c100e0f0d2c0d2c0d100c2d0c000d05"
TURN_ON = "2600bc016f3b0d100c2c0d100d100c100d100c100d100d100c100e0f0c110c100d2c0e0f0c100d100d0f0e0f0d100c100d2c0d2c0d2c0d100c100d2c0d100d100c100d100c100d100d100d0f0d100c100d100c110c100d100c100d100c110d0f0d100c100d100d100c100d100c100d100d100c100d100c100d2c0d2c0d100d100c100e0f0d0f0d0001486f390f100c2c0d100d100c100d100c100d100e0f0c100d100c110c100d2c0d100c100e0f0c100d100d100c100d2c0d2c0d2c0d100c100d2c0d100d100c100d100d0f0d100d100c100d100c100d100c100d100d2c0d100c100d2c0d100c2d0c100d100d100c100d2c0d2c0d100c2d0c100d100d0f0d100d100c100d100c110c100d2c0d2c0d2c0d2c0d2b0e2c0d100c2d0d0f0d110b2d0c100d2c0d100c110c100d100c100d100c110c100e0f0c100d100c110c100d2c0d2c0d2c0d100c100d100c110c100d100c100d100c100d2c0e2b0d2c0d100c100d100e0f0c100d100c100d100e0f0c100d100d100c100d100c100d100d2c0d100c100d100c100d100c100d2d0c100d100c100d100d100c100d100c110c100d100c100d100d100c100d100d100c2c0d2c0d100d100c2d0c2d0d0f0d2c0d000d05"
TEMP_UP = "2600bc0171390d100c2d0c100d100d100c100d100c100d100d100c100d100c100d2c0e0f0c110c100d100c100d100d100c2c0e2b0d2c0d100c110c2d0c100d100c100d100c110c100d100c100d100c110c100e0f0c100d100c100d100d100d0f0d100c110c100d100c100d100c110c100d100c100d100c110c2c0d2c0d100d100c100d100c100d0001486f3b0c110c2c0d100d100c100d100c100d100d100c100d100c110c100d2c0d100c100d100c100d100c110c100d2c0d2c0c2d0d100c100d2c0d100c110c100c110c100d100c100d100c110c100d100c100d100c2d0c100d100d2c0d100c2d0c100d100c100d100c2d0c2d0c110c2c0d100d100c100d100c100d100d100c100d100c2d0c2d0c2d0d2c0c2d0d2c0c100d2c0d100c100d2c0e0f0c2d0c110c100d100c100d100c110c100d100c100d100c110c100d100c2d0d2c0c2d0c100d100c100d100d100c100d100c100d100c2d0c2d0c2d0c100d100d100c100d100c100d100c110c100d100c100d100d100c100d100c100d2c0d100c110c100d100c100e0f0c2d0c110c100d10100c0d100c110c100d100c110c100d100c100d100c110c100d100c2d0c2d0c100d100d2c0c2d0c100d2c0d000d05"
TEMP_DOWN = "2600bc016f3b0c100d2c0d100d100c100d100c100d100d100c100d100c100d100c2d0d100c100d100c100e0f0c110c100d2c0d2c0c2d0d100c100d2c0d100c100d100c110c100d100c100d100c110c100d100c100d100c110d0f0d100c100d100c110c100d100c100d100c100d100d100c100d100c110d0f0d2c0d2c0c110c100d100c100d100c000148713a0c100d2c0d100c100d100c110c100c110c100d100c100d100d100c2d0c100d100c100d100d100c100d100c2d0d2c0c2d0d0f0d100c2d0d0f0d100d100c100d100c100d100d100c100d100c100d100c110c2d0c100d100c2d0d0f0d2c0d100c110c100c2d0d100c2d0d0f0d2c0d100c100d100c110c100d100c100d100c100d2d0c2c0d2c0d2c0d2c0d2c0d100c2d0c110c100d2c0d100c2d0d0f0d100c100d100c110c100d100c100e0f0c110c100d100c100d2c0e2b0e2b0d100c100d100c110c100d100c100d100d100c2c0d2c0d2c0d100d100c100d100c100d100c110c100d100c100d100c110c100d100c100d100d2c0c110c100d100c100d100c110c2d0c100d100c100d100d100c100d100c110c100d100c100d100d100c100d100c100d2c0d100c110c100d2c0d2c0d100c2d0c000d05"

#configuraciones del broadlink RM4C mini
DEVTYPE = 0x6539
HOST = "192.168.100.53"
PORT = 80
MAC = "24dfa7501214"


# Fetch the service account key JSON file contents
cred = credentials.Certificate('./energy-coach-firebase-adminsdk-wxvhm-d5099bd43d.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://energy-coach-default-rtdb.firebaseio.com/'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules

# Get a database reference to our posts
ref = db.reference('recomendation')

# Read the data at the posts reference (this is a blocking operation)

diccionario=ref.get()
opcion=diccionario['rec']


#dev = broadlink.gendevice(DEVTYPE,(HOST,PORT), MAC)
#dev.auth()
devices = broadlink.discover()
device = devices[0]
device.auth()
#dev.send_data(DATA)

def convert_data(data: str):
    return bytearray.fromhex(data)

def turn_on_AC(device):
    data = convert_data(TURN_ON)
    device.send_data(data)

def turn_off_AC(device):
    data = convert_data(TURN_OFF)
    device.send_data(data)

def temp_up_AC(device):
    data = convert_data(TEMP_UP)
    device.send_data(data)

def temp_down_AC(device):
    data = convert_data(TEMP_DOWN)
    device.send_data(data)

def control_AC(code: int):
    ans = True
    
    if code == 1:
        #encender aire
       turn_on_AC(device)
    if code == 2:
         #apagar aire
        turn_off_AC(device)
    if code == 3:
        #subir temperatura
        temp_up_AC(device)
    if code == 4:
        #bajar temperatura
        temp_down_AC(device)
    if code == 5:
        print("Standby")
    
def listener(event):
        print(event.data)
        dict=event.data
        print(dict['rec'])
        control_AC(int(dict['rec']))  # new data at /reference/event.path. None if deleted
def main():
    #control_AC(int(opcion))    
    firebase_admin.db.reference('/recomendation').listen(listener)
if __name__ == '__main__':
    main()
             

