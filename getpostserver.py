from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
import json
import time 
import requests


class Resquest(BaseHTTPRequestHandler):
    def handler(self):
        print("data:", self.rfile.readline().decode())
        self.wfile.write(self.rfile.readline())
 
    def do_GET(self):
        print(self.requestline)
        print(self.path)
        #print(self.args)
        curr_timestamp = time.strftime("%Y%m%d %H%M%S",time.localtime(time.time()))

        if  not ('/sendmsg' in self.path):
            self.send_error(404, "Page not Found!")
            return
 
        parsed_path = parse.urlparse(self.path)
        message_parts = [
            'CLIENT VALUES:',
            'client_address={} ({})'.format(
                self.client_address,
                self.address_string()),
            'command={}'.format(self.command),
            'path={}'.format(self.path),
            'real path={}'.format(parsed_path.path),
            'query={}'.format(parsed_path.query),
            'request_version={}'.format(self.request_version),
            '',
            'SERVER VALUES:',
            'server_version={}'.format(self.server_version),
            'sys_version={}'.format(self.sys_version),
            'protocol_version={}'.format(self.protocol_version),
            '',
            'HEADERS RECEIVED:',
        ]
        for name, value in sorted(self.headers.items()):
            message_parts.append(
                '{}={}'.format(name, value.rstrip())
            )
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

        print('parsed_path_query:',parsed_path.query)
        parsed_path_query = str(parsed_path.query)
        query_split = parsed_path_query.split("&")
        if len(query_split) != 2:
            print('lack of mobile&contents.')
        else:
            query_mobile = query_split[0]
            query_content =  query_split[1]

            query_mobile = query_mobile[7:]
            query_content = query_content[8:]

            sent_dingtalk_str = '{"phone": "'
            sent_dingtalk_str = sent_dingtalk_str + query_mobile +'", "content":"'
            sent_dingtalk_str = sent_dingtalk_str + query_content +'", "timestamp":'
            sent_dingtalk_str = sent_dingtalk_str + str(curr_timestamp)+'}'

            print(sent_dingtalk_str)
            dingtalkmsg(self,sent_dingtalk_str)


        #send_data_str:{"phone": "139", "content": "message", "timestamp": 1620892761.1030157}
        # data = {
        #     'result_code': '1',
        #     'result_desc': 'Success',
        #     'timestamp': '',
        #     'data': {'message_id': '25d55ad283aa400af464c76d713c07ad'}
        # }
        # self.send_response(200)
        # self.send_header('Content-type', 'application/json')
        # self.end_headers()
        # self.wfile.write(json.dumps(data).encode())
 
 
    def do_POST(self):
        print('headers: ',self.headers)
        print('command: ',self.command)
        curr_timestamp = time.strftime("%Y%m%d %H%M%S",time.localtime(time.time()))

        parsed_path = parse.urlparse(self.path)

        headers_content_length = self.headers['content-length']
        #普通的post可返回headers['content-length']有值，返回None的可能是没有附带json内容的情况
        #CAS的报警http（post），就是此情况，CAS报警通过url传递参数。
        if headers_content_length:
            req_datas = self.rfile.read(int(self.headers['content-length']))
            #重点在此步!
            catch_data = req_datas.decode('utf-8')
            print('catch_data: ',catch_data)

            data = {
                'result_code': '2',
                'result_desc': 'Success成功',
                'timestamp': '',
                'data': {'message_id': curr_timestamp}
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
            with open('getpostserver.log','a') as fp_getposts:
                fp_getposts.write(catch_data)
                fp_getposts.write('\n')
            dingtalkmsg(self,catch_data)
        else:
            req_datas = self.rfile.read(0)
            #print('parsed_path_query:',parsed_path.query)
            parsed_path_query = res2=parse.unquote(parsed_path.query,encoding="UTF-8")
            print('parsed_path_query:',parsed_path.query)

            query_split = parsed_path_query.split("&")            

            if len(query_split) != 2:
                print('lack of mobile&contents.')
            else:
                query_mobile = query_split[0]
                query_content =  query_split[1]

                query_mobile = query_mobile[7:]
                query_content = query_content[8:]

                sent_dingtalk_str = '{"phone": "'
                sent_dingtalk_str = sent_dingtalk_str + query_mobile +'", "content":"'
                sent_dingtalk_str = sent_dingtalk_str + query_content +'", "timestamp":"'
                sent_dingtalk_str = sent_dingtalk_str + str(curr_timestamp)+'"}'

                print('sent_dingtalk_str: ',sent_dingtalk_str)
                dingtalkmsg(self,sent_dingtalk_str)


def dingtalkmsg(self,send_data_str):
    #send_data_str:{"phone": "139", "content": "message", "timestamp": 1620892761.1030157}
    try:
        send_data = json.loads(send_data_str)
    except:
        send_data = {}
    print('send_data',send_data)
    send_data_content = "事件:" + str(send_data['content']) 
    content = {
        "msgtype": "text",
        "text": {
            "content": send_data_content
            # 这里必须包含之前定义关键字 
                },
        "at": {
           # 发送给群里的所有人
            "isAtAll": False
             #单独 @ 某个人，使用绑定的手机号，
                # 多个人用户英文逗号隔开
               # "131xxxxxx811",
               # "137xxxxxxxxx"
                }
                }
    data_dict = {
        "msgtype":"markdown",

        "markdown":{"title":"运维时间通知",
        "text":send_data_content + "\n\n" +
                "> **Application_ID:** app-20201208100505-58622\n\n"
                "> **Server:** compute_04\n\n"
                "> **TimeStamp:** " + str(send_data['timestamp'])
            },
        "at": {
            "atMobiles": ['jason','138211112112'],
            "isAtAll": False
                 }
              }

    headers = {"Content-Type": "application/json;charset=utf-8"}

    url = "https://oapi.dingtalk.com/robot/send?access_token=dad05c0b71cc7f415b0c404d4e0a6a925bd4cd6f8ff38b86b0b3459dbc44"
    print('send json',content)
    r = requests.post(url=url,headers=headers,json=data_dict)
    print(r.content.decode())

 
if __name__ == '__main__':
    host = ('', 9001)
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()

