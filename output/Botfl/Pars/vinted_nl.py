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
from fake_useragent import UserAgent
from urllib.request import urlopen
sys.path.insert(1,os.path.join(sys.path[0],'..'))
from Bot import Information
from Bot import Button
#,id,arr_stop,active_use_pars,obv,pros
bot = telebot.TeleBot(Information.token)  
def vinted_nl_pars(link,id,arr_stop,obv,pros,active_use_pars):
   current_page = 1
   all_page = 5 # all page
   gen_link = link
   headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
   #  PARS

   def find_current_catalog_id(link):
      ua = UserAgent()
      connect = requests.get(link, headers={'user-agent': f'{ua.random}'})
      soup = BeautifulSoup(connect.text , 'lxml')#connect to site  
      token = str(soup.find_all('meta')[-4]).split('content="')[1].split('"')[0]
      
      session = connect.text.split('"session_id":"')[1].split('","country"')[0]    
      if "catalog[]=" not in link and "search_text" not in link:
         
         catalog_id = str(soup.find('link',rel='alternative').get('href')).split('catalog_id=')[1]
      
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
   def returns_arr_information(catalog_id,current_page,session):
      ua = UserAgent()
      response = requests.get(link, headers={'User-Agent': ua.user_agent}) # Загружаем главную страницу для получения cookies
      x = response.cookies.get('_vinted_fr_session') # Сохраняем в переменную x cookie с именем _vinted_fr_session
      headers = {
         'authority': 'www.vinted.nl',
         'accept': 'application/json, text/plain, */*',
         'accept-language': 'it-fr',
         'dnt': '1',
         'referer': 'https://www.vinted.nl/vetements?catalog[]='+str(catalog_id)+'&page='+str(current_page),
         'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
         'sec-ch-ua-mobile': '?0',
         'sec-ch-ua-platform': '"Windows"',
         'sec-fetch-dest': 'empty',
         'sec-fetch-mode': 'cors',
         'sec-fetch-site': 'same-origin',
         'user-agent':  f'{ua.random}' ,
         #'x-csrf-token': token,
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
      if  "search_text" in gen_link:
         response = requests.get('https://www.vinted.nl/api/v2/catalog/items?search_text=iphone&catalog_ids=&color_ids=&brand_ids=&size_ids=&material_ids=&video_game_rating_ids=&status_ids=&is_for_swap=0&page='+str(current_page)+'&per_page=24&time=1662186434&search_session_id=0c23dbf6-982f-463b-9d30-404e2791d9a0'.format() ,headers={'User-Agent': ua.user_agent}, cookies={'_vinted_fr_session':x}).json() 
      else:
         response = requests.get('https://www.vinted.nl/api/v2/catalog/items', params=params, cookies={'_vinted_fr_session':x} , headers=headers).json()  
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
               price_ad = item.get("price")+" PL"
               link_to_ad = item.get('url')
               link_to_user = item.get('user').get('profile_url')
               #get photo
               response = urlopen(item.get('photo').get('url'))
               content = response.read()
               file = open('photo_'+str(id)+'.png', 'wb')
               file.write(content)
               file.close()      
               #
               time.sleep(random.randint(1,5))
               ua = UserAgent()
               response = requests.get(link_to_user, headers={'User-Agent': ua.user_agent}) # Загружаем главную страницу для получения cookies
               x = response.cookies.get('_vinted_fr_session') # Сохраняем в переменную x cookie с именем _vinted_fr_session
               link_ad = requests.get(link_to_ad, headers={'user-agent': f'{ua.random}'}, cookies={'_vinted_fr_session':x})
               soup = BeautifulSoup(link_ad.text , 'lxml')#сonnect to  link
               
               try:
                  release_data =  " ".join(str(soup.find(class_ = "relative")).split('datetime="')[1].split('"')[0].replace("T","/").split("+")[0].split(':')[:-1])
               except:
                  file = open("otus.txt", "w", encoding="utf-8")
                  file.write(link_ad.text)
                  file.close()
                  arr_stop[id] == "False"
                  bot.send_message(id,"<b>response 409 , через 5-10 мин попробуйте заново</b>".format(gen_link), reply_markup=Button.menu_users_telebot ,parse_mode='HTML')
                  current_page = 100
                  break
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
      
               chat_for_seller = "https://www.vinted.nl/"+soup.find(class_ = "c-button--default c-button--medium c-button c-button--truncated").get('href')

               location_ad = soup.find(class_ = "details-list__item-value").text.replace("\n","").replace("\t","").replace("'","").replace('"',"").lstrip()   

               if arr_stop != "False":
                  if int(obv) >= int(number_of_ads_from_the_author) and int(pros) >= int(number_of_views_to_ad) :
                     try:
                        bot.send_photo(id,open("photo_{}.png".format(id), 'rb'),"<b>⛓ Название товара</b> : {}\n\n<b>💵 Цена товарa</b> : {}\n<b>🏢 Город</b> : {}\n<b>👤 Ник пользователя</b> : {}\n<b>✉️ Количество обьявлений у пользователя</b> : {}\n<b>👁 Количество просмотров на товаре</b> : {}\n<b>🕓 Дата выложения товара</b> : {}\n\n<b>🔗 Ссылка на товар</b> : <a href ='{}'>Ссылка</a>\n\n<b>🔗 Ссылка на чат с продавцом</b> :  <a href='{}'>Чатик</a> ".format(name_ad,price_ad,location_ad,name_seller,number_of_ads_from_the_author,number_of_views_to_ad,release_data,link_to_ad,chat_for_seller) ,parse_mode='HTML')#send photo
                     except:
                        pass
      except Exception as E:
         bot.send_message(-1001761872781,E, reply_markup=Button.menu_users_telebot ,parse_mode='HTML')
         pass         
      current_page+=1
      arr_items = returns_arr_information(catalog_id,current_page,token,session)
   if arr_stop[id] != "False":
      bot.send_message(id,"<b>✅ Парс по ссылке: {} \nЗакончился</b>".format(gen_link), reply_markup=Button.menu_users_telebot ,parse_mode='HTML')
      active_use_pars.remove(id)     
   else:
      pass     
