# memelinebot
## 設計動機
跟朋友傳送訊息時常會使用梗圖回覆，因此想設計一個LineBot，方便存取與搜索有趣的梗圖
## 架構簡介
進入主選單後可選取**查看梗圖庫**或**搜索網站[Meme梗圖倉庫]的熱門梗圖**
### 我的梗圖庫
**取得[梗圖名稱]**: "梗圖超人"會回傳該圖片，便可將梗圖存取或分享至其他聊天室  
**替換[梗圖名稱]**: 輸入新的梗圖的名稱，再傳送欲替換的梗圖  
### 查看網站[Meme梗圖倉庫]
先選擇想搜索的類別: 全部創作/校園生活/日常垃圾話/暈船仔請進  
運用BeautifulSoup4爬取該網頁取得當前熱門梗圖(五張)  
## 使用教學
1. install `pipenv`
```
pip3 install pipenv
```
2. install 所需套件
```
pip3 install -r requirements.txt
pip3 install BeautifulSoup4
```
3. install `ngrok`
```
sudo snap install ngrok
```
4. run `ngrok` to deploy Line Chat Bot locally
```
ngrok http 8000
```
5. execute app.py
```
python3 app.py
```
## 操作展示  
* 輸入主選單後開始使用  
![](https://i.imgur.com/RpTc72u.jpg)  
* 按下我的梗圖庫，查看梗圖庫  
![](https://i.imgur.com/Nfb2JKw.jpg)  
* 為梗圖命名，傳送欲替換的梗圖，回到主選單  
![](https://i.imgur.com/ooY7Wjl.jpg)
![](https://i.imgur.com/i6lY3hv.jpg)  
* 取得梗圖，輸入"主選單"返回主選單  
![](https://i.imgur.com/5nK0hYo.jpg)  
* 查看網站，選取類別，獲得該類前五熱門梗圖!  
![](https://i.imgur.com/QFO5aI1.jpg)  
 
* 若過程中輸入無效指令，"梗圖超人"將提醒您: 請輸入正確指令  
