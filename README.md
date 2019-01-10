deploy Tesseract-OCR to Heroku(Linebot)
==== 
Code
-------
```python
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
image = Image.open(path)
t = pytesseract.image_to_string(image)
line_bot_api.reply_message(event.reply_token,TextSendMessage(text=t))'''


