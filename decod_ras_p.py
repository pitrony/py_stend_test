new_msg = msg
if msg['payload']['PTC'] == True:
    ptc = {'payload': "PTC ok"}
else:
    ptc = {'payload': "PTC not ok"}

speed_cases = {
    0: {'payload': "0 speed"},
    1: {'payload': "V1 speed (RH=1 RF=0 RY=0)"},
    2: {'payload': "V2 speed (RH=0 RF=1 RY=0)"},
    3: {'payload': "V3 speed (RH=1 RF=1 RY=0)"},
    4: {'payload': "V4 speed (RH=0 RF=0 RY=1)"},
    5: {'payload': "V5 speed (RH=1 RF=0 RY=1)"},
    6: {'payload': "V6 speed (RH=0 RF=1 RY=1)"},
    7: {'payload': "V7 speed (RH=1 RF=1 RY=1)"},
}

speed = speed_cases.get(msg['payload']['SPEED'], {'payload': "not correct speed"})

frn = {'payload': "Fren on"} if msg['payload']['FRN'] == True else {'payload': "Fren off"}
ru1 = {'payload': "Go to up"} if msg['payload']['RU1'] == True else None
ru2 = {'payload': "Go to down"} if msg['payload']['RU2'] == True else None
err = {'payload': "Eror direction"} if msg['payload']['RU2'] == True and msg['payload']['RU1'] == True else {'payload': "Ok"}

rgk = {'payload': "Contactor on"} if msg['payload']['RGK'] == True else {'payload': "Contactor off"}

result1 = [err, ptc, frn, rgk, ru2, ru1, speed]

# Function data2
new_msg = msg

pit = {'payload': "nearly Pit"} if msg['payload']['BOT'] == False else None
top = {'payload': "nearly Top"} if msg['payload']['TOP'] == False else None

err1 = {'payload': "Eror top and bot together"} if msg['payload']['TOP'] == False and msg['payload']['BOT'] == False else {'payload': " "}

opcl = {'payload': "door is close"} if msg['payload']['A3'] == True else {'payload': "door is open"}

ml2 = {'payload': "ML2 is on"} if msg['payload']['ML2'] == True else {'payload': ""}
ml1 = {'payload': "ML1 is on"} if msg['payload']['ML1'] == True else {'payload': ""}

if msg['payload']['ML2'] == True and msg['payload']['ML1'] == True:
    ml2 = {'payload': "In floor"}
    ml1 = {'payload': "In floor"}

dwn = {'payload': "move down"} if msg['payload']['DOWN'] == True else {'payload': ""}
up = {'payload': "move up"} if msg['payload']['UP'] == True else {'payload': ""}

insp = {'payload': "Normal"} if msg['payload']['INSP'] == True else {'payload': "Inspection"}

err2 = {'payload': "Try Move insp in normal"} if (new_msg['payload']['UP'] == True or new_msg['payload']['DOWN'] == True) and new_msg['payload']['INSP'] == True else None
err3 = {'payload': "error Move in insp both side"} if new_msg['payload']['UP'] == True and new_msg['payload']['DOWN'] == True and new_msg['payload']['INSP'] == False else None

result2 = [err1, err2, err3, pit, top, opcl, ml2, ml1, dwn, up, insp]

