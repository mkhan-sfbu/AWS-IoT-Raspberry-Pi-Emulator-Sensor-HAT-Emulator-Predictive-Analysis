from sense_emu import SenseHat
import signal
import sys
import requests
import json
from decimal import Decimal

def round_float(v, ndigits=0, rt_str=False):
    d = Decimal(v)
    v_str = ("{0:.%sf}" % ndigits).format(round(d, ndigits))
    if rt_str:
        return v_str
    return Decimal(v_str)

sense = SenseHat()

def destroyAndRelease():
    print("Ctrl+C detected")
    print("    ", end="\r", flush=True)


def handleExit(signum, frame):
    destroyAndRelease()
    sys.exit(1)
 
 
signal.signal(signal.SIGINT, handleExit)

prvTempVal=curTempVal=round_float(sense.temp)
prvHumdVal=curHumdVal=round_float(sense.humidity)

awsApiUrl = 'https://ytoyerd09d.execute-api.us-east-1.amazonaws.com/test/week12hw2watering'

while True:
  curTempVal=round_float(sense.temp)
  curHumdVal=round_float(sense.humidity)
  if prvTempVal!=curTempVal or prvHumdVal!=curHumdVal:
    prvTempVal=curTempVal
    prvHumdVal=curHumdVal
    tempValue = round_float(float(curTempVal) / 2.5 + 16, 2)
    humidityValue = round_float(64 * float(curHumdVal) / 100, 2)
    print("Temperature or Humedity Changed!", curTempVal, curHumdVal)
    payload={'data': str(tempValue)+', '+str(abs(humidityValue))}
    print(payload)
    r=requests.post(awsApiUrl, data=json.dumps(payload))
    rText=r.text
    if 87==ord(rText[1]):
      print("Please DO watering today...........................!!!!!!!!!!!!!")
    else:
      print("NO need to watering...")


