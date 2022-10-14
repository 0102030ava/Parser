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
from fake_useragent import UserAgent
from urllib.request import urlopen
sys.path.insert(1,os.path.join(sys.path[0],'..'))
from Bot import Information
from Bot import Button
from requests.auth import HTTPProxyAuth
#,id,arr_stop,active_use_pars,obv,pros
bot = telebot.TeleBot(Information.token)  
def vinted_it_pars(link,id,arr_stop,obv,pros,active_use_pars):
   current_page = 1
   all_page = 20 # all page
   gen_link = link
   user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
   #  PARS

   def find_current_catalog_id(link):
      ua = UserAgent()
      f = open('http.txt', 'r')
      l = [line.strip() for line in f] 
      random.shuffle(l)
      proxies = {"http":f"{':'.join(l[0].split(':')[:-2])}"}
      auth = HTTPProxyAuth(f"{l[0].split(':')[-2:][0]}", f"{l[0].split(':')[-2:][1]}")       
      connect = requests.get(link, headers={'user-agent': f'{ua.random}'}, proxies=proxies, auth=auth)
      soup = BeautifulSoup(connect.text , 'lxml')#connect to site    
      token = str(soup.find_all('meta')[-4]).split('content="')[1].split('"')[0]
      session = connect.text.split('"session_id":"')[1].split('","country"')[0]    
      if "catalog[]=" not in link and "search_text" not in link:
         try:
            catalog_id = str(soup.find('link',rel='alternative').get('href')).split('catalog_id=')[1]
         except:
            try:
               catalog_id = re.findall(r'\d{2,}',link)
            except:
               pass
      
      else:
         try:
            catalog_id = str(link).split("catalog[]=")[1].split("&")[0]
   
         except:
            try:
               catalog_id = str(link).split("catalog[]=")[1]
            except:
               catalog_id = None
               pass
 
      return catalog_id,token,session


   answer = find_current_catalog_id(link)
   catalog_id,token,session = answer[0],answer[1],answer[2]
   def returns_arr_information(catalog_id,current_page,token,session):
      try:
         text = gen_link.split("search_text=")[1].split('&')[0]
      except:
         pass
      ua = UserAgent()
      f = open('http.txt', 'r')
      l = [line.strip() for line in f] 
      random.shuffle(l)
      proxies = {"http":f"{':'.join(l[0].split(':')[:-2])}"}
      auth = HTTPProxyAuth(f"{l[0].split(':')[-2:][0]}", f"{l[0].split(':')[-2:][1]}")         
      response = requests.get(link, headers={'User-Agent': user_agent}, proxies=proxies, auth=auth) # Загружаем главную страницу для получения cookies
      x = response.cookies.get('_vinted_fr_session') # Сохраняем в переменную x cookie с именем _vinted_fr_session
      if "search_text" not in gen_link:
         headers = {
            'authority': 'www.vinted.it',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'it-fr',
            'dnt': '1',
            'referer': 'https://www.vinted.it/vetements?catalog[]='+str(catalog_id)+'&page='+str(current_page),
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent':  f'{ua.random}' ,
            'x-csrf-token': token,
               }

         params = {
         'catalog_ids': catalog_id,
         'color_ids': '',
         'brand_ids': '',
         'size_ids': '',
         'material_ids': '',
         'video_game_rating_ids': '',
         'status_ids': '',
         'is_for_swap': '0',
         'page': current_page,
         'per_page': '50',
         #'time': '1662159750',
         'search_session_id': session,
                  }
      else:
         headers = {
            'authority': 'www.vinted.it',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'it-fr',           
            'dnt': '1',
            'referer': 'https://www.vinted.it/vetements?search_text=head&currency=EUR&search_id=6350979173&order=newest_first&time=1662612074&page=2',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': f'{ua.random}',
            'x-csrf-token': token,
         }

         params = {
            'search_text': text,
            'catalog_ids': '',
            'currency': 'EUR',
            'color_ids': '',
            'brand_ids': '',
            'size_ids': '',
            'material_ids': '',
            'video_game_rating_ids': '',
            'status_ids': '',
            'is_for_swap': '0',
            'order': 'newest_first',
            'page': current_page,
            'per_page': '24',
            'time': '1662612074',
            'search_session_id': session,
         }

  
      f = open('http.txt', 'r')
      l = [line.strip() for line in f] 
      random.shuffle(l)
      proxies = {"http":f"{':'.join(l[0].split(':')[:-2])}"}
      auth = HTTPProxyAuth(f"{l[0].split(':')[-2:][0]}", f"{l[0].split(':')[-2:][1]}")         
      if  "search_text" in gen_link:
         response = requests.get('https://www.vinted.it/api/v2/catalog/items', params=params, cookies={'_vinted_fr_session':x}, headers=headers).json()
      else:
         response = requests.get('https://www.vinted.it/api/v2/catalog/items', params=params, cookies={'_vinted_fr_session':x} , headers=headers, proxies=proxies, auth=auth).json()  
         
      if catalog_id == [] and "search_text" not in gen_link:
         response = requests.get('https://www.vinted.it/api/v2/catalog/items?catalog_ids=&color_ids=&brand_ids=&size_ids=&material_ids=&video_game_rating_ids=&status_ids=&is_for_swap=0&page={}&per_page=24&time=1662610671&search_session_id=62e41994-fbd4-4f54-ab9a-7dc591e9c59c'.format(current_page) ,headers={'User-Agent': user_agent}, cookies={'_vinted_fr_session':x}, proxies=proxies, auth=auth).json() 
      items = response.get("items")
      with open('result_{}.json'.format(id),'w', encoding="utf-8") as file:
         json.dump(items,file,indent=4,ensure_ascii=False)
      return items


   arr_items = returns_arr_information(catalog_id,current_page,token,session)
   while current_page <= all_page:
      try:
         for item in arr_items:
            if arr_stop[id] == "False":
               current_page = 100
               break
            else:         
               name_ad = item.get("title")
               name_seller = item.get('user').get('login')
               price_ad = item.get("price")+" €"
               link_to_ad = item.get('url')
               link_to_user = item.get('user').get('profile_url')
               #get photo
               response = urlopen(item.get('photo').get('url'))
               content = response.read()
               file = open('photo_'+str(id)+'.png', 'wb')
               file.write(content)
               file.close()      
               #
               # time.sleep(random.randint(2,3))
               ua = UserAgent()
               f = open('http.txt', 'r')
               l = [line.strip() for line in f] 
               random.shuffle(l)
               proxies = {"http":f"{':'.join(l[0].split(':')[:-2])}"}
               auth = HTTPProxyAuth(f"{l[0].split(':')[-2:][0]}", f"{l[0].split(':')[-2:][1]}") 

               link_ad = requests.get(link_to_ad, headers={'user-agent': f'{ua.random}'}, proxies=proxies, auth=auth)
               soup = BeautifulSoup(link_ad.text , 'lxml')#сonnect to  link
               
               try:
                  release_data =  " ".join(str(soup.find(class_ = "relative")).split('datetime="')[1].split('"')[0].replace("T","/").split("+")[0].split(':')[:-1])
               except:
                  file = open("otus.txt", "w", encoding="utf-8")
                  file.write(link_ad.text)
                  file.close()
                  # arr_stop[id] == "False"
                  # bot.send_message(id,"<b>response 409 , через 5-10 мин попробуйте заново</b>".format(gen_link), reply_markup=Button.menu_users_telebot ,parse_mode='HTML')
                  time.sleep(3)
               try:
                  number_of_ads_from_the_author = str(soup.find(class_ = "c-text--subtitle c-text--left c-text").text).split("(")[1].split(")")[0].replace("\n","").replace("\t","").replace("'","").replace('"',"").replace(" ","").lstrip()               
               except:
                  number_of_ads_from_the_author = 0
               number_of_views_to_ad = soup.find_all(class_ = "details-list__item-value")              
               
               for i in number_of_views_to_ad:
                  try:
                     if type(int(i.text.replace(" ",''))) == int:
                        number_of_views_to_ad = i.text.replace(" ",'').replace("\t","").replace("\n","").replace('"',"").replace(" ","").lstrip() 
                        break
                  except:
                     pass
      
               chat_for_seller = "https://www.vinted.it/"+soup.find(class_ = "c-button--default c-button--medium c-button c-button--truncated").get('href')

               location_ad = soup.find_all(class_ = "details-list__item-value")
               for loc in location_ad:
                  if "Italia" in loc.text:
                     location_ad = loc.text.strip()

               if "aboba" != "False":
                  if int(obv) >= int(number_of_ads_from_the_author) and int(pros) >= int(number_of_views_to_ad) and "Italia" in location_ad:
                     try:
                        bot.send_photo(id,open("photo_{}.png".format(id), 'rb'),"<b>⛓ Название товара</b> : {}\n\n<b>💵 Цена товарa</b> : {}\n<b>🏢 Город</b> : {}\n<b>👤 Ник пользователя</b> : {}\n<b>✉️ Количество обьявлений у пользователя</b> : {}\n<b>👁 Количество просмотров на товаре</b> : {}\n<b>🕓 Дата выложения товара</b> : {}\n\n<b>🔗 Ссылка на товар</b> : <a href ='{}'>Ссылка</a>\n\n<b>🔗 Ссылка на чат с продавцом</b> :  <a href='{}'>Чатик</a> ".format(name_ad,price_ad,location_ad,name_seller,number_of_ads_from_the_author,number_of_views_to_ad,release_data,link_to_ad,chat_for_seller) ,parse_mode='HTML')#send photo
                     except:
                        pass
      except Exception as E:
            # bot.send_message(5456085368,E,parse_mode='HTML')
            pass
      current_page+=1
      arr_items = returns_arr_information(catalog_id,current_page,token,session)
   if arr_stop[id] != "False":
      print(current_page)
      bot.send_message(id,"<b>✅ Парс по ссылке: {} \nЗакончился</b>".format(gen_link), reply_markup=Button.menu_users_telebot ,parse_mode='HTML')
      # active_use_pars.remove(id)     
   else:
      pass     