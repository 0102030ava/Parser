from ast import excepthandler
import asyncio
import requests
from email import header
import aiohttp
from bs4 import BeautifulSoup
import lxml
import sys
import unidecode
import os
import random
from datetime import date
from fake_useragent import UserAgent
from urllib.request import urlopen
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import text, bold, italic, code, pre, hide_link
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo
sys.path.insert(1,os.path.join(sys.path[0],'..'))
from Bot import Information
from Bot import Button
#async def get_information(session,link:str,page_id:int) -> str:
stop_pars = {}
sub_procces = {}
async def get_page_data(session,page_id,link,id,arr_stop,obv,pros,active_use_pars,text,gen_link,user_reg,text2):
   a = []
   b = []
   stop_pars[id] = b
   sub_procces[id] = a
   bot = Bot(token=Information.token)
   f = open('http_md999.txt', 'r')
   l = [line.strip() for line in f] 
   random.shuffle(l)
   proxy = f"http://{':'.join(l[0].split(':')[2:])}@{':'.join(l[0].split(':')[:2])}"
   headers = {
      "user-agent":"Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405"
   }
   try:
      url = f"{link}?page={page_id}"
      async with session.get(url=url , headers=headers, proxy=str(proxy)) as response:
         response_text = await response.text()
         soup = BeautifulSoup(response_text, 'lxml')
         try:
            if "&" in link:
               url = f"{link}&page={page_id}"
               async with session.get(url=url , headers=headers, proxy=str(proxy)) as response:
                  response_text = await response.text()
                  soup = BeautifulSoup(response_text, 'lxml')    
            if "query=" in link:
               url = f"{link}&page={page_id}"
               async with session.get(url=url , headers=headers, proxy=str(proxy)) as response:
                  response_text = await response.text()
                  soup = BeautifulSoup(response_text, 'lxml')                 
         except Exception as E:
            print(E)
            pass
         all_ad = soup.find_all(class_ = "ads-list-photo-item")
         for ad in all_ad:
            pass
            if arr_stop[id] == "False":
               try:
                  await session.close()
               except:
                  pass
               break   
            ua = UserAgent()            
            try:  
               price_check = ad.find(class_ = "ads-list-photo-item-price-wrapper").text
               if "Договорная" not in price_check:
                  title_ad = ad.find(class_ = "ads-list-photo-item-title").text.strip() # title ad
                  link = "https://999.md"+ad.find(class_ = "ads-list-photo-item-title").find('a').get('href') #link ad
                  if link.split("https://999.md/")[1][0] == "r": #
                     response = urlopen(ad.find(class_ = "ads-list-photo-item-thumb").find("img").get("src"))
                     content = response.read()
                     file = open(f'photo{page_id}_{id}.png', 'wb')
                     file.write(content)
                     file.close()                    
                     async with session.get(url=link , headers={'user-agent': f'{ua.random}'}, proxy=str(proxy)) as response:          
                        response_text = await response.text()
                        soup = BeautifulSoup(response_text, 'lxml')
                        if soup.find(class_ = "adPage__aside__stats__owner is-verified") != None: 
                           pass
                        else:
                           login_user = soup.find(class_ = "adPage__aside__stats__owner__login").text.split(" ")[1].strip()
                           Product_release_date = soup.find(class_ = "adPage__aside__stats__date").text.split("я:")[1].strip()
                         
                           views_on_ad = soup.find(class_ = "adPage__aside__stats__views").text.split(" ")[1].split(" ")[0]
                           date_of_registration_user = soup.find(class_ = "adPage__aside__stats__owner__registreDate").text.split("На сайте")[1].strip()
                           city_to_user = soup.find(class_ = "adPage__content__footer__wrapper").text.split("Регион:")[1].split("Кон")[0].replace(' ','').replace(','," ").strip()
                           try :
         
                              phone = soup.find(class_ = "js-phone-number adPage__content__phone grid_18").text.split("+")[1].lstrip()
                              phone = unidecode.unidecode(phone)
                              phone = phone.replace(" ","")
                              try:
                                 if type(int(phone)) != int:
                                    phone = phone
                              except Exception as E:
                                 phone = None
                                 pass
                           except Exception as E :
                              phone = None
                              pass  
                           link_to_user = "https://999.md/ru/profile/"+login_user
                           
                           async with session.get(url=link_to_user , headers={'user-agent': f'{ua.random}'}, proxy=str(proxy)) as response:          
                              response_text = await response.text()
                              soup = BeautifulSoup(response_text, 'lxml')

                              Authors_number_of_ads = len(soup.find_all(class_ = "profile-ads-list-photo-item"))
                           
                              if phone not in sub_procces[id] and int(pros) >= int(views_on_ad) and int(obv) >= int(Authors_number_of_ads) and int(date_of_registration_user.split(" ")[-1]) >= int(user_reg) and int(Product_release_date.split(",")[0].split(" ")[-1]) == int(date.today().strftime("%Y")):

                                 if int(Product_release_date.split(" ")[0]) == int(date.today().strftime("%d")) or  int(Product_release_date.split(" ")[0]) == int(int(date.today().strftime("%d"))-1):
                                    if arr_stop[id] != "False":                             
                                       await bot.send_photo(id,open(f'photo{page_id}_{id}.png', 'rb'),f"<b>⛓ Название товара</b> : {title_ad}\n\n<b>💵 Цена товарa</b> : {price_check}\n<b>🏢 Город</b> : {city_to_user}\n<b>📱 Номер телефона</b> : {phone}\n<b>👤 Ник пользователя</b> : {login_user}\n<b>🕛 Дата регист. аккаунта</b> : {date_of_registration_user}\n<b>⏱ Дата выложения товара</b> :{Product_release_date}\n<b>👁‍🗨 Количество просмотров на товаре</b> :{views_on_ad}\n<b>📍 Количество обьявлений у автора</b> :{Authors_number_of_ads}\n\n<b>🔗 Ссылка на товар</b> : <a href='{link}'> Ссылочка</a>", reply_markup=Button.but_for_phone_as(phone,text,link,text2,title_ad.replace(" ","+")) , parse_mode='HTML')   
                                       a.append(phone)
                                       sub_procces[id] = sub_procces[id]+a

            except Exception as E:
               print(E)
               pass
         b.append(page_id)
         stop_pars[id] = stop_pars[id]+b
         if arr_stop[id] != "False":
            if len(stop_pars[id]) == 9:
               await bot.send_message(id,"<b>✅ Парс по ссылке: {} \nЗакончился</b>".format(gen_link) ,parse_mode='HTML')
               try:
                  await session.close()   
               except:
                  pass

   except Exception as e:
      print(e)
      pass
async def gather_data(link,id,arr_stop,obv,pros,active_use_pars,text,user_reg,text2):
   gen_link = link
   async with aiohttp.ClientSession() as session:

      tasks = []
      for page_id in range(10):
         task = asyncio.create_task(get_page_data(session,page_id+1,link,id,arr_stop,obv,pros,active_use_pars,text,gen_link,user_reg,text2))
         tasks.append(task)
      await asyncio.gather(*tasks)

def main(link,id,arr_stop,obv,pros,active_use_pars,text,user_reg,text2):
   asyncio.run(gather_data(link,id,arr_stop,obv,pros,active_use_pars,text,user_reg,text2))

#id,link,obv,pros,text = 5456085368,"https://999.md/ru/list/phone-and-communication/mobile-phones?applied=1&hide_duplicates=yes&o_1084_593=6371&ef=352%2C1078%2C1084&buy_online=no&o_352_1=776",100000,1000,"abba"
#main(id,link,obv,pros,text)

