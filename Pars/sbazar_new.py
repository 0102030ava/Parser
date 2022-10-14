from ast import ExtSlice
import json
from platform import release
from bs4 import BeautifulSoup
import requests 
import lxml
import telebot
import sys
import os 
import json
import time
import random
import re
from datetime import date
from fake_useragent import UserAgent
from urllib.request import urlopen
sys.path.insert(1,os.path.join(sys.path[0],'..'))
from Bot import Information
from Bot import Button

from requests.auth import HTTPProxyAuth
import datetime


bot = telebot.TeleBot(Information.token)  
def sbazar_pars(link,id,arr_stop,text,active_use_pars,user_reg,text2):
   gen_link = link
   used_phones = []
   price_f = 1
   price_t = 1000000
   current_page = 1
   all_page = 5
   category_id = link.split("https://www.sbazar.cz/")[1].split("-")[0]
   ua = UserAgent()
   f = open('http.txt', 'r')
   l = [line.strip() for line in f] 
   random.shuffle(l)
   proxies = {"http":f"{':'.join(l[0].split(':')[:-2])}"}
   auth = HTTPProxyAuth(f"{l[0].split(':')[-2:][0]}", f"{l[0].split(':')[-2:][1]}")         
   response = requests.get(link, headers={'User-Agent': f'{ua.random}'}, proxies=proxies, auth=auth) # Загружаем главную страницу для получения cookies
   x = response.cookies.get('_sbazar_sessoin') # Сохраняем в переменную x cookie с именем _vinted_fr_session
   if "hledej" not in gen_link:
      headers = {
         'authority': 'www.sbazar.cz',
         'accept': 'application/json',
         'accept-language': 'cs',
         'dnt': '1',
         'referer': 'https://www.sbazar.cz/29-detsky-bazar/cela-cr/cena-neomezena/nejnovejsi/2',
         'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
         'sec-ch-ua-mobile': '?0',
         'sec-ch-ua-platform': '"Windows"',
         'sec-fetch-dest': 'empty',
         'sec-fetch-mode': 'cors',
         'sec-fetch-site': 'same-origin',
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
      }

      params = {
         'offset': '36',
         'price_from' : f'{price_f}',
         'price_to': f'{price_t}',
         'category_id': f'{category_id}',
         'limit': '300',
         'timestamp_to': int(time.time()),
      }
   else:
      phrase = link.split("hledej/")[1]
      headers = {
         'authority': 'www.sbazar.cz',
         'accept': 'application/json',
         'accept-language': 'cs',
         # Requests sorts cookies= alphabetically
         # 'cookie': '__gfps_64b=wTxx5cYRH32Za8SmUftUloOoVfuhfIHn2XyX0.Tiav3.F7|1661525225; szncmpone=1; appver=v0.4.123; __gfp_64b=Y_S2rrPzGnQkpz6Z1pxsnQ0ehL9NbwjCucs.Zb7AIsP.V7|1661525251; sid=id=3763449858916890592|t=1661525251.745|te=1662622327.825|c=6138B0CAAA89DCDB5A5B6AC5ED99EFE4; __gsync_gdpr=1:YTU6bjpuOjE2NjI2MjIzMjc3OTY6MTY2MjYyMjMyNzc5Njpu; euconsent-v2=CPeUIIAPeUIIAD3ACBCSCfCsAP_AAEPAAATIIDoBhCokBSFCAGpYIIMAAAAHxxAAYCACABAAgAABABIAIAQAAAAQAAQgBAAAABQAIAIAAAAACEAAAAAAAAAAAQAAAAAAAAAAIQIAAAAAAiBAAAAAAABAAAAAAABAQAAAgAAAAAIAQAAAAAEAgAAAAAAAAAAAAAAAAQgAAAAAAAAAAAganAmAAWABUAC4AGQAQAAyABoADmAIgAigBMACeAFUAMQAfgBCQCIAIkARwAnABSgCxAGWAM0AdwA_QCEAEWALQAXUAwIBrAD5AJBATaAtQBeYDJAGlANTAAAA.YAAAAAAAAAAA; __gsync=1:YTU6NDk6MTY2MTUzMDc2MTMxNDoxMDoxNjYxNTI1MjI0NTI1OmExMDphMjoxMDE6NTUzNjc4NzphMjoxMDI6MzA5MzQ6YTI6MTA3OjU1MzY3ODk6YTI6MTA5OjQyNjg6YTI6MTEwOjA6YTI6MTEyOjU1MzY3ODg6YTI6MTEzOjQyNjk6YTI6MTE0OjQyNjg6YTI6MTE3OjU1MzY3ODg6YTI6MTE4OjU1MzY3ODk_; lps=eyJfZnJlc2giOmZhbHNlLCJfcGVybWFuZW50Ijp0cnVlfQ.YxoAMw.94zKokC4_0zSXnno_TkopcFmmWA; szncsr=1662648377',
         'dnt': '1',
         'referer': 'https://www.sbazar.cz/hledej/iphone%2011/0-vsechny-kategorie/cela-cr/cena-neomezena/nejnovejsi/2',
         'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
         'sec-ch-ua-mobile': '?0',
         'sec-ch-ua-platform': '"Windows"',
         'sec-fetch-dest': 'empty',
         'sec-fetch-mode': 'cors',
         'sec-fetch-site': 'same-origin',
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
      }

      params = {
         'offset': '36',
         'phrase': f'{phrase.replace("%20"," ")}',
         'limit': '500',
         'timestamp_to': int(time.time()),
      }      

   response = requests.get('https://www.sbazar.cz/api/v1/items/search', params=params, headers=headers, proxies=proxies, auth=auth).json()
   try:
      items = response.get("results")
      with open('result_{}.json'.format(id),'w', encoding="utf-8") as file:
            json.dump(items,file,indent=4,ensure_ascii=False)
      print(len(items))
      for item in items:
               if arr_stop[id] == "False":
                  current_page = 100
                  break
               else:     
                  
                  curent_time = item.get("edit_date")
                  year = str(curent_time).split('T')[0].split('-')[0]
                  mos = str(curent_time).split('T')[0].split('-')[1]
                  day = str(curent_time).split('T')[0].split('-')[2]

                  year_c = str(date.today()).split('-')[0]
                  mos_c = str(date.today()).split('-')[1]
                  day_c = str(date.today()).split('-')[2]
                  print(day_c)
                  if year == year_c and mos == mos_c:
                      if abs(int(day_c)-int(day)) <= 1:
                        title = item.get("name")
                        price = str(item.get("price")) + " Kč"
                        link = "https://www.sbazar.cz/"+item.get("user").get("user_service").get("shop_url")+"/detail/"+item.get("seo_name")
                        current_ad_ = requests.get(link)
                        soup = BeautifulSoup(current_ad_.text , 'lxml')#сonnect to  link
                        try:
                           phone = str(soup.find(class_ = "atm-link c-atm-phone c-seller-card__contact-phone").get('href')).split("+")[1] # find phone
                           #find phone
                           response = urlopen("https:"+soup.find(class_ = "ob-c-gallery__img").get('src'))
                           content = response.read()
                           file = open('photo_'+str(id)+'.png', 'wb')
                           file.write(content)
                           file.close()               
                           
                           price_ad = soup.find(class_ = "c-price__price").text+" Kč"  # find price ad
                           if price_ad.split(" ")[0] == "Dohodou":
                              price_ad = "Договорная"
                           
                           location_ad = soup.find(class_ = "p-uw-item__link").text # find location ad
                           regestration_user = "Зарегистрирован в "+str(soup.find(class_ = "c-seller-info__date").text).split(" ")[-1] # find reg. user
                           nick_user = soup.find(class_ = "c-seller-info__name c-seller-info__name--link").text # find nick user
                           if phone not in used_phones and int(regestration_user.split(" ")[-1]) >= int(user_reg) :
                              used_phones.append(phone)
                              
                              bot.send_photo(id,open("photo_{}.png".format(id), 'rb'),"<b>⛓ Название товара</b> : {}\n\n<b>💵 Цена товарa</b> : {}\n<b>📍 Дата выложения товара</b> : {}\n<b>🏢 Город</b> : {}\n<b>📱 Номер телефона</b> : {}\n<b>👤 Ник пользователя</b> : {}\n<b>🕛 Дата регист. аккаунта</b> : {}\n\n<b>🔗 Ссылка на товар</b> : <a href='{}'> Ссылочка</a>".format(title,price_ad,curent_time.replace("T",", "),location_ad,phone,nick_user,regestration_user,link) ,parse_mode='HTML' , reply_markup=Button.but_for_phone(phone,text,link,text2,title.replace(" ","+")))
                        except Exception as E:
                           pass  
   except Exception as E:
      pass
   if arr_stop[id] != "False":
      try:
         bot.send_message(id,"<b>✅ Парс по ссылке: {} \nЗакончился</b>".format(gen_link), reply_markup=Button.menu_users_telebot ,parse_mode='HTML')
         active_use_pars.remove(id)
      except:
         pass
      try:    
         os.remove("photo_{}.png".format(id))  
      except:
         pass

