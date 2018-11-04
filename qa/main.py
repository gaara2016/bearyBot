#coding=utf-8
from bearychat import openapi
import json
from urllib import parse
from tornado.ioloop import IOLoop,PeriodicCallback
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from tornado.websocket import websocket_connect
import qa.StockFun as stock

class Client(object):
    def __init__(self):
        self.ioloop = IOLoop.instance()
        self.openapi = openapi.Client("bf8ccfe31798793255856708978b3e3b")
        self.me = '@<=' + self.openapi.user.me()['id'] + '=>'
        self.ws = None
        self.connect()
        PeriodicCallback(self.keep_alive, 20000, io_loop=self.ioloop).start()
        self.ioloop.start()

    @gen.coroutine
    def connect(self):
        print("1")
        print("trying to connect")
        try:
            post_data = {'token': "bf8ccfe31798793255856708978b3e3b"}
            get_url = yield AsyncHTTPClient().fetch("https://rtm.bearychat.com/start", method="POST",
                                                    body=parse.urlencode(post_data), connect_timeout=5, request_timeout=5)
            url = json.loads(get_url.body.decode()).get('result', {}).get('ws_host')
            # print("2")
            # print ("url"+url)
            self.ws = yield websocket_connect(url, connect_timeout=5)
        except Exception as e:
            print("connection error,{}".format(e))
        else:
            # print("3")
            # print("connected")
            self.run()

    @gen.coroutine
    def run(self):
        while True:
            msg = yield self.ws.read_message()
            if msg is None:
                self.ws = None
                break
            try:
                msg = json.loads(msg)
            except:
                self.ws = None
                break

            if msg.get('type') != "channel_message":
                continue
            print("5")
            print(msg)
            #replay_func = Handler.get(msg.get("text"))
            text = msg.get('text')
            print("从bot接收到的消息:"+str(text))
            # self.me = text
            # print("refer_key")
            # print(msg.get('refer_key'))
            textArray = str(text).split("+")
            if textArray[0] == "股票查询":
                if msg.get('refer_key') != '':
                    raw_text = "选项：\n"\
                               "1：证券基本资料\n" \
                               "2：输出从当前开始的一周的K线\n" \
                               "3：三年除权信息\n" \
                               "4：复权因子\n" \
                               "5：季频盈利能力\n" \
                               "6：季频营运能力\n" \
                               "7：季频成长能力\n" \
                               "8：季频偿债能力\n" \
                               "9：季频现金流\n" \
                               "10：季频杜邦指数\n" \
                               "11：季频业绩快报\n" \
                               "12:季频业绩预告\n" \
                               "13:查询相关参数" \
                               "请输入选项 + 股票代码\n"
                    finish_text = json.dumps(
                        {"text": raw_text,
                         "vchannel_id": msg.get("vchannel_id"),
                         "call_id": 23,
                         # "refer_key": msg.get("key"),
                         "refer_key": '',
                         "type": "channel_message",
                         "channel_id": msg.get("channel_id")}
                    )
                    self.ws.write_message(finish_text)
            elif textArray[0] == "1":
                #StockInfo
                temp = []
                if msg.get('refer_key') != '':
                    raw_text = stock.StockFunctions.StockInfo(self,textArray[1])
                    print(raw_text)
                    for i in range(len(raw_text)):
                        test = ''
                        for j in range(len(raw_text[0])):
                            mat = "{:15}"
                            single = mat.format(raw_text[i][j])
                            test = test + single
                        temp.append(test)

                    # print(temp)
                    content = ""
                    for k in range(0,len(temp)):
                        content =content + temp[k]+"\n"
                    print(content)
                    finish_text = json.dumps(
                        {"text": content,
                         "vchannel_id": msg.get("vchannel_id"),
                         "call_id": 23,
                         # "refer_key": msg.get("key"),
                         "refer_key": '',
                         "type": "channel_message",
                         "channel_id": msg.get("channel_id")}
                    )
                    self.ws.write_message(finish_text)
            elif textArray[0] == "2":
                temp = []
                if msg.get('refer_key') != '':
                    raw_text = stock.StockFunctions.k_Line(self, textArray[1])
                    print(raw_text)
                    for i in range(len(raw_text)):
                        test = ''
                        for j in range(len(raw_text[0])):
                            mat = "{:15}"
                            single = mat.format(raw_text[i][j])
                            test = test + single
                        temp.append(test)

                    # print(temp)
                    content = ""
                    for k in range(0, len(temp)):
                        content = content + temp[k] + "\n"
                    print(content)
                    finish_text = json.dumps(
                        {"text": content,
                         "vchannel_id": msg.get("vchannel_id"),
                         "call_id": 23,
                         # "refer_key": msg.get("key"),
                         "refer_key": '',
                         "type": "channel_message",
                         "channel_id": msg.get("channel_id")}
                    )
                    self.ws.write_message(finish_text)


                print()
            elif textArray[0] == "3":
                temp = []
                if msg.get('refer_key') != '':
                    raw_text = stock.StockFunctions.ChuquanInfo(self, textArray[1])
                    print(raw_text)
                    for i in range(len(raw_text)):
                        test = ''
                        for j in range(len(raw_text[0])):
                            mat = "{:15}"
                            single = mat.format(raw_text[i][j])
                            test = test + single
                        temp.append(test)

                    # print(temp)
                    content = ""
                    for k in range(0, len(temp)):
                        content = content + temp[k] + "\n"
                    print(content)
                    finish_text = json.dumps(
                        {"text": content,
                         "vchannel_id": msg.get("vchannel_id"),
                         "call_id": 23,
                         # "refer_key": msg.get("key"),
                         "refer_key": '',
                         "type": "channel_message",
                         "channel_id": msg.get("channel_id")}
                    )
                    self.ws.write_message(finish_text)
                print()
            elif textArray[0] == "4":
                temp = []
                if msg.get('refer_key') != '':
                    raw_text = stock.StockFunctions.FuquanInfo(self, textArray[1])
                    print(raw_text)
                    for i in range(len(raw_text)):
                        test = ''
                        for j in range(len(raw_text[0])):
                            mat = "{:15}"
                            single = mat.format(raw_text[i][j])
                            test = test + single
                        temp.append(test)

                    # print(temp)
                    content = ""
                    for k in range(0, len(temp)):
                        content = content + temp[k] + "\n"
                    print(content)
                    finish_text = json.dumps(
                        {"text": content,
                         "vchannel_id": msg.get("vchannel_id"),
                         "call_id": 23,
                         # "refer_key": msg.get("key"),
                         "refer_key": '',
                         "type": "channel_message",
                         "channel_id": msg.get("channel_id")}
                    )
                    self.ws.write_message(finish_text)
                print()
            elif textArray[0] == "5":
                temp = []
                if msg.get('refer_key') != '':
                    raw_text = stock.StockFunctions.Jipinyingli(self, textArray[1])
                    print(raw_text)
                    for i in range(len(raw_text)):
                        test = ''
                        for j in range(len(raw_text[0])):
                            mat = "{:15}"
                            single = mat.format(raw_text[i][j])
                            test = test + single
                        temp.append(test)

                    # print(temp)
                    content = ""
                    for k in range(0, len(temp)):
                        content = content + temp[k] + "\n"
                    print(content)
                    finish_text = json.dumps(
                        {"text": content,
                         "vchannel_id": msg.get("vchannel_id"),
                         "call_id": 23,
                         # "refer_key": msg.get("key"),
                         "refer_key": '',
                         "type": "channel_message",
                         "channel_id": msg.get("channel_id")}
                    )
                    self.ws.write_message(finish_text)
                print()
            elif textArray[0] == "6":
                temp = []
                if msg.get('refer_key') != '':
                    raw_text = stock.StockFunctions.Jipinyingyun(self, textArray[1])
                    print(raw_text)
                    for i in range(len(raw_text)):
                        test = ''
                        for j in range(len(raw_text[0])):
                            mat = "{:15}"
                            single = mat.format(raw_text[i][j])
                            test = test + single
                        temp.append(test)

                    # print(temp)
                    content = ""
                    for k in range(0, len(temp)):
                        content = content + temp[k] + "\n"
                    print(content)
                    finish_text = json.dumps(
                        {"text": content,
                         "vchannel_id": msg.get("vchannel_id"),
                         "call_id": 23,
                         # "refer_key": msg.get("key"),
                         "refer_key": '',
                         "type": "channel_message",
                         "channel_id": msg.get("channel_id")}
                    )
                    self.ws.write_message(finish_text)
                print()
            elif textArray[0] == "7":
                temp = []
                if msg.get('refer_key') != '':
                    raw_text = stock.StockFunctions.Jipinchengzhang(self, textArray[1])
                    print(raw_text)
                    for i in range(len(raw_text)):
                        test = ''
                        for j in range(len(raw_text[0])):
                            mat = "{:15}"
                            single = mat.format(raw_text[i][j])
                            test = test + single
                        temp.append(test)

                    # print(temp)
                    content = ""
                    for k in range(0, len(temp)):
                        content = content + temp[k] + "\n"
                    print(content)
                    finish_text = json.dumps(
                        {"text": content,
                         "vchannel_id": msg.get("vchannel_id"),
                         "call_id": 23,
                         # "refer_key": msg.get("key"),
                         "refer_key": '',
                         "type": "channel_message",
                         "channel_id": msg.get("channel_id")}
                    )
                    self.ws.write_message(finish_text)
                print()
            elif textArray[0] == "8":
                temp = []
                if msg.get('refer_key') != '':
                    raw_text = stock.StockFunctions.Jipinchangzhai(self, textArray[1])
                    print(raw_text)
                    for i in range(len(raw_text)):
                        test = ''
                        for j in range(len(raw_text[0])):
                            mat = "{:15}"
                            single = mat.format(raw_text[i][j])
                            test = test + single
                        temp.append(test)

                    # print(temp)
                    content = ""
                    for k in range(0, len(temp)):
                        content = content + temp[k] + "\n"
                    print(content)
                    finish_text = json.dumps(
                        {"text": content,
                         "vchannel_id": msg.get("vchannel_id"),
                         "call_id": 23,
                         # "refer_key": msg.get("key"),
                         "refer_key": '',
                         "type": "channel_message",
                         "channel_id": msg.get("channel_id")}
                    )
                    self.ws.write_message(finish_text)
                print()
            elif textArray[0] =="9":
                temp = []
                if msg.get('refer_key') != '':
                    raw_text = stock.StockFunctions.Jipinxianjinliu(self, textArray[1])
                    print(raw_text)
                    for i in range(len(raw_text)):
                        test = ''
                        for j in range(len(raw_text[0])):
                            mat = "{:15}"
                            single = mat.format(raw_text[i][j])
                            test = test + single
                        temp.append(test)

                    # print(temp)
                    content = ""
                    for k in range(0, len(temp)):
                        content = content + temp[k] + "\n"
                    print(content)
                    finish_text = json.dumps(
                        {"text": content,
                         "vchannel_id": msg.get("vchannel_id"),
                         "call_id": 23,
                         # "refer_key": msg.get("key"),
                         "refer_key": '',
                         "type": "channel_message",
                         "channel_id": msg.get("channel_id")}
                    )
                    self.ws.write_message(finish_text)

                print()
            elif textArray[0] == "10":
                temp = []
                if msg.get('refer_key') != '':
                    raw_text = stock.StockFunctions.Jipindubang(self, textArray[1])
                    print(raw_text)
                    for i in range(len(raw_text)):
                        test = ''
                        for j in range(len(raw_text[0])):
                            mat = "{:15}"
                            single = mat.format(raw_text[i][j])
                            test = test + single
                        temp.append(test)

                    # print(temp)
                    content = ""
                    for k in range(0, len(temp)):
                        content = content + temp[k] + "\n"
                    print(content)
                    finish_text = json.dumps(
                        {"text": content,
                         "vchannel_id": msg.get("vchannel_id"),
                         "call_id": 23,
                         # "refer_key": msg.get("key"),
                         "refer_key": '',
                         "type": "channel_message",
                         "channel_id": msg.get("channel_id")}
                    )
                    self.ws.write_message(finish_text)
                print()
            elif textArray[0] == "11":
                temp = []
                if msg.get('refer_key') != '':
                    raw_text = stock.StockFunctions.Jipinyejikuaibao(self, textArray[1])
                    print(raw_text)
                    for i in range(len(raw_text)):
                        test = ''
                        for j in range(len(raw_text[0])):
                            mat = "{:15}"
                            single = mat.format(raw_text[i][j])
                            test = test + single
                        temp.append(test)

                    # print(temp)
                    content = ""
                    for k in range(0, len(temp)):
                        content = content + temp[k] + "\n"
                    print(content)
                    finish_text = json.dumps(
                        {"text": content,
                         "vchannel_id": msg.get("vchannel_id"),
                         "call_id": 23,
                         # "refer_key": msg.get("key"),
                         "refer_key": '',
                         "type": "channel_message",
                         "channel_id": msg.get("channel_id")}
                    )
                    self.ws.write_message(finish_text)
                print()
            elif textArray[0] == "12":
                temp = []
                if msg.get('refer_key') != '':
                    raw_text = stock.StockFunctions.JipinyejiPredict(self, textArray[1])
                    print(raw_text)
                    for i in range(len(raw_text)):
                        test = ''
                        for j in range(len(raw_text[0])):
                            mat = "{:15}"
                            single = mat.format(raw_text[i][j])
                            test = test + single
                        temp.append(test)

                    # print(temp)
                    content = ""
                    for k in range(0, len(temp)):
                        content = content + temp[k] + "\n"
                    print(content)
                    finish_text = json.dumps(
                        {"text": content,
                         "vchannel_id": msg.get("vchannel_id"),
                         "call_id": 23,
                         # "refer_key": msg.get("key"),
                         "refer_key": '',
                         "type": "channel_message",
                         "channel_id": msg.get("channel_id")}
                    )
                    self.ws.write_message(finish_text)
            elif textArray[0] == "13":
                if msg.get('refer_key') != '':
                    raw_text = "https://github.com/gaara2016/bearyBot/blob/master/qa/参数说明文档"
                    finish_text = json.dumps(
                        {"text": raw_text,
                        "vchannel_id": msg.get("vchannel_id"),
                        "call_id": 23,
                        "refer_key": '',
                        "type": "channel_message",
                        "channel_id": msg.get("channel_id")}
                    )
                    self.ws.write_message(finish_text)

            else:
                if msg.get('refer_key') != '':
                    raw_text = "请输入:股票查询"
                    finish_text = json.dumps(
                        {"text": raw_text,
                        "vchannel_id": msg.get("vchannel_id"),
                        "call_id": 23,
                        "refer_key": '',
                        "type": "channel_message",
                        "channel_id": msg.get("channel_id")}
                    )
                    self.ws.write_message(finish_text)

    def keep_alive(self):
        if self.ws is None:
            self.connect()
        # else:
        #     self.ws.write_message('{"call_id": 29, "type": "ping"}')
if __name__ == "__main__":
    Client()
