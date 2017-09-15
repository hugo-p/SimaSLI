# -*- coding: cp1252 -*-
import pygame
from pygame.locals import *
import time
import sys
import ConfigParser
import serial
import re
########## library perso ##########
import textinput
import simaCore
###################################

pygame.init()
input_text =  textinput.TextInput()

default_code = "00000"
file = 'db.txt'

logo = 'logo.png'
icon = 'icon.png'
cfg = 'config.cfg'

########## Fichier config.cfg ##########
config = ConfigParser.ConfigParser()
config.read(cfg)
port = config.get('arduino', 'port')
baud = config.get('arduino','debit')
timeout = config.getint('arduino', 'timeout')
showdbg = config.getboolean('sima', 'debug')
debugt = config.getint('sima', 'debug_timeout')
file = config.get('sima', 'database')
default_code = config.get('sima', 'debug_code')
########################################

########## Couleurs ##########
BLANC = (225,225,225)
ROUGE = (240, 0, 0)
NOIR = (0, 0, 0)
VIOLET = (184, 65, 217)
VERT = (0, 217, 0)
BLEU = (106, 145, 209)
ORANGE = (244, 134, 66)
##############################

########## Test du serial port ##########
com = None
try: 
        ser_arduino = serial.Serial(port, baud, rtscts=True, dsrdtr=True, timeout=timeout)
        com = 1
        print("[INFO] Port available")
except IOError:
        com = 0
        showdbg = True
        print("[WARNING] Port unavailable! Debug mode forced!")
########################################

########## Setup de la fenetre ##########
win = pygame.display.set_mode((800, 450))

font = pygame.font.Font("VeraBd.ttf", 40)
font_little = pygame.font.Font("VeraBd.ttf", 25)

label_intr = b"F1 - Mode interprétation"
intr = font.render(label_intr.decode('utf-8'), True, NOIR)

label_learn = u"F2 - Mode apprentissage"
learn = font.render(label_learn, True, NOIR)

label_test = u"F3 - Mode test/debug"
test = font.render(label_test, True, NOIR)

label_port = u"Port: " + port
render_port = font_little.render(label_port, True, VIOLET)

label_debit = b"Débit: " + baud
render_debit = font_little.render(label_debit.decode('utf-8'), True, VERT)

label_timeout = b"Serial Timeout: " + str(timeout) + "s"
render_timeout = font_little.render(label_timeout.decode('utf-8'), True, ORANGE)

label_debug = b"Debug activé"
render_debug = font_little.render(label_debug.decode('utf-8'), True, ROUGE)

image_logo = pygame.image.load(logo).convert_alpha()
image_icon = pygame.image.load(icon)

pygame.display.set_icon(image_icon)
caption= "SímaSLI - Sign Language Interpreter"
pygame.display.set_caption(caption, 'SímaSLI')
#############################################

################## Logger ###################
print("[INFO] Port: " + port)
print("[INFO] Baudrate: " + baud)
print("[INFO] Serial timeout: " + str(timeout))
print("[INFO] Debug: " + str(showdbg))
print("[INFO] Debug timeout: " + str(debugt))
print("[INFO] Database: " + file)
print("[INFO] Default code: " + default_code)
############################################

########## Lancement du programme ##########
loop = True

