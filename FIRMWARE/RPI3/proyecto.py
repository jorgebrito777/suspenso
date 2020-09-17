import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from datetime import datetime

MS="Des"
h=16
m=58



est="Desactivado"
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(13, GPIO.OUT )
GPIO.setup(15, GPIO.OUT )
GPIO.setup(16, GPIO.OUT )
GPIO.setup(18, GPIO.OUT )
# HORA DEFINIDA PARA RIEGO

     
def riego_on():	#Funcion de riego encendido
   global est

   input_state = GPIO.input(11)
   if input_state == False:
      GPIO.output(13, True)   # Enciende el LED
      est="Activado"
      print("on")

def riego_off():	#Funcion de riego encendido
   global est

   input_state = GPIO.input(12)
   if input_state == False:
      GPIO.output(13, False)   # Enciende el LED
      est="Desactivado"
      print("off") 
   	
def tanque_lleno():	# Funcion de nivel de agua - tanque con agua
   global tan
   input_state = GPIO.input(7)
   if input_state == True:
      GPIO.output(16, True)   
      tan="Lleno"


	
   else:
      GPIO.output(16, False)   
      tan="Vacio"
  
   return tan 



def tanque_vacio():	# Funcion de nivel de agua - tanque sin agua
    input_state = GPIO.input(7)
    if input_state == False:
        GPIO.output(18, True)   
        return("Apagado")
        tan="Vacio"
       
	
    else:
        GPIO.output(18, False)   
	
def on_message(client, obj, msg):
   
    print( msg.payload.decode( "utf-8"))
    global est
    # Setencia  servidor de boton activado y desactivo 
    global MS
    MS=msg.payload.decode( "utf-8")
    if MS=="ACTIVADO":
        GPIO.output(13, True)   # Enciende el LED
        est="Activado"
        print("on")
      
   
    else:

        GPIO.output(13, False)   # Enciende el LED
        est="Desactivado"
       
    
	
# Sentencia servidor de comparación de la hora 
  
    global h
    global m
    
    h=int(msg.payload.decode("utf-8").split(":")[0]);
    m=int(msg.payload.decode("utf-8").split(":")[1]);
    

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.username_pw_set("menalyluzuriaga@gmail.com","1600482853mena")
mqttc.connect("maqiatto.com" , 1883)
mqttc.subscribe("menalyluzuriaga@gmail.com/test1", 0)
rc=0
print("inicio...")

def hora_activa():
   global est
   global MS
   if (h==h1) and  (m==m1 )and (MS!="DESACTIVADO"):
      GPIO.output(13, True)   # Enciende el LED
      est="Activado"
      print("on")
      

while True:

    ahora = datetime.now() 
    h1=ahora.hour
    m1=ahora.minute
    time.sleep(1)

    re=est	# Riego encendido
    res=riego_on()
    rea=riego_off()

    tl=tanque_lleno() 	# Tanque lleno
    tv=tanque_vacio() 	# Tanque vacio
    rc= mqttc.loop()
    ah=hora_activa()
    if(h<=9 and m<=9):
      mqttc.publish("menalyluzuriaga@gmail.com/test",str(re)+" "+str(tl)+" "+"0"+str(h)+":0"+str(m))
    if(h<=9 and m>=10):
      mqttc.publish("menalyluzuriaga@gmail.com/test",str(re)+" "+str(tl)+" "+"0"+str(h)+":"+str(m))
    if(h>=10 and m<=9):
      mqttc.publish("menalyluzuriaga@gmail.com/test",str(re)+" "+str(tl)+" "+str(h)+":0"+str(m))
    if(h>=10 and m>=10):
      mqttc.publish("menalyluzuriaga@gmail.com/test",str(re)+" "+str(tl)+" "+str(h)+":"+str(m))


