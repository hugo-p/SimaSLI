@echo off
echo Activation de la page de codes 1252.
echo Pour la prise en charge des accents.
chcp 1252
if exist config.cfg (
	if exist db.txt (
		python main.py
		) else (
		echo Base de données introuvable
		echo Creez un fichier db.txt
		)
	)	else (
	echo Fichier configuration introuvable
	echo Creez un fichier config.cfg
	)