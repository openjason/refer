import http.client, urllib.parse
import json
import time
import sys


def post_json_data(str1,str2):
	curr_timestamp = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))

	#str2_utf8 = str2.encode('utf-8')
	diag1 = {'phone':str1,'content':str2,'timestamp':curr_timestamp} #要发送的数据 ，因为要转成json格式，所以是字典类型
	data = json.dumps(diag1)

	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	conn = http.client.HTTPConnection('10.88.0.247', 9001)
	conn.request('POST', '/sendmsg', data.encode('utf-8'), headers)#往server端发送数据
	response = conn.getresponse()

	stc1 = response.read().decode('utf-8')#接受server端返回的数据
	stc = json.loads(stc1)

	print("-----------------接受server端返回的数据----------------")
	print(stc)
	print("-----------------接受server端返回的数据----------------")

	conn.close()



if __name__ == '__main__':

	if len(sys.argv) == 3:
		post_json_data(sys.argv[1],sys.argv[2])	
	else:	
		print ('参数个数为:', len(sys.argv), '个参数。')

		print ('参数列表:', str(sys.argv))
		print ('脚本名:', str(sys.argv[0]))
