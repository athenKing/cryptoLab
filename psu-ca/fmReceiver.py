from ot.otExtReceiver import  GeneralOTReceiver
from ot.simplest.receiver import SimplestReceiver
import math,json,requests
from parameters import CONFIG
from common.ds import genFlajoletMartin
from ot.networkConfig import NETWORK

def int2str(intLen,Integer):
    modulo = 1<<intLen
    Integer = Integer % modulo
    text = '0'*intLen
    Integer = bin(Integer)[2:]
    final = text[:intLen-len(Integer)] + Integer
    return final

if __name__ == "__main__":
    partialSum = 0
    wLen = CONFIG["DongLou"]["wLen"]
    PRIME = CONFIG["DongLou"]["PRIME"]

    fd = open('data/bob.data', 'r')
    bob = json.loads(fd.read())
    fd.close()
    fs = genFlajoletMartin(bob,wLen)

    r = requests.get('http://0.0.0.0:{}/onInit'.format(NETWORK["fmSender"]))
    simplestRecv = SimplestReceiver()
    simplestRecv.initiate(int(fs[0]))
    LASTSELECT = int(simplestRecv.final())
    partialSum += LASTSELECT

    for i in range(1,wLen):
        r = requests.get('http://0.0.0.0:{}/onOthers'.format(NETWORK["fmSender"]),json=json.dumps({"round":i}))

        choice = int(fs[i])
        if LASTSELECT%2==1:
            choice +=  2

        recv = GeneralOTReceiver(int2str(2,choice))
        LASTSELECT = int(recv.final())
        partialSum += LASTSELECT

    r = requests.get('http://0.0.0.0:{}/onGetFinal'.format(NETWORK["fmSender"]))
    final = (r.json()["partial"]+partialSum)%PRIME
    print(final)