while loop:
    events = pygame.event.get()
    loop_menu = True
    loop_intr = False
    loop_learn = False
    loop_test = False
    while loop_menu:
        win.fill(BLANC)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                simaCore.Quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                simaCore.Quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    simaCore.Restart()
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        print("[SimaCore] Mode interpretation")
                        loop_intr = True
                        loop_menu = False
                        error = None
                        TITLE_COORD = (170, 100)
                        ERROR_COORD = (180, 200)
                        FR_COORD = (80, 200)
                        EN_COORD = (80, 250)
                        ####### Initialisation database #######
                        code = simaCore.GetCode(file)
                        word_fr = simaCore.GetFr(file)
                        word_en = simaCore.GetEn(file)
                        #######################################
                        old = "77777"
                        while loop_intr:
                            events = pygame.event.get()
                            for event in events:
                                if event.type == pygame.QUIT:
                                    simaCore.Quit()
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                    simaCore.Restart()
                            label_intr_title = b"Mode interprétation"
                            render_intr_title = font.render(label_intr_title.decode('utf-8'), True, NOIR)
                            win.blit(render_intr_title, TITLE_COORD)
                            pygame.display.flip()
                            if com==0:
                                ser = default_code
                            else:
                                ser = simaCore.GetArduinoCode(ser_arduino)
                            if ser != old:
                                old = ser
                                show_fr = simaCore.interpreter_fr(ser, code, word_fr)
                                show_en = simaCore.interpreter_en(ser, code, word_en)
								
                                if show_fr == "error":
                                    error = 1
                                    label_unknown = "Signe non reconnu"

                                elif show_fr == "null":
                                    simaCore.Restart()
                                else:
                                    error = 0
                                    print("[INFO] " + show_fr)
                                    print("[INFO] " + show_en)
                                    label_motfr = b"FR: " + show_fr
                                    label_moten = b"EN: " + show_en

                            win.fill(BLANC)
                            label_intr_title = b"Mode interprétation"
                            render_intr_title = font.render(label_intr_title.decode('utf-8'), True, NOIR)
                            win.blit(render_intr_title, TITLE_COORD)
                            if error == 1:
                                render_unknown = font.render(label_unknown, True, ROUGE)
                                win.blit(render_unknown, ERROR_COORD)
                            else:
                                render_motfr = font.render(label_motfr.decode('utf-8'), True, VERT)
                                render_moten = font.render(label_moten.decode('utf-8'), True, VERT)
                                win.blit(render_motfr, FR_COORD)
                                win.blit(render_moten, EN_COORD)
                            pygame.display.flip()

                    elif event.key == pygame.K_F2:
                        print("[SimaCore] Mode apprentissage")
                        loop_learn = True
                        loop_menu = False
                        while loop_learn:
                            win.fill(BLANC)
                            events = pygame.event.get()
                            for event in events:
                                if event.type == pygame.QUIT:
                                    simaCore.Quit()
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                    simaCore.Restart()
                            pygame.draw.rect(win, BLEU, (150, 265, 500, 40))
                            win.blit(input_text.get_surface(), (155, 270))
                            label_learn_title = b"Mode apprentissage"
                            render_learn_title = font.render(label_learn_title.decode('utf-8'), True, NOIR)
                            win.blit(render_learn_title, (170, 110))

                            label_learn_advice1 = b'Rentrez les 2 mots à apprendre: "fr;en"'
                            render_learn_advice1 = font_little.render(label_learn_advice1.decode('utf-8'), True, NOIR)
                            win.blit(render_learn_advice1, (120, 220))
                            
                            if input_text.update(events):
                                get_new = input_text.get_text()
                                pygame.time.delay(500)
                                if com==0:
                                    ser = default_code
                                else:
                                    ser = simaCore.GetArduinoCode(ser_arduino)
                                simaCore.learn(ser, get_new, file)
                            pygame.display.flip()

                    elif com == 0 and event.key == pygame.K_F3:
                        print("[SimaCore] Mode test/debug")
                        print("[INFO] You can define debug timeout in the cfg file")
                        loop_test = True
                        loop_menu = False
                        TITLE_COORD = (260, 100)
                        ERROR_COORD = (200, 200)
                        NULL_COORD = (230, 200)
                        error = None
                        ####### Initialisation database #######
                        code = simaCore.GetCode(file)
                        word_fr = simaCore.GetFr(file)
                        word_en = simaCore.GetEn(file)
                        #######################################
                        while loop_test:
                            win.fill(BLANC)
                            events = pygame.event.get()
                            for event in events:
                                if event.type == pygame.QUIT:
                                    simaCore.Quit()
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                    simaCore.Restart()
                            pygame.draw.rect(win, BLEU, (150, 265, 500, 40))
                            win.blit(input_text.get_surface(), (155, 270))
                            label_test_title = b"Mode Test"
                            render_test_title = font.render(label_test_title.decode('utf-8'), True, NOIR)
                            win.blit(render_test_title, TITLE_COORD)

                            label_test_advice1 = b'Testez un code: "12345", (delai configurable)'
                            render_test_advice1 = font_little.render(label_test_advice1.decode('utf-8'), True, NOIR)
                            win.blit(render_test_advice1, (85, 200))

                            if input_text.update(events):
                                code_test = input_text.get_text()
                                debugfr = simaCore.debug_fr(code_test, code, word_fr)
                                debugen = simaCore.debug_en(code_test, code, word_en)

                                if debugfr == "error":
                                    error = 1
                                    label_unknown = "Signe non reconnu"

                                elif debugfr == "null" or debugfr == "0":
                                    error = 2
                                    label_null = "ERREUR = NULL"

                                else:
                                    error = 0
                                    label_motfr = b"FR: " + debugfr
                                    label_moten = b"EN: " + debugen

                                win.fill(BLANC)
                                label_intr_title = b"Mode Test: " + str(debugt) + "s"
                                if error == 1:
                                    render_unknown = font.render(label_unknown, True, ROUGE)
                                    win.blit(render_unknown, ERROR_COORD)
                                elif error == 2:
                                    render_null = font.render(label_null, True, ROUGE)
                                    win.blit(render_null, NULL_COORD)
                                elif error == 0:
                                    render_motfr = font.render(label_motfr.decode('utf-8'), True, VERT)
                                    render_moten = font.render(label_moten.decode('utf-8'), True, VERT)
                                    win.blit(render_motfr, (80, 200))
                                    win.blit(render_moten, (80, 250))

                                render_intr_title = font.render(label_intr_title.decode('utf-8'), True, NOIR)
                                win.blit(render_intr_title, TITLE_COORD)
                                pygame.display.flip()
                                debug_delay = debugt * 1000
                                pygame.time.delay(debug_delay)
                            pygame.display.flip()

        win.blit(intr, (100, 30))
        win.blit(learn, (100, 90))
        win.blit(render_port, (100, 270))
        win.blit(render_debit, (100, 310))
        win.blit(render_timeout, (100, 350))
        win.blit(image_logo, (450, 250))
        if showdbg:
            win.blit(test, (100, 150))
            win.blit(render_debug, (100, 390))
        pygame.display.update()
