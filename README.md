deploy Tesseract-OCR to Heroku(Linebot)
==== 

Descript
-------

Because I have stuck on the this question for two days,I take some notes to remind me of deeploying the Tesseract-OCR to Heroku.First, Tesseract is an OCR sponsored by Google. It is open-source and its binaries are available for lots of platforms, Additionally, it is a popular go-to library when OCR functionalities are required in an app. Setting up Tesseract-OCR is a procedure in popular development environments such as Heroku.Most of all,the following article is the process of deploying and coding.

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

Focus on the path!!!->'/app/.apt/usr/bin/tesseract'
-------

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
You must create the file named as Aptfile,or the error will emerge.
![](https://i.imgur.com/dAfw6XC.jpg"step2")

3.set a heroku config variable named TESSDATA_PREFIX. This is the path to the data downloaded by the tesseract-ocr-eng package.
-------
You can use the command following:

```
heroku config:set TESSDATA_PREFIX=/app/.apt/usr/share/tesseract-ocr/tessdata
```
or you can input the TESSDATA_PREFIX=/app/.apt/usr/share/tesseract-ocr/tessdata by using Graphical interface on heroku
![](https://i.imgur.com/SrYlCC8.jpg"step3")

Notes
====

1.I got errors when I paste the tesseract-ocr into the requirements.txt file.Because I used to add buildpack,I always need to key my       required module.But in this case,never use the requirements.txt.

2.You must set a heroku config variable named TESSDATA_PREFIX,and inputing the TESSDATA_PREFIX's path.
  <br>the error image of ignoring the configuration of variable named TESSDATA_PREFIX
![](https://i.imgur.com/lIPGDWN.jpg"step3")

LINEBOT Display
====
![](https://i.imgur.com/ZNbwTGP.jpg"LINEBOT")

Reference
====
https://stackoverflow.com/questions/42370732/heroku-error-opening-data-file-app-vendor-tesseract-ocr-tessdata-eng-traineddat
https://github.com/heroku/heroku-buildpack-apt
https://medium.com/@pro_science108/configurin-tesseract-ocr-in-heroku-16-444a4c079c41



















