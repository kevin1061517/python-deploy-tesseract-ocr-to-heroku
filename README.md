Deploy Tesseract-OCR to Heroku(Linebot)
==== 

Descript
-------

Because I have stuck on the this question for two days, I take some notes to remind me of deeploying the Tesseract-OCR to Heroku. First, Tesseract is an OCR sponsored by Google. It is open-source and its binaries are available for lots of platforms, Additionally, it is a popular go-to library when OCR functionalities are required in an app. Setting up Tesseract-OCR is a procedure in popular development environments such as Heroku.Most of all, the following article is the process of deploying and coding.

Python Code
-------

```python
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
image = Image.open(path)
t = pytesseract.image_to_string(image)
line_bot_api.reply_message(event.reply_token,TextSendMessage(text=t))
```

**Focus on the path!!! -> '/app/.apt/usr/bin/tesseract'**

step
==== 

1.Add heroku-apt-buildpack into buildpacks on heroku:
-------
You can use the command following:
```
heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt
```
or you can input the https://github.com/heroku/heroku-buildpack-apt by using Graphical interface on heroku
![](https://i.imgur.com/GNJGqWt.jpg"step3")



2.Create a file named as Aptfile in your app directory and paste the following:
-------
```
tesseract-ocr
tesseract-ocr-eng
```
You must create the file named as Aptfile, or the error will emerge.
![](https://i.imgur.com/dAfw6XC.jpg"step2")

3.set a heroku config variable named TESSDATA_PREFIX. This is the path to the data downloaded by the tesseract-ocr-eng package.
-------
You can use the command following:

```
heroku config:set TESSDATA_PREFIX=/app/.apt/usr/share/tesseract-ocr/4.00/tessdata
```
or you can input the TESSDATA_PREFIX=/app/.apt/usr/share/tesseract-ocr/4.00/tessdata by using Graphical interface on heroku
![](https://i.imgur.com/SrYlCC8.jpg"step3")

Notes
====

1.I got errors when I paste the tesseract-ocr into the requirements.txt.Because 

* I used to add buildpack on heroku, I always need to input my required module into requirements.txt. But in this case,you never need the requirements.txt.
      
2.You must set a heroku config variable named TESSDATA_PREFIX, and inputing the TESSDATA_PREFIX's path.

* the error image of ignoring the configuration of variable named TESSDATA_PREFIX
      
![](https://i.imgur.com/lIPGDWN.jpg"variable")
3.Most of all,how can I find the main file named tesseract on heroku.

* First I would execuate the cmd command on heroku CLI and perform certain commands in the following commands.I should step into bash in order to find the path of tesseract on heroku bash.

```
heroku run bash
which tesseract
.......
```

![](https://i.imgur.com/l8YbsmS.jpg "heroku bash")

* Focus on fourth line

LINEBOT screenshop
====
![](https://i.imgur.com/RkQOeih.jpg"LINEBOT")

Code
====

```
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

#process image
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
```    
    
Reference
====
https://stackoverflow.com/questions/42370732/heroku-error-opening-data-file-app-vendor-tesseract-ocr-tessdata-eng-traineddat
<br>https://github.com/heroku/heroku-buildpack-apt
<br>https://medium.com/@pro_science108/configurin-tesseract-ocr-in-heroku-16-444a4c079c41


