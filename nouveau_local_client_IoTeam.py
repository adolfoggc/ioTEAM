# -*- coding: utf-8 -*-

import RPi.GPIO as gpio
import os, time
import paho.mqtt.client as mqtt
import sys
import datetime
import random, threading, json

#####definicoes:

Broker = "localhost"
PortaBroker = 1883
KeepAliveBroker = 60
Luz = 'IoTEAM/light' 
Presenca = 'IoTEAM/presence'
Response = 'IoTEAM/response_00'
Action = 'IoTEAM/action'
gpio.setmode(gpio.BCM)
#força tensão no pino para baixo
#23 sensor de presença
gpio.setup(23, gpio.IN, pull_up_down = gpio.PUD_DOWN)

#sensor de luminosidade
gpio.setup(24, gpio.IN, pull_up_down = gpio.PUD_DOWN)

#sinal de resposta
gpio.setup(25, gpio.OUT)
gpio.output(25,0)

#####callbacks
#Callback - Conexao ao broker realizada
def on_connect(client, userdata, flags, rc):
    #print('[STATUS] Conectado ao Broker. Resultado de conexao: '+str(rc))
    print('[STATUS] Conectado ao Broker')
    #faz subscribe automatico no topico
    client.subscribe(Response)

#Callback - Mensagem recebida do broker
def on_message(client, userdata, msg):
    MensagemRecebida = str(msg.payload)
    
    print('[MSG RECEBIDA] Topico: '+msg.topic+' / Mensagem: '+MensagemRecebida)
    sensor_Data_Handler(msg.topic, msg.payload)

#Callback - Em caso de desconectar
def on_disconnect(client, userdata,rc=0):
    logging.debug('Código de desconexão: '+str(rc))
    client.loop_stop()
    

    
def return_time():
    return time.strftime('%Y %b %d %H:%M:%S -03', time.gmtime())
try:
        acao = 0
        #print(datetime.tzname())
        print('[STATUS] Inicializando MQTT...')
        #inicializa MQTT:
        client = mqtt.Client(client_id='IoTEAM_Device_00') #informando ID do cliente
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(Broker, PortaBroker, KeepAliveBroker)
        
        #client.loop_forever() #aguardando callbacks
        client.loop_start()
        if(gpio.input(23) == 1):
            
            presence_data = {}
            presence_data['Date'] = return_time()
	    presence_data['Detection'] = 'STARTING - YES'
	    presence_json_data = json.dumps(presence_data)
            
            client.publish(Presenca, presence_json_data)
            presence = 1
            print('P->1,A')
            
        else:
            presence_data = {}
            presence_data['Date'] = return_time()
	    presence_data['Detection'] = 'STARTING - NO'
	    presence_json_data = json.dumps(presence_data)
            
            client.publish(Presenca, presence_json_data)
            
            presence = 0
            print('P->0,A')
        if(gpio.input(24) == 1):
            light_data = {}
            light_data['Date'] = return_time()
	    light_data['State'] = 'STARTING - DARK'
	    light_json_data = json.dumps(light_data)
            
            client.publish(Luz, light_json_data )
            
            luz = 1
            print('L->1,A')
        else:
            light_data = {}
            light_data['Date'] = return_time()
	    light_data['State'] = 'STARTING - LIGHT'
	    light_json_data = json.dumps(light_data)
            
            client.publish(Luz, light_json_data)
            
            luz = 0
            print('L->0,A')
        client.loop_stop()
        client.loop_forever()
        while True:
            if(gpio.input(23) == 1 and presence == 0):
                presence_data = {}
                presence_data['Date'] = return_time()
                presence_data['Detection'] = 'YES'
                presence_json_data = json.dumps(presence_data)
                client.publish(Presenca, presence_json_data)
                
                presence = 1
                print('P:0->1')
            elif (gpio.input(23) == 0 and presence == 1):
                presence_data = {}
                presence_data['Date'] = return_time()
                presence_data['Detection'] = 'NO'
                presence_json_data = json.dumps(presence_data)
            
                client.publish(Presenca, presence_json_data)
                presence = 0
                print('P:1->0')
            if(gpio.input(24) == 1 and luz == 0):
                light_data = {}
                light_data['Date'] = return_time()
                light_data['State'] = 'LIGHT'
                light_json_data = json.dumps(light_data)
            
                client.publish(Luz, light_json_data)
                luz = 1
                print('L:0->1')
            if(gpio.input(24) == 0 and luz == 1):
                light_data = {}
                light_data['Date'] = return_time()
                light_data['State'] = 'DARK'
                light_json_data = json.dumps(light_data)
            
                client.publish(Luz, light_json_data)
                
                luz = 0
                print('L:1->0')
                
            #ações com lógica invertida devido relé
            if (luz == 1 or presence == 0):
            
                if (acao == 0):
                    gpio.output(25, 1)
                    action_data = {}
                    action_data['Date'] = return_time()
                    action_data['State'] = 'OFF'
                    action_json_data = json.dumps(action_data)
            
                    client.publish(Action, action_json_data)

                    print('A:1->0')
                    acao = 1
            if (luz == 0 and presence == 1):
            #if (luz == 1 or presence == 0):
                if (acao == 1):
                    gpio.output(25, 0)
                    action_data = {}
                    action_data['Date'] = return_time()
                    action_data['State'] = 'ON'
                    action_json_data = json.dumps(action_data)
            
                    client.publish(Action, action_json_data)

                    print('A:0->1')
                    acao = 0
except KeyboardInterrupt:
        print '\nCtrl+C pressionado, encerrando aplicacao e saindo...'
        if(gpio.input(23) == 1):
            presence_data = {}
            presence_data['Date'] = return_time()
	    presence_data['Detection'] = 'DISCONNECTING -YES'
	    presence_json_data = json.dumps(presence_data)
            
            client.publish(Presenca, presence_json_data)
            print('P >1<, D')
        else:
            presence_data = {}
            presence_data['Date'] = return_time()
	    presence_data['Detection'] = 'DISCONNECTING - NO'
	    presence_json_data = json.dumps(presence_data)
            
            client.publish(Presenca, presence_json_data)
            print('P >0<, D')
        if(gpio.input(24) == 1):
            light_data = {}
            light_data['Date'] = return_time()
	    light_data['State'] = 'DISCONNECTING - LIGHT'
	    light_json_data = json.dumps(light_data)
            
            client.publish(Luz, light_json_data)
            print('L >1<, D')
        else:
            light_data = {}
            light_data['Date'] = return_time()
	    light_data['State'] = 'DISCONNECTING - DARK'
	    light_json_data = json.dumps(light_data)
            
            client.publish(Luz, light_json_data)
            print('L >0<, D')
        client.loop_stop() #encerra o loop
        gpio.cleanup()
        sys.exit(0)
