import paho.mqtt.client as mqtt
import threading,os,time
from bottle import route, run

html='''
<meta content="True" name="HandheldFriendly" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="mobile-web-app-capable" content="yes" />
<script type="text/javascript" src="//leytton.gitee.io/simjq/releases/simJQ-2.2.min.js"></script>
<style>
a{
	display: inline-block;
    padding: 1em;
    font-size: 3em;
    font-weight: 600;
    line-height: 20px;
    white-space: nowrap;
    vertical-align: middle;
    cursor: pointer;
    user-select: none;
    background-repeat: repeat-x;
    background-position: -1px -1px;
    background-size: 110% 110%;
    border: 1px solid rgba(27,31,35,0.2);
    border-radius: 0.25em;
    -webkit-appearance: none;
    color: #fff;
    background-color: #28a745;
    background-image: linear-gradient(-180deg, #34d058 0%, #28a745 90%);
    text-transform: none;
    text-decoration: none;
    margin: 1em;
}
</style>
<script>
function send(a){
	$.ajax({
	   	method: 'GET',
	   	url:"/"+a,
	    success: function (data,xhr) {
	       alert("发送成功");
	    }
	});
}
</script>
<body style="text-align: center;">
<a onclick="send('1')">开</a>
<br>
<a onclick="send('0')" style="background-image: linear-gradient(-180deg, #d03434 0%, #a72828 90%);">关</a>
<br>
<iframe src="/watch" />
'''

rec=""
html2="""
 <meta http-equiv="refresh" content="1">
 """
def sendMqtt(s):
	print(s)
	client.publish("cuiliyan/suo/a", payload=s, qos=0, retain=False)

@route('/favicon.ico')
def index():
	return

@route('/watch')
def index():
	return html2+suo+'<br>'+rec

@route('/:name')
def index(name = '-'):
	sendMqtt("cmd"+name+"pw1234")
	return "cmd"+name
@route('/')
def index(name = '-'):
	client.publish("home/light", payload=name, qos=0, retain=False)
	return html

# 当连接上服务器后回调此函数
def on_connect(client, userdata, flags, rc):
	pass
    #print("Connected with result code " + str(rc))
    #client.subscribe("home/light")


# 从服务器接受到消息后回调此函数
suo=""
def on_message(client, userdata, msg):
	global rec,suo
	msg=msg.payload.decode('utf8')
	print("命令:" + msg)
	if msg=="kai":
		rec=time.strftime("%Y %B %d %Y %H:%M:%S", time.localtime(time.time()))+" 开<br>"+rec
		return
	if msg=="guan":
		rec=time.strftime("%Y %B %d %Y %H:%M:%S", time.localtime(time.time()))+" 关<br>"+rec
		return
	suo=msg

client = mqtt.Client(client_id="DeviceId-n44f8pa9b3",)
# 参数有 Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
client.on_connect = on_connect  #设置连接上服务器回调函数
client.on_message = on_message  #设置接收到服务器消息回调函数
#client.tls_set()
#client.username_pw_set("chome/ctrl1", password="y0m3kp+k7kdqLykuAdRyyl6REv7iO6+P5zY2UdjiwRY=")
client.connect("test.mosquitto.org", 1883, 60)  # 连接服务器,端口为1883,维持心跳为60秒
client.subscribe("cuiliyan/suo/b")
threading.Thread(target=client.loop_forever).start()
PORT = int(os.getenv('PORT', 8080))
run(host='0.0.0.0',port=PORT)