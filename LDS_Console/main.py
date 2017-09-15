# -*- coding: cp1252 -*-
import time
import sys
import ConfigParser
import serial
from colorama import init, Fore
import re

init(autoreset=True)

txt = []
idx = None

#Fichier config.cfg
port = None
baud = None
cfg = 'config.cfg'
config = ConfigParser.ConfigParser()
config.read(cfg)
port = config.get('arduino', 'port')
baud = config.getint('arduino','debit')
print (Fore.GREEN + "Initialisation du logiciel...")
print (Fore.GREEN + "Lecture du fichier config.cfg")
time.sleep(1)
#Fin de la config
com = None
try:
        ser_arduino = serial.Serial(port, baud)
        print (Fore.MAGENTA + "Port: " + port)
        print (Fore.MAGENTA + "Baud: " + str(baud))
        com = 1
except IOError:
        print (Fore.RED + "Port: " + port + " //indisponible - unavailable")
        print (Fore.RED + "Baud: " + str(baud))
        com = 0

rep = True
while rep:
        print ("""
        1.Mode interpretation
        2.Mode apprentissage
        3.Mode test (sans liaison serie)
        4.Quitter

        1.Intepreter mode
        2.Machine learning
        3.Test (test without serial communication)
        4.Quit
                """)

        rep=raw_input("Choisissez le mode - Choose the mode: ")
        #Mode interprétation
        if rep=="1":
                print(Fore.CYAN + """
                > Initialisation du mode interpretation
                > Initializing of interpreter mode
                        """)
                time.sleep(2)
                rep=False
                db = open('db.txt', 'r')
                with db as inputfile:
                        for line in inputfile:
                                txt.append(line.strip().split(';'))

                code = [item[0] for item in txt]
                word_fr = [item[1] for item in txt]
                word_en = [item[2] for item in txt]

                try:
                        while True:
                                data_ser = ['00000']
                                if com == 1:
                                        ser = ser_arduino.readline()
                                else:
                                        ser = "00000"
                                data_ser = re.findall('\d+', ser)
                                if data_ser[0] in code:
                                        idx = code.index(data_ser[0])
                                        print (Fore.CYAN + "FR:" + word_fr[idx])
                                        print (Fore.CYAN + "EN:" + word_en[idx])
                                        print " "
                                else:
                                        print (Fore.RED + "Signe non reconnu")
                                        print (Fore.RED + "Unknown sign")
                except KeyboardInterrupt:
                        print (Fore.RED + "> Liaison interrompue")
                        print (Fore.RED + "> Interpreter closed")
                        rep=True
        #Mode apprentissage
        elif rep=="2":
                print(Fore.CYAN + """
                > Initialisation du mode apprentissage
                > Initializing of machine learning mode
                        """)
                time.sleep(2)
                rep=False
                ask_fr=None
                ask_en=None
                db = open('db.txt', 'a')
                ask_fr=raw_input("Mot a apprendre: ")
                ask_en=raw_input("Word to learn: ")
                print (Fore.GREEN + "Nous allons proceder a l'apprentissage d'un mot")
                print (Fore.GREEN + "We're going to learn a word")
                print ("> Faites le signe et gardez la position durant tout le processus")
                print ("> Do the sign and keep the position throughout the process")
                print (Fore.RED + "Ne bougez pas ! - Don't move!")
                time.sleep(1)
                data_ser = ['00000']
                if com == 1:
                        ser = ser_arduino.readline()
                else:
                        ser = "00000"
                data_ser = re.findall('\d+', ser)
                print (Fore.RED + "Le processus peut durer quelques secondes")
                print (Fore.RED + "The process may takes a few seconds")
                time.sleep(2)
                db.write("\n" + data_ser[0] + ";" + ask_fr + ";" + ask_en)
                db.close
                print (Fore.GREEN + "> Apprentissage termine")
                print (Fore.GREEN + "> Learning finished")
                time.sleep(0.5)
                rep=True

        #Mode TEST
        elif rep=="3":
                print(Fore.YELLOW + """
                > Initialisation du mode test
                > Initializing of Test mode
                        """)
                debug = True
                db = open('db.txt', 'r')
                with db as inputfile:
                        for line in inputfile:
                                txt.append(line.strip().split(';'))
                code = [item[0] for item in txt]
                word_fr = [item[1] for item in txt]
                word_en = [item[2] for item in txt]
                while debug:
                        ask=raw_input("Continuer ? - Continue? o/n: ")
                        if ask =="o" or ask =="O" or ask =="y" or ask =="Y":
                                deb=raw_input("Donnees/Data: ")
                                print (Fore.YELLOW + "Simulation: " + deb)
                                time.sleep(.200)
                                if deb in code:
                                        idx = code.index(deb)
                                        print (Fore.CYAN + "FR:" + word_fr[idx])
                                        print (Fore.CYAN + "EN:" + word_en[idx])
                                        print " "
                                else:
                                        print (Fore.RED + "Signe non reconnu")
                                        print (Fore.RED + "Unknown sign")
                                        print " "
                                        time.sleep(1)
                                time.sleep(.200)
                        else:
                                debug = False
        #Fermeture
        elif rep=="4":
                print(Fore.MAGENTA + """
                > Fermeture...
                > Shutdown...
                        """)
                time.sleep(1)
                sys.exit()

        #Gestion d'erreur
        else:
                print(Fore.RED + """
                > ERREUR: Valeur innatendue (1,2,3,4)
                > ERROR: Unattended value (1,2,3,4)
                        """)
                time.sleep(2)
                rep=True
