from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import re
import time
import pymysql

# Create your views here.
line_bot_api="***"
handler="***"
parser="***"

@csrf_exempt
def callback(request):
    if request.method=='POST':
        signature=request.META['HTTP_X_LINE_SIGNATURE']
        body=request.body.decode('utf-8')

        try:
            events=parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden("")
        except LineBotApiError:
            return HttpResponseBadRequest("")

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext=event.message.text
                    if mtext=="01有用資訊" or mtext=="01有靈性啟發" or mtext=="01有趣" or mtext=="01不認同" or mtext=="01有心情感受":
                        userid=str(event.source).split('"')[7]
                        db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                        cursor=db.cursor()
                        db.autocommit(True)
                        sql_str="update forward set q1=\"{}\" where userid=\"{}\" order by time desc limit 1".format(mtext, userid)
                        cursor.execute(sql_str)
                        db.close()
                        message=ImagemapSendMessage(
                            base_url='https://i.imgur.com/2WwmrDTd.png',
                            alt_text='Image Map',
                            base_size=BaseSize(width=1040, height=1040),
                            actions=[
                                MessageImagemapAction(
                                    text='02有一點',
                                    area=ImagemapArea(x=520, y=0, width=520, height=520)
                                ),
                                MessageImagemapAction(
                                    text='02普通',
                                    area=ImagemapArea(x=0, y=520, width=520, height=520)
                                ),
                                MessageImagemapAction(
                                    text='02非常',
                                    area=ImagemapArea(x=520, y=520, width=520, height=520)
                                )
                            ]
                        )
                        line_bot_api.reply_message(event.reply_token, message)
                        return HttpResponse("")

                    elif mtext=="02有一點" or mtext=="02普通" or mtext=="02非常":
                        userid=str(event.source).split('"')[7]
                        db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                        cursor=db.cursor()
                        db.autocommit(True)
                        sql_str="update forward set q2=\"{}\" where userid=\"{}\" order by time desc limit 1".format(mtext, userid)
                        cursor.execute(sql_str)
                        db.close()
                        message=TemplateSendMessage(
                            alt_text='Confirm template',
                            template=ConfirmTemplate(
                                text='3.請問您有回覆該則訊息嗎？',
                                actions=[
                                    MessageTemplateAction(label='有', text='03有'),
                                    MessageTemplateAction(label='無', text='03無')
                                ]
                            )
                        )
                        line_bot_api.reply_message(event.reply_token, message)
                        return HttpResponse("")

                    elif mtext=="03有" or mtext=="03無":
                        userid=str(event.source).split('"')[7]
                        db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                        cursor=db.cursor()
                        db.autocommit(True)
                        sql_str="update forward set q3=\"{}\" where userid=\"{}\" order by time desc limit 1".format(mtext, userid)
                        cursor.execute(sql_str)
                        db.close()
                        message=TemplateSendMessage(
                            alt_text='Confirm template',
                            template=ConfirmTemplate(
                                text='4.請問您是否有分享這個訊息給其他人？',
                                actions=[
                                    MessageTemplateAction(label='有', text='04有'),
                                    MessageTemplateAction(label='無', text='04無')
                                ]
                            )
                        )
                        line_bot_api.reply_message(event.reply_token, message)
                        return HttpResponse("")

                    elif mtext=="04有" or mtext=="04無":
                        userid=str(event.source).split('"')[7]
                        db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                        cursor=db.cursor()
                        db.autocommit(True)
                        sql_str="update forward set q4=\"{}\" where userid=\"{}\" order by time desc limit 1".format(mtext, userid)
                        cursor.execute(sql_str)
                        db.close()
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(
                            text="5.請問您在哪個群組中看到這訊息？（請先輸入05，再輸入群組名，例如：05媽祖進香群；若並非在群組中讀到此訊息，請輸入：05無）"
                        ))
                        return HttpResponse("")

                    elif re.match(r"^(05).+",mtext):
                        userid=str(event.source).split('"')[7]
                        db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                        cursor=db.cursor()
                        db.autocommit(True)
                        sql_str="update forward set q5=\"{}\" where userid=\"{}\" order by time desc limit 1".format(mtext, userid)
                        cursor.execute(sql_str)
                        db.close()
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(
                            text="6.請問發這封訊息的人是？（請先輸入06，再輸入發訊息者在社群媒體中的名字，例如：06王小明）"
                        ))
                        return HttpResponse("")

                    elif re.match(r"^(06).+",mtext):
                        userid=str(event.source).split('"')[7]
                        db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                        cursor=db.cursor()
                        db.autocommit(True)
                        sql_str="update forward set q6=\"{}\" where userid=\"{}\" order by time desc limit 1".format(mtext, userid)
                        cursor.execute(sql_str)
                        db.close()
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(
                            text="已完成登錄，宗教機器人謝謝您！下次看到有感的訊息，別忘了轉傳給我喔！"
                        ))
                        return HttpResponse("")


                    elif mtext=="我主動發了公開訊息，我要登錄":
                        message=TemplateSendMessage(
                            alt_text='Confirm template',
                            template=ButtonsTemplate(
                                text='請問您在哪裡主動發文？',
                                actions=[
                                    MessageTemplateAction(label='LINE', text='10LINE'),
                                    MessageTemplateAction(label='Facebook', text='10Facebook')
                                ]
                            )
                        )
                        line_bot_api.reply_message(event.reply_token, message)

                    elif mtext=="10LINE":
                        userid=str(event.source).split('"')[7]
                        time=str(event.timestamp)[0:10]
                        db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                        cursor=db.cursor()
                        db.autocommit(True)
                        sql_str="insert into line(userid, time) values(\"{}\",\"{}\")".format(userid, time)
                        cursor.execute(sql_str)
                        db.close()
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(
                            text="11.請問您在何群組中發文？（請先輸入11，再輸入群組名稱，例如：11媽祖進香群；若並非在群組發文，請輸入：11無）"
                        ))
                        return HttpResponse("")

                    elif re.match(r"^(11).+",mtext):
                        userid=str(event.source).split('"')[7]
                        db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                        cursor=db.cursor()
                        db.autocommit(True)
                        sql_str="update line set q1=\"{}\" where userid=\"{}\" order by time desc limit 1".format(mtext, userid)
                        cursor.execute(sql_str)
                        db.close()
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(
                            text="12.請問您是發文給誰？（請先輸入12，再輸入人名，例如：12王小明；若無明確對象，請輸入：12無）"
                        ))
                        return HttpResponse("")

                    elif re.match(r"^(12).+",mtext):
                        userid=str(event.source).split('"')[7]
                        db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                        cursor=db.cursor()
                        db.autocommit(True)
                        sql_str="update line set q2=\"{}\" where userid=\"{}\" order by time desc limit 1".format(mtext, userid)
                        cursor.execute(sql_str)
                        db.close()
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(
                            text="已完成登錄，宗教機器人謝謝您！下次若還有主動發文，別忘了來這裡登錄喔"
                        ))
                        return HttpResponse("")


                    elif mtext=="10Facebook":
                        userid=str(event.source).split('"')[7]
                        time=str(event.timestamp)[0:10]
                        db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                        cursor=db.cursor()
                        db.autocommit(True)
                        sql_str="insert into facebook(userid, time) values(\"{}\",\"{}\")".format(userid, time)
                        cursor.execute(sql_str)
                        db.close()
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(
                            text="13.請問您是在誰的FB發文？（請先輸入13，再輸入人名或社團名稱，例如：13王小明、13媽祖進香群；若是在自己的FB發文，請輸入：13自己）"
                        ))
                        return HttpResponse("")

                    elif re.match(r"^(13).+",mtext):
                        userid=str(event.source).split('"')[7]
                        db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                        cursor=db.cursor()
                        db.autocommit(True)
                        sql_str="update facebook set q1=\"{}\" where userid=\"{}\" order by time desc limit 1".format(mtext, userid)
                        cursor.execute(sql_str)
                        db.close()
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(
                            text="已完成登錄，宗教機器人謝謝您！下次若還有主動發文，別忘了來這裡登錄喔"
                        ))
                        return HttpResponse("")


                    else:
                        userid=str(event.source).split('"')[7]
                        time=str(event.timestamp)[0:10]
                        db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                        cursor=db.cursor()
                        db.autocommit(True)
                        sql_str="insert into forward(userid, time, content) values(\"{}\",\"{}\",\"{}\")".format(userid, time, mtext)
                        cursor.execute(sql_str)
                        db.close()
                        message=ImagemapSendMessage(
                            base_url='https://i.imgur.com/af8Qqgra.png',
                            alt_text='Image Map',
                            base_size=BaseSize(width=1040, height=1560),
                            actions=[
                                MessageImagemapAction(
                                    text='01有用資訊',
                                    area=ImagemapArea(x=520, y=0, width=520, height=520)
                                ),
                                MessageImagemapAction(
                                    text='01有靈性啟發',
                                    area=ImagemapArea(x=0, y=520, width=520, height=520)
                                ),
                                MessageImagemapAction(
                                    text='01有趣',
                                    area=ImagemapArea(x=520, y=520, width=520, height=520)
                                ),
                                MessageImagemapAction(
                                    text='01不認同',
                                    area=ImagemapArea(x=0, y=1040, width=520, height=520)
                                ),
                                MessageImagemapAction(
                                    text='01有心情感受',
                                    area=ImagemapArea(x=520, y=1040, width=520, height=520)
                                )
                            ]
                        )
                        line_bot_api.reply_message(event.reply_token, message)
                        return HttpResponse("")

            else:
                return HttpResponse("")
    else:
        return HttpResponseBadRequest("")
