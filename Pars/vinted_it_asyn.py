from ast import ExtSlice
import json
from logging import NullHandler
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
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import text, bold, italic, code, pre, hide_link
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo
from requests.auth import HTTPProxyAuth
import aiohttp
import asyncio
stop_pars = {}

def generate_correct_json_link(link):
   ua = UserAgent()
   f = open('http_vinted.txt', 'r')
   l = [line.strip() for line in f] 
   random.shuffle(l)
   proxies = {"http":f"{':'.join(l[0].split(':')[:-2])}"}
   auth = HTTPProxyAuth(f"{l[0].split(':')[-2:][0]}", f"{l[0].split(':')[-2:][1]}")     


   connect = requests.get(link, headers={'user-agent': f'{ua.random}'}, proxies=proxies, auth=auth)
   soup = BeautifulSoup(connect.text , 'lxml')#connect to site    

      #generate correct json link

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
def generate_json(link,page_id,id):


   answer = generate_correct_json_link(link)
   catalog_id,token,session = answer[0],answer[1],answer[2]
   gen_link = link



   ua = UserAgent()
   f = open('http_vinted.txt', 'r')
   l = [line.strip() for line in f] 
   random.shuffle(l)
   proxies = {"http":f"{':'.join(l[0].split(':')[:-2])}"}
   auth = HTTPProxyAuth(f"{l[0].split(':')[-2:][0]}", f"{l[0].split(':')[-2:][1]}")         
   response = requests.get(link, headers={'user-agent': f'{ua.random}'}, proxies=proxies, auth=auth) # Загружаем главную страницу для получения cookies
   x = response.cookies.get('_vinted_fr_session') # Сохраняем в переменную x cookie с именем _vinted_fr_session
   if "search_text" not in gen_link:
         headers = {
            'authority': 'www.vinted.it',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'it-fr',
            'dnt': '1',
            'referer': 'https://www.vinted.it/vetements?catalog[]='+str(catalog_id)+'&page='+str(page_id+1),
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
            'order': 'newest_first',         
            'page': page_id+1,
            'per_page': '100',
           
            'search_session_id': session,
                  }
   else:
      text = gen_link.split("search_text=")[1].split('&')[0]
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
            'page': page_id+1,
            'per_page': '100',
            
            'search_session_id': session,
         }

  
   f = open('http_vinted.txt', 'r')
   l = [line.strip() for line in f] 
   random.shuffle(l)
   proxies = {"http":f"{':'.join(l[0].split(':')[:-2])}"}
   auth = HTTPProxyAuth(f"{l[0].split(':')[-2:][0]}", f"{l[0].split(':')[-2:][1]}")         
   if  "search_text" in gen_link:
         response = requests.get('https://www.vinted.it/api/v2/catalog/items', params=params, cookies={'_vinted_fr_session':x}, headers=headers).json()
   else:
         response = requests.get('https://www.vinted.it/api/v2/catalog/items', params=params, cookies={'_vinted_fr_session':x} , headers=headers, proxies=proxies, auth=auth).json()  
         
   if catalog_id == [] and "search_text" not in gen_link:
         response = requests.get('https://www.vinted.it/api/v2/catalog/items?catalog_ids=&color_ids=&brand_ids=&size_ids=&material_ids=&video_game_rating_ids=&status_ids=&is_for_swap=0&page={}&per_page=24&time=1662610671&search_session_id=62e41994-fbd4-4f54-ab9a-7dc591e9c59c'.format(page_id+1) , headers={'user-agent': f'{ua.random}'}, cookies={'_vinted_fr_session':x}, proxies=proxies, auth=auth).json() 
   items = response.get("items")
   with open('result_{}_{}.json'.format(id,page_id+1),'w', encoding="utf-8") as file:
         json.dump(items,file,indent=4,ensure_ascii=False)
   if items == [] or items is None or len(items) == 0:
      generate_json(link,page_id,id)

def send_inf(link,id):
   for page_id in range(3):
      generate_json(link,page_id,id)


async def gather_data(link,id,arr_stop,obv,pros):
   gen_link = link
   async with aiohttp.ClientSession() as session:
      tasks = []
      for page_id in range(3):
         task = asyncio.create_task(pars_vinted(session,link,id,page_id+1,obv,pros,arr_stop))
         tasks.append(task)
      await asyncio.gather(*tasks)

