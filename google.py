from colorama import init, Fore, Back, Style #Importamos la libreria de colorama
init(autoreset=True) #Necesitamos este init con el autoreset para que examine una por una las lineas de colorama
import json # importamos json
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools #importamos oauth
import datetime
import requests
from rfc3339 import rfc3339
#Correo
import base64
from email.mime.text import MIMEText
import mimetypes
import os
#Configuración api Google calendar
SCOPES = 'https://www.googleapis.com/auth/calendar'    #Acceso de lectura / escritura al calendario
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
	creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))
opcionMenu=" "
opcionGmail=" "
"""#configuracion api Gmail
SCOPES = ['https://mail.google.com',"https://mail.google.com",  "https://www.googleapis.com/auth/gmail.compose",  
"https://www.googleapis.com/auth/gmail.modify", "https://www.googleapis.com/auth/gmail.compose"]
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service= build('gmail', 'v1', http=creds.authorize(Http("""


def menu (opcionMenu): #Definicion menú
	print(Fore.YELLOW + Style.BRIGHT +("---------------------"))
	print(Fore.YELLOW + Style.BRIGHT +("---------------------"))
	print(Fore.WHITE + Style.BRIGHT +("Herramientas de Google."))
	print(Fore.YELLOW + Style.BRIGHT +("---------------------"))
	print(Fore.YELLOW + Style.BRIGHT +("1-Buscador de fechas"))
	print(Fore.YELLOW + Style.BRIGHT +("2-Creador de eventos"))
	print(Fore.YELLOW + Style.BRIGHT +("3-Gmail"))
	print(Fore.YELLOW + Style.BRIGHT +("4-Salir."))
	print(Fore.YELLOW + Style.BRIGHT +("---------------------"))
	opcionMenu = int(input(Fore.YELLOW + Style.BRIGHT +("Dime una opción correcta. ")))
	return opcionMenu
def menuGmail (opcionGmail): #Definicion de submenu
	print(Fore.RED + Style.BRIGHT +("---------------------"))
	print(Fore.RED + Style.BRIGHT +("---------------------"))
	print(Fore.WHITE + Style.BRIGHT +("Gmail."))
	print(Fore.RED + Style.BRIGHT +("---------------------"))
	print(Fore.RED + Style.BRIGHT +("1-Enviar mensaje "))
	print(Fore.RED + Style.BRIGHT +("2-Buscador de mensajes"))
	print(Fore.RED + Style.BRIGHT +("3-Monitorear correo"))
	print(Fore.RED + Style.BRIGHT +("4-Salir."))
	print(Fore.RED + Style.BRIGHT +("---------------------"))
	opcionGmail = int(input((Fore.RED + Style.BRIGHT +"Dime una opción correcta. ")))
	return opcionGmail


def crearMensaje (message, receptor, emisor, asunto):
	message['to'] = receptor
	message['from'] = emisor
	message['subject'] = asunto
	return{'raw': base64.urlsafe_b64encode(message.as_string())} #codificacion obligatoria
def enviarCorreo(service, user_id, message):
	message = service.users().messages().get(userId='me', id=msg_id).execute()
	return message	
