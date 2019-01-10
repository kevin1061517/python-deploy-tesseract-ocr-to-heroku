#fang_test herokuapp
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from firebase import firebase
from linebot.models import (
    SourceUser,SourceGroup,SourceRoom,LeaveEvent,JoinEvent,
    TemplateSendMessage,PostbackEvent,AudioMessage,LocationMessage,
    ButtonsTemplate,LocationSendMessage,AudioSendMessage,ButtonsTemplate,
    ImageMessage,URITemplateAction,MessageTemplateAction,ConfirmTemplate,
    PostbackTemplateAction,ImageSendMessage,MessageEvent, TextMessage, 
    TextSendMessage,StickerMessage, StickerSendMessage,DatetimePickerTemplateAction,
    CarouselColumn,CarouselTemplate,VideoSendMessage,ImagemapSendMessage,BaseSize,
    URIImagemapAction,MessageImagemapAction,ImagemapArea,ImageCarouselColumn,ImageCarouselTemplate,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,URIAction,LocationAction,QuickReply,QuickReplyButton,
    DatetimePickerAction,PostbackAction,MessageAction,CameraAction,CameraRollAction
)
from imgurpython import ImgurClient
from config import *
import re
from bs4 import BeautifulSoup as bf
import requests
import random
import os,tempfile
from datetime import timedelta, datetime
from time import sleep
from urllib.parse import quote
from urllib import parse
app = Flask(__name__)
#imgur上傳照片
client_id = os.getenv('client_id',None)
client_secret = os.getenv('client_secret',None)
album_id = os.getenv('album_id',None)
access_token = os.getenv('access_token',None)
refresh_token = os.getenv('refresh_token',None)
client = ImgurClient(client_id, client_secret, access_token, refresh_token)
url = os.getenv('firebase_bot',None)
fb = firebase.FirebaseApplication(url,None)
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN',None))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET', None))

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body,signature)
    except LineBotApiError as e:
        print("Catch exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("ERROR is %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def get_total_flex(body_content,footer_content=[ButtonComponent(style='link',action=URIAction(label='My github', uri='https://github.com/kevin1061517?tab=repositories'))]):
    bubble = BubbleContainer(
#            header=BoxComponent(
#                layout='vertical',
#                contents=header_content#---->這樣子也行 contents=[t[0],t[1]]
#            ),
            body=BoxComponent(
                layout='vertical',
                contents=body_content
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents= footer_content
            )
        )
    return bubble

def look_up(tex):
    content = ''
    target_url = 'https://tw.dictionary.search.yahoo.com/search;_ylt=AwrtXG86cTRcUGoAESt9rolQ?p={}&fr2=sb-top'.format(tex)
    res =  requests.get(target_url)
    soup = bf(res.text,'html.parser')
    try:
        content += '{}\n'.format(soup.select('.lh-22.mh-22.mt-12.mb-12.mr-25.last')[0].text)
        for i in soup.select('.layoutCenter .lh-22.mh-22.ml-50.mt-12.mb-12'):
            if i.select('p  span') != []:   
                content += '{}\n{}\n'.format(i.select('.fz-14')[0].text,i.select('p  span')[0].text)
            else:
                content += '{}\n'.format(i.select('.fz-14')[0].text)
        if content == '':
            for i in soup.select('.layoutCenter .ml-50.mt-5.last'):
                content += i.text
    except IndexError:
        content = '查無此字'
    return content


def integer_word(word):
    content = look_up(word)
    if content != '查無此字':
        content = [TextComponent(text='🔍英文單字查詢',weight='bold', align='center',size='md',wrap=True,color='#000000'),SeparatorComponent(margin='lg'),TextComponent(text=content, size='sm',wrap=True,color='#000000')]
        audio_button = [
                    SeparatorComponent(),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=PostbackAction(label='📢 美式發音', data='audio/{}'.format(word))
                    )
                    ]
        bubble = get_total_flex(content,audio_button)
        message = FlexSendMessage(alt_text="hello", contents=bubble)
    else:
        message = TextSendMessage(text=content)
    return message
def template_img(path):
            print('temp---------'+str(path))
            buttons_template = TemplateSendMessage(
            alt_text='news template',
            template=ButtonsTemplate(
                title='你傳來的是照片喔',
                text='請選擇怎樣處理',
                thumbnail_image_url='https://i.imgur.com/GoAYFqv.jpg',
                actions=[
                    PostbackTemplateAction(
                        label='影像文字翻譯辨識',
                        text='請稍等....',
                        data = 'trans/{}'.format(path)
                    ),
                    PostbackTemplateAction(
                        label='影像儲存至相簿',
                        text='請稍等....',
                        data = 'image/{}'.format(path)
                    )
                ]
            )
            )
            return buttons_template
@handler.add(PostbackEvent)
def handle_postback(event):
    temp = event.postback.data
    s = ''
    if temp[:5] == 'image':
     print('------postback'+str(temp))
     t = temp.split('/')
     path = '/{}/{}'.format(t[2],t[3])
     print('postback---------'+str(path))
     img_id = 1
     t = fb.get('/pic',None)
     if t!=None:
         count = 1
         for key,value in t.items():
            if count == len(t):#取得最後一個dict項目
                img_id = int(value['id'])+1
            count+=1
     try:

        client = ImgurClient(client_id, client_secret, access_token, refresh_token)
        config = {
            'album': album_id,
            'name' : img_id,
            'title': img_id,
            'description': 'Cute kitten being cute on'
        }
        client.upload_from_path(path, config=config, anon=False)
        os.remove(path)
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text='上傳成功'),image_reply])
     except  Exception as e:
        t = '上傳失敗'+str(e.args)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=t))
    elif temp[:5] == 'trans':
     t = temp.split('/')
     path = '/{}/{}'.format(t[2],t[3])
     print('postback----'+str(path)) 
     pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
     image = Image.open(path)
     t = pytesseract.image_to_string(image)
     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=t))

# 處理圖片
@handler.add(MessageEvent,message=ImageMessage)
def handle_msg_img(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(prefix='jpg-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name
    path = tempfile_path

    buttons_template = template_img(path)
    line_bot_api.reply_message(event.reply_token,buttons_template)

# 處理訊息:
@handler.add(MessageEvent, message=TextMessage)
def handle_msg_text(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name
    picture_url = profile.picture_url
    if re.search(r'eng$',event.message.text.lower())!=None:
        keyword = event.message.text.lower()[:-3]
        keyword = keyword.replace(' ','')
        print('-----------'+keyword)
        message = integer_word(keyword)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )

















