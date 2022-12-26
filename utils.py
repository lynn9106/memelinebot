import os
import requests
import re
from bs4 import BeautifulSoup
import pyimgur
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ImageCarouselColumn, ImageCarouselTemplate, ButtonsTemplate, MessageTemplateAction, URITemplateAction, ImageSendMessage, CarouselTemplate, CarouselColumn
listName = ["Emtpy1", "Empty2", "Empty3", "Empty4", "Empty5"]
listPicUrl = ["https://i.imgur.com/5gGbzht.jpg",
              "https://i.imgur.com/5gGbzht.jpg",
              "https://i.imgur.com/5gGbzht.jpg",
              "https://i.imgur.com/5gGbzht.jpg",
              "https://i.imgur.com/5gGbzht.jpg"]

memeurl_list = ["https://memes.tw/wtf", "https://memes.tw/wtf?contest=11",
                "https://memes.tw/wtf?contest=6", "https://memes.tw/wtf?contest=3106"]

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
YOUTUBE_API_KEY = "AIzaSyBVOrQgfote9RtizxMfg_x2m3P6xjp9dJY"


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))
    return "OK"


def send_button_message(reply_token, title, text, btn, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='button template',
        template=ButtonsTemplate(
            title=title,
            text=text,
            thumbnail_image_url=url,
            actions=btn
        )
    )
    line_bot_api.reply_message(reply_token, message)
    return "OK"


def send_button_carousel(reply_token):
    global listName
    global listPicUrl

    line_bot_api = LineBotApi(channel_access_token)

    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=listPicUrl[0],
                    title=listName[0],
                    text='梗圖1',
                    actions=[
                        MessageTemplateAction(
                            label='取得['+listName[0]+']',
                            text='取得梗圖1'
                        ),
                        MessageTemplateAction(
                            label='替換['+listName[0]+']',
                            text='替換梗圖1'
                        ),
                        MessageTemplateAction(
                            label='返回主選單',
                            text='主選單'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=listPicUrl[1],
                    title=listName[1],
                    text='梗圖2',
                    actions=[
                        MessageTemplateAction(
                            label='取得[' + listName[1] + ']',
                            text='取得梗圖2'
                        ),
                        MessageTemplateAction(
                            label='替換[' + listName[1] + ']',
                            text='替換梗圖2'
                        ),
                        MessageTemplateAction(
                            label='返回主選單',
                            text='主選單'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=listPicUrl[2],
                    title=listName[2],
                    text='梗圖3',
                    actions=[
                        MessageTemplateAction(
                            label='取得[' + listName[2] + ']',
                            text='取得梗圖3'
                        ),
                        MessageTemplateAction(
                            label='替換[' + listName[2] + ']',
                            text='替換梗圖3'
                        ),
                        MessageTemplateAction(
                            label='返回主選單',
                            text='主選單'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=listPicUrl[3],
                    title=listName[3],
                    text='梗圖4',
                    actions=[
                        MessageTemplateAction(
                            label='取得[' + listName[3] + ']',
                            text='取得梗圖4'
                        ),
                        MessageTemplateAction(
                            label='替換[' + listName[3] + ']',
                            text='替換梗圖4'
                        ),
                        MessageTemplateAction(
                            label='返回主選單',
                            text='主選單'
                        )

                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=listPicUrl[4],
                    title=listName[4],
                    text='梗圖5',
                    actions=[
                        MessageTemplateAction(
                            label='取得[' + listName[4] + ']',
                            text='取得梗圖5'
                        ),
                        MessageTemplateAction(
                            label='替換[' + listName[4] + ']',
                            text='替換梗圖5'
                        ),
                        MessageTemplateAction(
                            label='返回主選單',
                            text='主選單'
                        )
                    ]
                )

            ]
        )
    )
    line_bot_api.reply_message(reply_token, carousel_template_message)


def send_image_message(reply_token, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
    )
    line_bot_api.reply_message(reply_token, message)


def uploadingpic(event):
    line_bot_api = LineBotApi(channel_access_token)
    SendImage = line_bot_api.get_message_content(event.message.id)
    local_save = './img/' + event.message.id + '.png'
    with open(local_save, 'wb') as fd:
        for chenk in SendImage.iter_content():
            fd.write(chenk)
    url = glucose_graph('1044fa0c6494e8c', local_save)
    return url


def glucose_graph(client_id, imgpath):
    im = pyimgur.Imgur(client_id)
    upload_image = im.upload_image(imgpath, title="Uploaded with PyImgur")
    return upload_image.link


def searchmeme(event, webtype):
    print("in search")
    myurl_list = []
    mypic_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    url = memeurl_list[webtype]
    r = requests.get(url, headers=headers)
    print(r.status_code)
    soup = BeautifulSoup(r.text, "html.parser")
    pics = soup.find_all(class_=re.compile("^sensitive-content"))
    for index, pic in enumerate(pics):
        if index < 5:
            pic_a = pic.select_one("a")
            pic_href = pic_a.get('href')
            myurl_list.append('https://memes.tw' + pic_href)
            pic_img = pic_a.select_one("img")
            mypic_list.append(pic_img['data-src'])

    col = []
    for i in range(5):
        c = ImageCarouselColumn(
            image_url=mypic_list[i],
            action=URITemplateAction(
                label='點我進入網站',
                uri=myurl_list[i]
            )
        )
        col.append(c)

    send_carousel_message(event.reply_token, col)


def send_carousel_message(reply_token, col):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='Carousel template',
        template=ImageCarouselTemplate(columns=col)
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"
