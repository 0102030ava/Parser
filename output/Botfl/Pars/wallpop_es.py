
from bs4 import BeautifulSoup
import requests 
import lxml
import telebot
import sys
import os 
import time
from urllib.request import urlopen
sys.path.insert(1,os.path.join(sys.path[0],'..'))
from Bot.Information import token
from Bot import Button
bot = telebot.TeleBot(token)  
#link,id
def wallpop_es_pars(link,id,arr_stop,obv,pros,active_use_pars):
   current_page = 1
   all_page = 6
   def generate_current_link(link,current_page):#generate current link
      index_page = None
      gen_link = link
      #Base link check
      arr_name_categorias = ["coches-segunda-mano","motos","motor-y-accesorios","moda-y-complementos","inmobiliaria","tv-audio-foto","moviles-telefonos","electronica","deporte-y-ocio","bicicletas","consolas-y-videojuegos",'muebles-deco-y-jardin','electrodomesticos',"libros-pelis-musica","ninos-y-bebes","coleccionismo","construccion-y-reformas","industria-agricultura","empleo","servicios","otros"]
      arr_id_categorias = ["100","14000","12800","12465","200","12545","16000","15000","12579","17000","12900","12467","13100","12463","12461","18000","19000","20000","21000","13200","12485"]
      print(len(arr_name_categorias))
      print(len(arr_id_categorias))
      for num,base_link in enumerate(arr_name_categorias):
         if base_link in link:
            link = "https://api.wallapop.com/api/v3/general/search?user_province=Madrid&latitude=40.41956&start=40&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=b2a9a11e-50d2-435e-b4c5-a1ecbca2ccf8&country_code=ES&items_count=40&density_type=20&filters_source=default_filters&time_filter=today&order_by=closest&step={}&category_ids={}&longitude=-3.69196".format(current_page+1,arr_id_categorias[num])
            index_page = "step="
            break
      if "keywords" in link and "category_ids" not in link:
         link = "https://api.wallapop.com/api/v3/general/search?user_province=Madrid&keywords={}&latitude=40.41956&start={}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=e38c122d-8295-40c7-a3fe-7994353e4716&country_code=ES&experiment=distance_sensitivity_v6_variation_D&items_count=39&filters_source=recent_searches&order_by=most_relevance&step=0&longitude=-3.69196".format(link.split("keywords=")[1].split("&")[0],current_page+1)
         index_page = "start="
      elif "keywords" in link and "category_ids"  in link:
         link = "https://api.wallapop.com/api/v3/general/search?user_province=Madrid&keywords={}&latitude=40.41956&start={}&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=27f6c231-ae87-4e18-a89d-b9df3538c323&country_code=ES&experiment=distance_sensitivity_v6_variation_D&items_count=40&filters_source=suggester&order_by=most_relevance&step=0&category_ids={}&longitude=-3.69196".format(link.split("keywords=")[1].split("&")[0],current_page+1,link.split("category_ids=")[1].split("&")[0])
         index_page = "start="
      if "&start" not in link:
         link = "https://api.wallapop.com/api/v3/general/search?user_province=Madrid&latitude=40.41956&start=0&user_region=Comunidad+de+Madrid&user_city=Madrid&search_id=4bfd941c-02c4-4f67-96fb-429c5b45393a&country_code=ES&experiment=distance_sensitivity_v6_variation_D&items_count=26&density_type=20&filters_source=default_filters&time_filter=today&order_by=closest&step={}&category_ids=14000&longitude=-3.69196".format(current_page+1)
         index_page = "step="
      return(link,index_page,gen_link)

   answer = generate_current_link(link,current_page) # answer to def
   link,index_page,gen_link = answer[0], answer[1],answer[2]
   arr_ads = str(requests.get(link).text).split('[{"original"') # connect to answer

   while current_page <= all_page: # handler num
      for ad in arr_ads[1:]: #hundler ad
         if arr_stop[id] == "False":
            all_page = 10
            break
         else:
            
            try:
               name_ad = ad.split('"title":"')[1].split('","description"')[0] # name ad
               price_ad = ad.split('"price":')[1].split(',"currency"')[0] + " €"# price ad
               link_to_ad = 'https://es.wallapop.com/item/'+ad.split('"web_slug":"')[1].split('","category_id"')[0] #link to ad
               location_ad = ad.split('"city":"')[1].split('","postal_code"')[0]# location as
               link_to_user = "https://es.wallapop.com/app/user/{}/published".format(ad.split('"seller_id":"')[1].split('","favorited"')[0]) #link to user
               chat_for_seller = "https://es.wallapop.com/app/chat?itemId={}".format(ad.split('{"id":"')[1].split('","micro_name"')[0])

               #find url to photo
               response = urlopen(str(ad.split('","xsmall"')[0][2:]).split("?")[0])
               content = response.read()
               file = open('photo_'+str(id)+'.png', 'wb')
               file.write(content)
               file.close()

               #succes find photo
               link_ad = requests.get(link_to_ad)
               soup = BeautifulSoup(link_ad.text , 'lxml')#сonnect to  link
               name_seller = soup.find(class_ = "card-user-detail-name").text.replace("\n","").replace("\t","").replace("'","").replace('"',"").lstrip()
               number_of_views_to_ad = soup.find_all(class_ = "card-product-detail-user-stats-right")[1].text
               release_date = soup.find(class_ = "card-product-detail-user-stats-published").text.replace("\n","").replace("\t","").replace("'","").replace('"',"").lstrip()
               number_of_ads_from_the_author = str(soup.find(class_ = "card-user-detail-rating").text).split(" ")[0].replace("\n","").replace("\t","").replace("'","").replace('"',"").lstrip()
               if arr_stop[id] != "False":
                  if int(obv) >= int(number_of_ads_from_the_author) and int(pros) >= int(number_of_views_to_ad) :
                     bot.send_photo(id,open("photo_{}.png".format(id), 'rb'),"<b>⛓ Название товара</b> : {}\n\n<b>💵 Цена товарa</b> : {}\n<b>🏢 Город</b> : {}\n<b>👤 Ник пользователя</b> : {}\n<b>✉️ Количество обьявлений у пользователя</b> : {}\n<b>👁 Количество просмотров на товаре</b> : {}\n<b>🕓 Дата выложения товара</b> : {}\n\n<b>🔗 Ссылка на товар</b> : <a href ='{}'>Ссылка</a>\n\n<b>🔗 Ссылка на чат с продавцом</b> :  <a href='{}'>Чатик</a> ".format(name_ad,price_ad,location_ad,name_seller,number_of_ads_from_the_author,number_of_views_to_ad,release_date,link_to_ad,chat_for_seller) ,parse_mode='HTML')#send photo
                     #bot.send_message(id,"<b>⛓ Название товара</b> : {}\n\n<b>💵 Цена товарa</b> : {}\n<b>🏢 Город</b> : {}\n<b>👤 Ник пользователя</b> : {}\n<b>✉️ Количество обьявлений у пользователя</b> : {}\n<b>👁 Количество просмотров на товаре</b> : {}\n<b>🕓 Дата выложения товара</b> : {}\n\n<b>🔗 Ссылка на товар</b> : <a href ='{}'>Ссылка</a>\n\n<b>🔗 Ссылка на чат с продавцом</b> :  <a href='{}'>Чатик</a> ".format(name_ad,price_ad,location_ad,name_seller,number_of_ads_from_the_author,number_of_views_to_ad,release_date,link_to_ad,chat_for_seller) ,parse_mode='HTML')
            except Exception as E:
               pass 
      current_page+=1
      link = gen_link
      answer = generate_current_link(link,current_page) # answer to def
      link = answer[0]
      arr_ads = str(requests.get(link).text).split('[{"original"') # connect to answer
   if arr_stop[id] != "False":
      bot.send_message(id,"<b>✅ Парс по ссылке: {} \nЗакончился</b>".format(gen_link), reply_markup=Button.menu_users_telebot ,parse_mode='HTML')
      active_use_pars.remove(id)
      try:    
         os.remove("photo_{}.png".format(id))  
      except:
         pass      
   else:
      pass
