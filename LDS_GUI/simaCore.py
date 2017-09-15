# -*- coding: cp1252 -*-
import time
import sys
import ConfigParser
import serial
import re
import os

def Restart():
    print("[SimaCore] Reboot")
    python = sys.executable
    os.execl(python, python, * sys.argv)

def Quit():
    print("[SimaCore] Shutdown")
    sys.exit()._exit()

def GetArduinoCode(arduino):
    code = arduino.readline()
    data_ser = re.findall('\d+', code)
    if not data_ser or data_ser[0] == 0:
        print("[ERROR] No glove.")
        return "0"
    else:
        return data_ser[0]
            
def GetCode(file):
    txt = []
    db = open(file, 'r')
    with db as inputfile:
        for line in inputfile:
            txt.append(line.strip().split(';'))
        code = [item[0] for item in txt]
    db.close()
    return code

def GetFr(file):
    txt = []
    db = open(file, 'r')
    with db as inputfile:
        for line in inputfile:
            txt.append(line.strip().split(';'))
        word_fr = [item[1] for item in txt]
    db.close()
    return word_fr

def GetEn(file):
    txt = []
    db = open(file, 'r')
    with db as inputfile:
        for line in inputfile:
            txt.append(line.strip().split(';'))
        word_en = [item[2] for item in txt]
    db.close()
    return word_en

def interpreter_fr(ser, code, word_fr):
    if ser != "0":
        if ser in code:
            idx = code.index(ser)
            return word_fr[idx]
        else:
            print("[WARNING] Code non reconnu")
            return "error"
    else:
        print("[ERROR] Le code recu est invalide")
        return "null"

def interpreter_en(ser, code, word_en):
    if ser != "0":
        if ser in code:
            idx = code.index(ser)
            return word_en[idx]
        else:
            print("[WARNING] Unknown code")
            return "error"
    else:
        print("[ERROR] Invalid code")
        return "null"
        
def learn(ser, words_new, file):
    try:
        db = open(file, 'a')
        data_ser = re.findall('\d+', ser)
        line = ("\n" + data_ser[0] + ";" + words_new)
        db.write(line)
        db.close()
        print ("[INFO] Success ! Learned line: "+ line)
    except IOError:
        print("[ERROR] Database I/O Error!")

def debug_fr(value, code, word_fr):
    data_ser = re.findall('\d+', value)
    if not data_ser:
        print ("[ERROR] Gant deconnecte")
        return "0"
    elif data_ser[0] != "0":
        if data_ser[0] in code:
            idx = code.index(data_ser[0])
            return word_fr[idx]
        else:
            print ("[WARNING] Code non reconnu")
            return "error"
    else:
        print ("[ERROR] Le code recu est invalide")
        return "null"

def debug_en(value, code, word_en):
    data_ser = re.findall('\d+', value)
    if not data_ser:
        print ("[ERROR] Glove is not connected")
        return "0"
    elif data_ser[0] != "0":
        if data_ser[0] in code:
            idx = code.index(data_ser[0])
            return word_en[idx]
        else:
            print ("[WARNING] Unknown code")
            return "error"
    else:
        print ("[ERROR] Invalid code")
        return "null"