while True: #un bucle true para que se ejecute siempre
	opcionMenu=menu(opcionMenu) #Para monstrar el menu siempre
	#condicionales para cada opcion del menu 
	if opcionMenu == 1:
		print(Fore.GREEN + Style.BRIGHT +("============================="))
		print(Fore.WHITE + Style.BRIGHT +("Buscador de eventos por fecha"))
		print(Fore.GREEN + Style.BRIGHT +("============================="))
		 # Llamar api
		fechaMin = input (Fore.WHITE + Style.BRIGHT +("Dime una fecha mínima a buscar (año,mes,dia,hora): "))
		listafechamin=fechaMin.split(",")
		#print(listafechamin)
		datemin = datetime.datetime(int(listafechamin[0]),int(listafechamin[1]),int(listafechamin[2]),int(listafechamin[3]))
		timeMin = rfc3339(datemin) 
		fechaMax = input(Fore.WHITE + Style.BRIGHT +("Dime una fecha maxima a buscar (año,mes,dia,hora): "))
		listafechamax=fechaMax.split(",")
		datemax = datetime.datetime(int(listafechamax[0]),int(listafechamax[1]),int(listafechamax[2]),int(listafechamax[3]))
		timeMax = rfc3339(datemax)
		#print("TimeMax:",timeMax)
		events_result = service.events().list(calendarId='primary', timeMin=timeMin,timeMax=timeMax,
												  maxResults=100, singleEvents=True,
												  orderBy='startTime').execute()
		events = events_result.get('items', [])
		#print(events)
		if len(events) == 0:
			print(Fore.WHITE + Style.BRIGHT +('No se encontraron eventos'))
		for event in events:
			start = event['start'].get('dateTime', event['start'].get('date'))
			print(Fore.WHITE + Style.BRIGHT +(start, event['summary']))
		print(Fore.GREEN + Style.BRIGHT +("***********************************"))
		print(Fore.GREEN + Style.BRIGHT +('Imprimiendo 100 eventos encontrados'))

	elif opcionMenu == 2:
		event = {
			'summary': '',
			'location': '',
			'description': '',
			'start': {
			'dateTime': '',
			},
			'end': {
			'dateTime': '',#2018-06-15T09:00:00-07:00
			},
			}
		nombreEvento=input(Fore.BLUE + Style.BRIGHT +("Introduce el nombre del evento: "))
		event["summary"]=nombreEvento
		localizacion=input(Fore.BLUE + Style.BRIGHT +("Introduce la localización del evento: "))
		event["location"]=localizacion
		descripcion=input(Fore.BLUE + Style.BRIGHT +("Introduce la descripción del evento: "))
		event["description"]=descripcion
			
		#Pido una fecha por teclado.
		fechaInic = input(Fore.BLUE + Style.BRIGHT +("Dime una fecha de inicio (año,mes,dia,hora): "))
		listafechaInic=fechaInic.split(",")
		#print(listafechamin)
		inicioF = datetime.datetime(int(listafechaInic[0]),int(listafechaInic[1]),int(listafechaInic[2]),int(listafechaInic[3]))
		fechaInicio = rfc3339(inicioF) 
		event['start']['dateTime']=fechaInicio
		fechaFn = input(Fore.BLUE + Style.BRIGHT +("Dime una fecha de fin (año,mes,dia,hora): "))
		listafechaFin=fechaFn.split(",")
		finF = datetime.datetime(int(listafechaFin[0]),int(listafechaFin[1]),int(listafechaFin[2]),int(listafechaFin[3]))
		fechaFin = rfc3339(finF)
		event['end']['dateTime']=fechaFin
		evento=service.events().insert(calendarId='primary', body=event).execute()
		print (Fore.WHITE + Style.BRIGHT +('Evento creado correctamente:'))
	elif opcionMenu == 3:
		while True:
			opcionGmail=menuGmail(opcionGmail)
			if opcionGmail == 1:
				message = MIMEText(input(Fore.BROWN + Style.BRIGHT +("Dime el texto que quieres enviar. ")))
				receptor = input(Fore.BROWN + Style.BRIGHT +("Para quien va este email. "))
				emisor = input(Fore.BROWN + Style.BRIGHT +("Emisor del email. "))
				asunto=input(Fore.BROWN + Style.BRIGHT +("Introduce el asunto"))
				crearMensaje()
				enviarCorreo()
				print(Fore.WHITE + Style.BRIGHT +("Enviado corretamente"))
			elif opcionGmail == 2:
				response = requests.get("https://www.googleapis.com/gmail/v1/users/me/messages?q=in:sent after:2018/01/01 before:2018/01/30")
				#Llamada a la API con la variable buscar
				data=response.json()
				print(Fore.WHITE + Style.BRIGHT +(data))

			elif opcionGmail == 4:
				break
	elif opcionMenu == 4:
		print(Fore.WHITE + Style.BRIGHT +("---------------------"))
		print(Fore.GREEN + Style.BRIGHT +("Gracias por usar esta herramienta."))
		print(Fore.WHITE + Style.BRIGHT +("---------------------"))
		break
				