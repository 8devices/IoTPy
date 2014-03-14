from mosquitto import Mosquitto

def on_connect(mosq, obj, rc):
    mosq.subscribe("8dev/response", 0)
    print("rc: "+str(rc))

def on_message(mosq, obj, msg):
    print("response:"+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

def on_publish(mosq, obj, mid):
    print("mid: "+str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)

mqttc = Mosquitto()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
#mqttc.on_log = on_log
#mqttc.connect("test.mosquitto.org", 1883, 60)
mqttc.connect("192.168.101.96", 1883, 60)
while True:
    mqttc.loop(1, 1)
    cmd = raw_input("Enter command for remote: ")
    mqttc.publish("8dev/cmd", cmd)
    mqttc.loop(1, 2)






