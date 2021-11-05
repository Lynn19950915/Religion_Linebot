from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import re
import time
import pymysql

# Create your views here.
line_bot_api=LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler=WebhookHandler(settings.LINE_CHANNEL_SECRET)
parser=WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method=="POST":
        signature=request.META["HTTP_X_LINE_SIGNATURE"]
        body=request.body.decode("utf-8")

        try:
            events=parser.parse(body, signature)
        except ValueError:
            return None
        except InvalidSignatureError:
            return HttpResponseForbidden("")
        except LineBotApiError:
            return HttpResponseBadRequest("")

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext=event.message.text.strip()
                    if mtext=="00是，開始登錄":
                        messageQ01_event(event)
                        return HttpResponse("")

                    elif mtext=="01有用資訊" or mtext=="01有靈性啟發" or mtext=="01有趣" or mtext=="01不認同":
                        userid=str(event.source).split('"')[7]
                        db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                        cursor=db.cursor()
                        db.autocommit(True)
                        sql_str="update forward set q1=\"{}\" where userid=\"{}\" order by time desc limit 1".format(mtext, userid)
                        cursor.execute(sql_str)
                        db.close()
                        messageQ02_event(event)
                        return HttpResponse("")

                    elif mtext=="01有心情感受":
                        userid=str(event.source).split('"')[7]
                        db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                        cursor=db.cursor()
                        db.autocommit(True)
                        sql_str="update forward set q1=\"{}\" where userid=\"{}\" order by time desc limit 1".format(mtext, userid)
                        cursor.execute(sql_str)
                        db.close()
                        messageQ02A_event(event)
                        return HttpResponse("")

                    elif mtext=="02有一點" or mtext=="02普通" or mtext=="02非常" or mtext=="02非常陰鬱低落" or mtext=="02有點陰鬱低落" or mtext=="02有點陽光正面" or mtext=="02非常陽光正面":
                        userid=str(event.source).split('"')[7]
                        db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                        cursor=db.cursor()
                        db.autocommit(True)
                        sql_str="update forward set q2=\"{}\" where userid=\"{}\" order by time desc limit 1".format(mtext, userid)
                        cursor.execute(sql_str)
                        db.close()
                        messageQ03_event(event)
                        return HttpResponse("")

                    elif mtext=="03有" or mtext=="03無":
                        userid=str(event.source).split('"')[7]
                        db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                        cursor=db.cursor()
                        db.autocommit(True)
                        sql_str="update forward set q3=\"{}\" where userid=\"{}\" order by time desc limit 1".format(mtext, userid)
                        cursor.execute(sql_str)
                        db.close()
                        messageQ04_event(event)
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

                    elif re.match(r"^(05)\.?$", mtext) or re.match(r"^(06)\.?$", mtext) or re.match(r"^(11)\.?$", mtext) or re.match(r"^(12)\.?$", mtext) or re.match(r"^(13)\.?$", mtext):
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(
                            text="您並沒有完整輸入訊息，請連同題號再重新輸入一次！謝謝您！"
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
                        messageQ10_event(event)
                        return HttpResponse("")

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
                            text="已完成登錄，宗教機器人謝謝您！下次若還有主動發文，別忘了來這裡登錄喔！"
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
                            text="已完成登錄，宗教機器人謝謝您！下次若還有主動發文，別忘了來這裡登錄喔！"
                        ))
                        return HttpResponse("")


                    elif mtext=="00不，不是":
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(
                            text="謝謝您！若要登錄主動發訊息內容，請點按下方圖片選單；如果其他客服問題，請點選以下連結 https://***"
                        ))
                        return HttpResponse("")

                    elif re.findall(r".+@.+",mtext):
                        userid=str(event.source).split('"')[7]
                        time=str(event.timestamp)[0:10]
                        makesure=1
                        db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                        cursor=db.cursor()
                        db.autocommit(True)
                        sql_str="insert into email(userid, time, content, makesure) values(\"{}\",\"{}\",\"{}\",\"{}\")".format(userid, time, mtext,makesure)
                        cursor.execute(sql_str)
                        db.close()
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(
                            text="已收到您的e-mail，我們會盡快以e-mail方式連繫您，請留意***@gate.sinica.edu.tw的來信。萬一在三天內未收到我們電子信件的通知，請務必與我們連繫。"
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
                        messageQ00_event(event)
                        return HttpResponse("")

                elif isinstance(event.message, ImageMessage):
                    userid=str(event.source).split('"')[7]
                    time=str(event.timestamp)[0:10]
                    db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                    cursor=db.cursor()
                    db.autocommit(True)
                    sql_str="insert into forward(userid, time, content) values(\"{}\",\"{}\",\"圖片\")".format(userid, time)
                    cursor.execute(sql_str)
                    db.close()
                    messageQ00_event(event)
                    return HttpResponse("")

                elif isinstance(event.message, AudioMessage):
                    userid=str(event.source).split('"')[7]
                    time=str(event.timestamp)[0:10]
                    db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                    cursor=db.cursor()
                    db.autocommit(True)
                    sql_str="insert into forward(userid, time, content) values(\"{}\",\"{}\",\"聲音\")".format(userid, time)
                    cursor.execute(sql_str)
                    db.close()
                    messageQ00_event(event)
                    return HttpResponse("")

                elif isinstance(event.message, VideoMessage):
                    userid=str(event.source).split('"')[7]
                    time=str(event.timestamp)[0:10]
                    db=pymysql.connect(host="***", user="***", passwd="***", db="***")
                    cursor=db.cursor()
                    db.autocommit(True)
                    sql_str="insert into forward(userid, time, content) values(\"{}\",\"{}\",\"影片\")".format(userid, time)
                    cursor.execute(sql_str)
                    db.close()
                    messageQ00_event(event)
                    return HttpResponse("")

            else:
                return HttpResponse("")
    else:
        return HttpResponseBadRequest("")


def messageQ00_event(event):
    messageQ00=TemplateSendMessage(
        alt_text="Confirm templateQ00",
        template=ConfirmTemplate(
            text="您剛才轉傳了一則特別有感的訊息",
            actions=[
                MessageTemplateAction(label="是，開始登錄", text="00是，開始登錄"),
                MessageTemplateAction(label="不，不是", text="00不，不是")
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, messageQ00)

def messageQ01_event(event):
    question=BubbleContainer(
        size="micro",
        hero=ImageComponent(
            url="https://i.imgur.com/wf28JsJ.png",
            size="full", aspect_ratio="1:1", aspect_mode="cover"
        ),
        body=BoxComponent(
            layout="vertical",
            contents=[
                TextComponent(align="center", text="請右滑選擇答案")
            ]
        )
    )
    answer1=BubbleContainer(
        size="micro",
        hero=ImageComponent(
            url="https://i.imgur.com/lFbfxb4.jpg",
            size="full", aspect_ratio="1:1", aspect_mode="cover"
        ),
        footer=BoxComponent(
            layout="vertical",
            contents=[
                ButtonComponent(style="primary", action=MessageAction(label="按此選擇", text="01有用資訊"))
            ]
        )
    )
    answer2=BubbleContainer(
        size="micro",
        hero=ImageComponent(
            url="https://i.imgur.com/IOflINs.png",
            size="full", aspect_ratio="1:1", aspect_mode="cover"
        ),
        footer=BoxComponent(
            layout="vertical",
            contents=[
                ButtonComponent(style="primary", action=MessageAction(label="按此選擇", text="01有心情感受"))
            ]
        )
    )
    answer3=BubbleContainer(
        size="micro",
        hero=ImageComponent(
            url="https://i.imgur.com/GxKNQta.png",
            size="full", aspect_ratio="1:1", aspect_mode="cover"
        ),
        footer=BoxComponent(
            layout="vertical",
            contents=[
                ButtonComponent(style="primary", action=MessageAction(label="按此選擇", text="01有靈性啟發"))
            ]
        )
    )
    answer4=BubbleContainer(
        size="micro",
        hero=ImageComponent(
            url="https://i.imgur.com/6HJcznp.jpg",
            size="full", aspect_ratio="1:1", aspect_mode="cover"
        ),
        footer=BoxComponent(
            layout="vertical",
            contents=[
                ButtonComponent(style="primary", action=MessageAction(label="按此選擇", text="01有趣"))
            ]
        )
    )
    answer5=BubbleContainer(
        size="micro",
        hero=ImageComponent(
            url="https://i.imgur.com/VuuPxHE.jpg",
            size="full", aspect_ratio="1:1", aspect_mode="cover"
        ),
        footer=BoxComponent(
            layout="vertical",
            contents=[
                ButtonComponent(style="primary", action=MessageAction(label="按此選擇", text="01不認同"))
            ]
        )
    )
    carousel=CarouselContainer(contents=[question, answer1, answer2, answer3, answer4, answer5])
    message=FlexSendMessage(alt_text="FlexSendMessage Q01", contents=carousel)
    line_bot_api.reply_message(event.reply_token, message)

def messageQ02_event(event):
    question=BubbleContainer(
        size="micro",
        hero=ImageComponent(
            url="https://i.imgur.com/yXQBOEu.png",
            size="full", aspect_ratio="1:1", aspect_mode="cover"
        ),
        body=BoxComponent(
            layout="vertical",
            contents=[
                TextComponent(align="center", text="請右滑選擇答案")
            ]
        )
    )
    answer1=BubbleContainer(
        size="micro",
        hero=ImageComponent(
            url="https://i.imgur.com/pbczlfF.png",
            size="full", aspect_ratio="1:1", aspect_mode="cover"
        ),
        footer=BoxComponent(
            layout="vertical",
            contents=[
                ButtonComponent(style="primary", action=MessageAction(label="按此選擇", text="02有一點"))
            ]
        )
    )
    answer2=BubbleContainer(
        size="micro",
        hero=ImageComponent(
            url="https://i.imgur.com/YSfhCG3.png",
            size="full", aspect_ratio="1:1", aspect_mode="cover"
        ),
        footer=BoxComponent(
            layout="vertical",
            contents=[
                ButtonComponent(style="primary", action=MessageAction(label="按此選擇", text="02普通"))
            ]
        )
    )
    answer3=BubbleContainer(
        size="micro",
        hero=ImageComponent(
            url="https://i.imgur.com/FNETMRD.png",
            size="full", aspect_ratio="1:1", aspect_mode="cover"
        ),
        footer=BoxComponent(
            layout="vertical",
            contents=[
                ButtonComponent(style="primary", action=MessageAction(label="按此選擇", text="02非常"))
            ]
        )
    )
    carousel=CarouselContainer(contents=[question, answer1, answer2, answer3])
    message=FlexSendMessage(alt_text="FlexSendMessage Q02", contents=carousel)
    line_bot_api.reply_message(event.reply_token, message)

def messageQ02A_event(event):
    question=BubbleContainer(
        size="micro",
        hero=ImageComponent(
            url="https://i.imgur.com/yXQBOEu.png",
            size="full", aspect_ratio="1:1", aspect_mode="cover"
        ),
        body=BoxComponent(
            layout="vertical",
            contents=[
                TextComponent(align="center", text="請右滑選擇答案")
            ]
        )
    )
    answer1=BubbleContainer(
        size="micro",
        hero=ImageComponent(
            url="https://i.imgur.com/m3tZwhN.png",
            size="full", aspect_ratio="1:1", aspect_mode="cover"
        ),
        body=BoxComponent(
            layout="vertical",
            contents=[
                ButtonComponent(style="primary", action=MessageAction(label="按此選擇", text="02非常陰鬱低落"))
            ]
        )
    )
    answer2=BubbleContainer(
        size="micro",
        hero=ImageComponent(
            url="https://i.imgur.com/xG6nHEy.png",
            size="full", aspect_ratio="1:1", aspect_mode="cover"
        ),
        body=BoxComponent(
            layout="vertical",
            contents=[
                ButtonComponent(style="primary", action=MessageAction(label="按此選擇", text="02有點陰鬱低落"))
            ]
        )
    )
    answer3=BubbleContainer(
        size="micro",
        hero=ImageComponent(
            url="https://i.imgur.com/mBhYzMA.png",
            size="full", aspect_ratio="1:1", aspect_mode="cover"
        ),
        body=BoxComponent(
            layout="vertical",
            contents=[
                ButtonComponent(style="primary", action=MessageAction(label="按此選擇", text="02有點陽光正面"))
            ]
        )
    )
    answer4=BubbleContainer(
        size="micro",
        hero=ImageComponent(
            url="https://i.imgur.com/BSiqvur.png",
            size="full", aspect_ratio="1:1", aspect_mode="cover"
        ),
        body=BoxComponent(
            layout="vertical",
            contents=[
                ButtonComponent(style="primary", action=MessageAction(label="按此選擇", text="02非常陽光正面"))
            ]
        )
    )
    carousel=CarouselContainer(contents=[question, answer1, answer2, answer3, answer4])
    message=FlexSendMessage(alt_text="FlexSendMessage Q02A", contents=carousel)
    line_bot_api.reply_message(event.reply_token, message)

def messageQ03_event(event):
    messageQ03=TemplateSendMessage(
        alt_text="Confirm templateQ03",
        template=ConfirmTemplate(
            text="3.請問您有回覆該則訊息嗎？",
            actions=[
                MessageTemplateAction(label="有", text="03有"),
                MessageTemplateAction(label="無", text="03無")
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, messageQ04)

def messageQ04_event(event):
    messageQ04=TemplateSendMessage(
        alt_text="Confirm templateQ04",
        template=ConfirmTemplate(
            text="4.請問您是否有分享這個訊息給其他人？",
            actions=[
                MessageTemplateAction(label="有", text="04有"),
                MessageTemplateAction(label="無", text="04無")
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, messageQ04)

def messageQ10_event(event):
    messageQ10=TemplateSendMessage(
        alt_text="Confirm templateQ10",
        template=ButtonsTemplate(
            text="請問您在哪裡主動發文？",
            actions=[
                MessageTemplateAction(label="LINE", text="10LINE"),
                MessageTemplateAction(label="Facebook", text="10Facebook")
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, messageQ10)
