#LIBRERIAS TELEGRAM
import telebot
from telebot import types, util
#LIBRERIAS IMDB.COM
import omdb
from omdb import OMDBClient
#LIBRERIA PARA PARSEAR DATOS
import json
import requests

token = 'TOKEN_TELEGRAM'
bot = telebot.TeleBot(token)
omdb.set_default('apikey', 'TOKEN_OMDB')


#GUARDA EN comandos.txt, CADA MENSAJE RECIBIDO
def guardar_comandos(comando):
    f = open('comandos.txt','a')
    f.write('\n' + comando)
    f.close()


#EL COMANDO 'vercomandos', LEE Y DEVUELVE EL CONTENIDO DE comandos.txt
@bot.message_handler(commands=['vercomandos'])
def comandos(message):
    cmds = open("comandos.txt", "rb").read()
    txt = util.split_string(cmds, 3000)
    for x in txt:
	    bot.send_message(message.chat.id, x)


#PRIMERA FUNCIÓN, SE ACTIVA AL RECIBIR 'start'
def hola(message):
    mensaje = (
    "Hola {}\n".format(message.from_user.first_name)+
    "Escribe 'peli titanic', por ejemplo, para recibir datos de esa película\n"+
    "Tambien puedes buscar información de Transantiago al escribir 'micro PA269', por ejemplo.\n"+
    "recuerda iniciar el mensaje con 'peli' o 'micro'"
    )
    bot.send_message(message.chat.id, mensaje)

# COMANDO START, SE SIGUE LA MISMA LÓGICA PARA TODOS LOS COMANDOS PERSONALIZADOS
@bot.message_handler(commands=['start'])
def inicio(message):
    hola(message) #EJECUTA LA FUNCIÓN ANTERIOR



#CONSULTA Y RESPUESTA A IMDB.COM
#SE ACTIVA AL RECIBIR 'peli titanic' por ejemplo
def get_pelicula(titulo):
    res = omdb.request(t=titulo)
    peli = res.json()    
    info_ = ("\n\n\nTítulo\n"+peli['Title']+"\n\n"+
    "Estreno\n"+peli['Released']+"\n\n"+
    "Género\n"+peli['Genre']+"\n\n"+
    "Elenco principal\n"+peli['Actors']+"\n\n"+
    "Premios \n"+peli['Awards']+"\n\n"+
    "Dirigida por\n"+peli['Director']+"\n\n"+
    "Escrita por\n"+peli['Writer']+"\n\n"+
    "Rating IMDb\n"+peli['imdbRating']+" de 10 ("+ peli['imdbVotes'] +" votos) \n\n"+
    "Produccion \n"+peli['Production']+"\n\n"
    +peli['Poster']
    )
    return info_

#CONSULTA Y RESPUESTA A API TRANSANTIAGO
#SE ACTIVA AL RECIBIR 'micro PA269' por ejemplo
def get_paradero(paradero, m_id):
    r = (requests.get('https://api.adderou.cl/ts/?paradero='+str(paradero))).json()
    bot.send_message(m_id,('🚏 ')+(r['descripcion']))
    for x in r['servicios']:
        if x['valido']==1:
            bot.send_message(m_id,'🚌 '+x['servicio']+'\n'+x['tiempo']+'\n'+x['distancia'])
        elif x['valido']==0:
            bot.send_message(m_id,'🚫 🚌 '+x['servicio']+'\n'+x['descripcionError'])
            

#CONTROLADOR DE MENSAJES
@bot.message_handler(func=lambda message: True)
def responder(message):
    mensaje =  (message.text).lower()
    guardar_comandos(mensaje)
    if mensaje[0:4]=='peli':
        titulo = mensaje[4:]
        bot.send_message(message.chat.id, get_pelicula(titulo))
    elif mensaje[0:5]=='micro':
        paradero = mensaje[5:]
        bot.send_message(message.chat.id, get_paradero(paradero,message.chat.id ))
    else:

        bot.send_message(message.chat.id, 'Cómo dice que dijo?')
        bot.send_message(message.chat.id, "Necesitas ayuda? 🧐")



print("BOT INICIADO...")
bot.polling() #INICIO DE SCRIPT
