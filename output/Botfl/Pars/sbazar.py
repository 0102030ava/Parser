from bs4 import BeautifulSoup
import requests 
import lxml
import telebot
import sys
import os 
from urllib.request import urlopen
sys.path.insert(1,os.path.join(sys.path[0],'..'))
from Bot import Information
from Bot import Button

bot = telebot.TeleBot(Information.token)  
def sbazar_pars(link,id,arr_stop,text,active_use_pars):
   used_phones = []
   try:
      try:
          link = str(link).replace(" ","")
      except:
          pass
      if link[-1] == "/":
         link = link[:-1]
   except:
      pass

   if "/cela-cr/cena-neomezena/nejnovejsi" not in link: #сheck link 
      link = link + "/cela-cr/cena-neomezena/nejnovejsi/"
   try:
      if type(int(link.split("/")[-1])) == int: #check num
         current_page = int(link.split("/")[-1])
   except:
         current_page = 1 # Basic num pages

   num_page = current_page + 4 # all page
   #                                                                 PARS

   connect = requests.get(link+str(current_page))
   soup = BeautifulSoup(connect.text , 'lxml')#connect to site

   while num_page >= current_page:# handler num

      all_ads = soup.find_all(class_ = "c-item c-item--uw") #all ads in site

      for current_ad in all_ads: #hundler ad
         if arr_stop[id] == "False":
            num_page = 10
            break
            
         else:

            name_ad = current_ad.find(class_ = "c-item__name-text").text # find name ad
            link_ad = current_ad.find(class_ = "c-item__link").get('href') # find link to ad
            current_ad_ = requests.get(link_ad)

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
               if phone not in used_phones:
                  used_phones.append(phone)
                  bot.send_photo(id,open("photo_{}.png".format(id), 'rb'),"<b>⛓ Название товара</b> : {}\n\n<b>💵 Цена товарa</b> : {}\n<b>🏢 Город</b> : {}\n<b>📱 Номер телефона</b> : {}\n<b>👤 Ник пользователя</b> : {}\n<b>🕛 Дата регист. аккаунта</b> : {}\n\n<b>🔗 Ссылка на товар</b> : <a href='{}'> Ссылочка</a>".format(name_ad,price_ad,location_ad,phone,nick_user,regestration_user,link_ad) ,parse_mode='HTML' , reply_markup=Button.but_for_phone(phone,text,link_ad))   
            except Exception as E:
               pass
      current_page+=1
      r = requests.get(link+str(current_page))
      soup = BeautifulSoup(r.text , 'lxml')
   if arr_stop[id] != "False":
      try:
         bot.send_message(id,"<b>✅ Парс по ссылке: {} \nЗакончился</b>".format(link), reply_markup=Button.menu_users_telebot ,parse_mode='HTML')
         active_use_pars.remove(id)
      except:
         pass
      try:    
         os.remove("photo_{}.png".format(id))  
      except:
         pass
   else:
      pass




