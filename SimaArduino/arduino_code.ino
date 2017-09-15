const int flex[] = {A0, A1, A2, A3, A4};                //pin flex
int bp[] = {12, 8, 9, 10, 11};                          //pin interrupteurs bout doigt
int flexp[5];                                           //variables 'resistance' des flex
bool bps[5];                                            //variables 'etat' des interrupteurs
int d[5];                                               //variables intermediaires 'etat' doigts
int doigt[5];                                           //variables finales 'etat' doigts

void setup(){
  Serial.begin(9600);                                   //initialisation de la communication série
  for (int i = 0; i < 5; i++){                          //setup des pins des flex/interrp
        pinMode(flex[i], INPUT);
        pinMode(bp[i], INPUT);
  }
}

void loop(){
    for (int i = 0; i < 5; i++){
        flexp[i] = analogRead(flex[i]);                 //acquisition de la 'position' des flex
        bps[i] = digitalRead(bp[i]);                    //acquisition de l'etat des interrupteurs
        
        d[i] = map(flexp[i], 90, 280, 0, 300);          //on ramène la valeur de la resistance à un multiple de 3
        d[i] = constrain(d[i], 0, 300);                 //on récupère les quelques valeurs volatiles

        doigt[i] = 0;                                   //valeur par défaut Etat 0 = dysfonctionnement d'un flex

        if (flexp[i] > 0){                              //si valeur resistance > 0 alors flex en place
            if (d[i] <= 100){                           //test doigt plié
                doigt[i] = 3;
            } else if (d[i] > 200){                     //test doigt tendu
                doigt[i] = 1;
            } else {                                    //test doigt à moitié plié
                doigt[i] = 2;
            }
            if (bps[i] == 1){                           //test si interrupteur activé (boolean)
                doigt[i] = doigt[i] + 3;                //si activé, rajouter 3
            }
        }
        Serial.print(doigt[i]);                         //Envoie des valeurs dans le port série
  }
    Serial.println();                                   //saut de ligne après chaque séquence de traitement
    delay(150);                                         //pause système
}
