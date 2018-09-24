import threading,os,time,mybottle
from mybottle import route, run,template,static_file,post,request
import json
import socket  
import time
import threading
ser=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ser.bind(('0.0.0.0',6000))

def rec_thread():
	while(1):
		s=str(ser.recvfrom(2048)[0])
		print(s)
t1=threading.Thread(target=rec_thread, args=())
t1.setDaemon(True)
t1.start()
def live_thread():
	while(1):
	    ser.sendto("ep=Q8X14B6KHD9DVWB2&pw=112233".encode('utf8'), ('115.29.240.46',6000))
	    time.sleep(15)
t2=threading.Thread(target=live_thread, args=())
t2.setDaemon(True)
t2.start()

class iot_device(object):
	def __init__(self):
		super(iot_device, self).__init__()
		self.last_state=""
		self.history=""
	def update(self,msg):
		if msg=="kai":
			self.history=get_str_time()+" 开<br>"+self.history
			return
		if msg=="guan":
			self.history=get_str_time()+" 关<br>"+self.history
			return
		if(self.last_state==msg):
			return
		print("update",msg)
		self.last_state=msg
		self.history=get_str_time()+msg+"<br>"+self.history
		

html2="""
 <meta http-equiv="refresh" content="1">
 """
def sendMqtt(s):
	client.publish("cuiliyan/suo/a", payload=s, qos=0, retain=False)
	print(s)
	

@route('/favicon.ico')
def index():
	return

@route('/watch/:id')
def index(id):
	return html2+'<br>'+iot_devices[id].history
@route('/device/:id')
def index(id):
	return template('ctrl',device_id=id)

@route('/show')
def index():
	s=[]
	for key in iot_devices:
		s.append(key)
	return template('show',keys=s)

@route('/')
def index(name = '-'):
	return template('index')

@route('/js/:name')
def index(name = '-'):
	return static_file(name, root="views")
@route('/css/:name')
def index(name = '-'):
	return static_file(name, root="views")

@post('/cmd')
def index():
	if request.forms.get('password')=="1234":
		username = request.forms.get('username')
		cmd = int(request.forms.get('cmd'))
		if cmd==1:
			ser.sendto("on".encode('utf8'), ('115.29.240.46',6000))
		else:
			ser.sendto("off".encode('utf8'), ('115.29.240.46',6000))
		return "1"
	else:
		return "0"


def get_str_time():
	return time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time()))
# 从服务器接受到消息后回调此函数
iot_devices={}
iot_devices.update({ "nbiot": iot_device()})
# def on_message(client, userdata, msg):
# 	msg=msg.payload.decode('utf8')
# 	try:
# 		result=json.loads(msg)
# 		d_id=str(result["id"])
# 		d_data=result["data"]
# 		if iot_devices.get(d_id)==None:
# 			iot_devices.update({d_id: iot_device()})
# 		iot_devices[d_id].update(d_data)
# 	except Exception as e:
# 		print(msg,e)
	# d_id=msg[7:13]
	



PORT = int(os.getenv('PORT', 80))
mybottle.debug(True)
run(host='0.0.0.0',port=PORT)