async def pars_vinted(session,link,id,page_id,obv,pros,arr_stop):
   try:
      b = []
      stop_pars[id] = b
      bot = Bot(token=Information.token)
      with open('result_{}_{}.json'.format(id,page_id), encoding="utf-8") as f:
         templates = json.load(f)
         for item in templates:
               if arr_stop[id] == "False":
                  try:
                     await session.close()   
                  except:
                        pass
                  break            
               else:     
                  #Get information for json    
                  name_ad = item.get("title")
                  name_seller = item.get('user').get('login')
                  price_ad = item.get("price")+" €"
                  link_to_ad = item.get('url')
                  link_to_user = item.get('user').get('profile_url')

                  # get photo
                  response = urlopen(item.get('photo').get('url'))
                  content = response.read()
                  file = open('photo_'+str(id)+'_'+str(page_id)+'.png', 'wb')
                  file.write(content)
                  file.close() 
                  #------------------------


                  #Get cookie
                  ua = UserAgent()
                  f = open('http_vinted.txt', 'r')
                  l = [line.strip() for line in f] 
                  proxy = f"http://{':'.join(l[page_id-1].split(':')[2:])}@{':'.join(l[page_id-1].split(':')[:2])}"
                  async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar()) as s:
                     async with s.get("https://www.vinted.it", headers={'user-agent': f'{ua.random}'}, proxy=str(proxy)) as r:
                        cookies = s.cookie_jar.filter_cookies('https://www.vinted.it/')

                  headers = {
                     'authority': 'www.vinted.it',
                     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                     'cache-control': 'max-age=0',
                     'dnt': '1',
                     'referer': 'https://www.vinted.it/',
                     'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
                     'sec-ch-ua-mobile': '?0',
                     'sec-ch-ua-platform': '"Windows"',
                     'sec-fetch-dest': 'document',
                     'sec-fetch-mode': 'navigate',
                     'sec-fetch-site': 'same-origin',
                     'sec-fetch-user': '?1',
                     'upgrade-insecure-requests': '1',
                     'user-agent': f'{ua.random}',
                  }

                  #--------------------------------------

                  async with session.get(url=link_to_ad , headers=headers,  cookies=cookies) as response:
                     response_text = await response.text()
                     soup = BeautifulSoup(response_text, 'lxml')
                     if page_id == 1:
                        await asyncio.sleep(random.randint(3,6))
                     if page_id == 2:
                        await asyncio.sleep(random.randint(4,8))
                     if page_id == 3:
                        await asyncio.sleep(random.randint(2,5))
                     if page_id == 4:
                        await asyncio.sleep(random.randint(3,9))                        
                     try:
                        release_data =  " ".join(str(soup.find(class_ = "relative")).split('datetime="')[1].split('"')[0].replace("T","/").split("+")[0].split(':')[:-1])
                     except:
                        file = open("otus_it.txt", "w", encoding="utf-8")
                        file.write(response_text)
                        file.close()   

                     try:
                        number_of_ads_from_the_author = str(soup.find(class_ = "c-text--subtitle c-text--left c-text").text).split("(")[1].split(")")[0].replace("\n","").replace("\t","").replace("'","").replace('"',"").replace(" ","").lstrip()               
                     except:
                        number_of_ads_from_the_author = 0
                     number_of_views_to_ad = soup.find_all(class_ = "details-list__item-value")              
                     for i in number_of_views_to_ad:
                        try:
                           if type(int(i.text.lstrip())) == int:
                              number_of_views_to_ad = i.text.lstrip()
                              break
                        except:
                           pass
                     try:
                        chat_for_seller = "https://www.vinted.it/"+soup.find(class_ = "c-button--default c-button--medium c-button c-button--truncated").get('href')
                        location_ad = soup.find_all(class_ = "details-list__item-value")
                        for loc in location_ad:
                           if "Italia" in loc.text:
                              location_ad = loc.text.strip()
                        if arr_stop[id] != "False":
                           if int(obv) >= int(number_of_ads_from_the_author) and int(pros) >= int(number_of_views_to_ad) and "Italia" in location_ad:
                              try:
                                 await bot.send_photo(id,open("photo_{}_{}.png".format(id,page_id), 'rb'),"<b>⛓ Название товара</b> : {}\n\n<b>💵 Цена товарa</b> : {}\n<b>🏢 Город</b> : {}\n<b>👤 Ник пользователя</b> : {}\n<b>✉️ Количество обьявлений у пользователя</b> : {}\n<b>👁 Количество просмотров на товаре</b> : {}\n<b>🕓 Дата выложения товара</b> : {}\n\n<b>🔗 Ссылка на товар</b> : <a href ='{}'>Ссылка</a>\n\n<b>🔗 Ссылка на чат с продавцом</b> :  <a href='{}'>Чатик</a> ".format(name_ad,price_ad,location_ad,name_seller,number_of_ads_from_the_author,number_of_views_to_ad,release_data,link_to_ad,chat_for_seller) ,parse_mode='HTML')#send photo
                              except:
                                 pass
                     except Exception as E:
                        print(E)
                        pass
         b.append(page_id)
         stop_pars[id] = stop_pars[id]+b
         if arr_stop[id] != "False":
            if len(stop_pars[id]) == 3:
               await bot.send_message(id,"<b>✅ Парс по ссылке: {} \nЗакончился</b>".format(link) ,parse_mode='HTML')
               try:
                  await session.close()   
               except:
                     pass
   except Exception as E:
      print(E)
      pass
def mainv(link,id,arr_stop,obv,pros):
   send_inf(link,id)
   asyncio.run(gather_data(link,id,arr_stop,obv,pros))

