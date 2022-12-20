import os
import globalvar
from transitions.extensions import GraphMachine

from utils import send_text_message,send_button_message,send_button_carousel,send_image_message,uploadingpic,searchmeme,listName,listPicUrl
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction

OnpicX = 0


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_start(self, event):
        text = event.message.text
        return text == "主選單"

    def is_going_to_mypic(self, event):
        text = event.message.text
        return text == "我的梗圖庫"
    def is_going_to_search(self, event):
        text = event.message.text
        return text == "查看網站[Meme梗圖倉庫]"

    def is_going_to_searchingname(self, event):
        text = event.message.text
        match text:
            case '全部創作':
                globalvar.set("webtype", 0)
                ok = True
            case '校園生活':
                globalvar.set("webtype", 1)
                ok = True
            case '日常垃圾話':
                globalvar.set("webtype", 2)
                ok = True
            case '暈船仔請進':
                globalvar.set("webtype", 3)
                ok = True
            case _:
                ok = False
        return ok

    def is_going_to_getpic(self, event):
        global OnpicX
        text = event.message.text
        match text:
            case '取得梗圖1':
                OnpicX = 0
                ok = True
            case '取得梗圖2':
                OnpicX = 1
                ok = True
            case '取得梗圖3':
                OnpicX = 2
                ok = True
            case '取得梗圖4':
                OnpicX = 3
                ok = True
            case '取得梗圖5':
                OnpicX = 4
                ok = True
            case _:
                ok = False
        return ok


    def is_going_to_picname(self, event):
        global OnpicX
        text = event.message.text
        match text:
            case '替換梗圖1':
                OnpicX = 0
                ok = True
            case '替換梗圖2':
                OnpicX = 1
                ok = True
            case '替換梗圖3':
                OnpicX = 2
                ok = True
            case '替換梗圖4':
                OnpicX = 3
                ok = True
            case '替換梗圖5':
                OnpicX = 4
                ok = True
            case _:
                ok = False
        return ok

    def is_going_to_changepic(self, event):
        if (event.message.type == "text"):
            globalvar.set("mode", 1)
            text = event.message.text
            listName[OnpicX] = text
            print(globalvar.get("mode"))
            print("going to enter changepic")
            return True

    def is_going_to_savepic(self, event):
        print("enter savepic")
        if ( event.message.type == "image" ):
            listPicUrl[OnpicX] = uploadingpic(event)
            globalvar.set("mode", 0)
            print(globalvar.get("mode"))
            print(listPicUrl[OnpicX])
            return True
        else:
            print("need pic")
            return False

    def on_enter_start(self, event):
        if globalvar.get("enterstart") == 0:
            title = '你可以~'
            text = '選擇以下功能ﾚ(ﾟ∀ﾟ)ﾍ'
            btn = [
                MessageTemplateAction(
                    label='我的梗圖庫',
                    text='我的梗圖庫'
                ),
                MessageTemplateAction(
                    label='查看網站[Meme梗圖倉庫]',
                    text='查看網站[Meme梗圖倉庫]'
                )
            ]
            url = 'https://i.imgur.com/KIudu08.jpeg'
            send_button_message(event.reply_token, title, text, btn, url)
        else:
            globalvar.set("enterstart", 0)
        return "OK"

    def on_enter_mypic(self, event):
        send_button_carousel(event.reply_token)
        return "OK"

    def on_enter_search(self, event):
        title = '你可以~'
        text = '選擇以下類別ﾚ(ﾟ∀ﾟ)ﾍ'
        btn = [
            MessageTemplateAction(
                label='全部創作',
                text='全部創作'
            ),
            MessageTemplateAction(
                label='校園生活',
                text='校園生活'
            ),
            MessageTemplateAction(
                label='日常垃圾話',
                text='日常垃圾話'
            ),
            MessageTemplateAction(
                label='暈船仔請進',
                text='暈船仔請進'
            )
        ]
        url = 'https://i.imgur.com/4ZbFbU6.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
        return "OK"

    def on_enter_searchingname(self, event):
        searchmeme(event, globalvar.get("webtype"))
        return "OK"


    def on_enter_getpic(self, event):
        global OnpicX
        send_image_message(event.reply_token, listPicUrl[OnpicX])

    def on_enter_picname(self, event):
        send_text_message(event.reply_token, '請輸入梗圖名稱')
        return "OK"

    def on_enter_changepic(self, event):
        send_text_message(event.reply_token, '請傳送想要替換的梗圖')
        return "OK"

    def on_enter_savepic(self, event):
        globalvar.set("enterstart", 1)
        title = '梗圖已儲存!你回到了主選單~'
        text = '選擇以下功能ﾚ(ﾟ∀ﾟ)ﾍ'
        btn = [
            MessageTemplateAction(
                label='我的梗圖庫',
                text='我的梗圖庫'
            ),
            MessageTemplateAction(
                label='查看網站[Meme梗圖倉庫]',
                text='查看網站[Meme梗圖倉庫]'
            )
        ]
        url = 'https://i.imgur.com/KIudu08.jpeg'
        send_button_message(event.reply_token, title, text, btn, url)
        self.go_back(event)





