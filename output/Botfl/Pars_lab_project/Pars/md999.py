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
import re
import random
import datetime
from datetime import datetime
from fake_useragent import UserAgent
from urllib.request import urlopen
sys.path.insert(1,os.path.join(sys.path[0],'..'))
from Bot import Information
from Bot import Button
bot = telebot.TeleBot(Information.token)  


def tovarka_999(link,id,arr_stop,obv,pros,active_use_pars,text):
    gen_link = link.replace(" ",'')
    tek_str = 1
    used_phones = []
    while tek_str <= 10:
        try:
            ua = UserAgent()
            r = requests.get(gen_link, headers={'user-agent': f'{ua.random}'})
            soup = BeautifulSoup(r.text , 'lxml')
            sam_parser = soup.find_all(class_ = "ads-list-photo-item")
            for poisk in sam_parser:
                ua = UserAgent()
                if arr_stop[id] == "False":
                     current_page = 100
                     break                
                try:
                    pr = poisk.find(class_ = "ads-list-photo-item-price-wrapper").text
                    if str(pr) != " Договорная  ":
                        cena = poisk.find(class_ = "ads-list-photo-item-price-wrapper").text.replace("\t","").replace("\n","").lstrip()
                        name_tovara = poisk.find(class_ = "ads-list-photo-item-title").text.replace("\n","").replace("\t","").replace("'","").replace('"',"").lstrip()
                        ssulka = "https://999.md"+poisk.find(class_ = "ads-list-photo-item-title").find('a').get('href')
                        if ssulka.split("https://999.md/")[1][0] == "r":
                            response = urlopen(poisk.find(class_ = "ads-list-photo-item-thumb").find("img").get("src"))
                            content = response.read()
                            file = open('photo_'+str(id)+'.png', 'wb')
                            file.write(content)
                            file.close()                              
                            g = requests.get(ssulka, headers={'user-agent': f'{ua.random}'})
                            soup = BeautifulSoup(g.text , 'lxml')
                            #---------Name User

                            if soup.find(class_ = "adPage__aside__stats__owner is-verified") != None:
                                pass
                            else:
                                name_user = soup.find(class_ = "adPage__aside__stats__owner__login").text.split(" ")[1]
                                vulojenie_tovara = soup.find(class_ = "adPage__aside__stats__date").text.split("я:")[1]
                                prosmotru = soup.find(class_ = "adPage__aside__stats__views").text
                                data_reg = soup.find(class_ = "adPage__aside__stats__owner__registreDate").text.split("На сайте")[1]
                                gorod = soup.find(class_ = "adPage__content__footer__wrapper").text.split("Регион:")[1].split("Кон")[0].replace(' ','').replace(','," ")
                                #gorod = str(soup).split('</span> </div> <div class="region-list__list"')[0].split('<span>')[1] + str(soup).split('</label> </li> <li class="reg')[0]
                             
                                kategoria = soup.find_all('span' , itemprop="name")[1].text
                                prosmotru = prosmotru.split(" ")[1].split(" ")[0]
                                try :
                                    telefon = str("+"+str(soup).split('"country_code":')[1].split('}], "title": "')[0]+str(soup).split('"national_number": "')[1].split('", "country_code"')[0]).replace(" ","")
                                    try:
                                        if type(int(telefon)) != int:
                                            telefon = str("+"+str(soup).split('{"phone_number": "')[1].split('", "national_number":')[0]).replace(" ","")
                                    except:
                                        pass
                                except :
                                    pass
                                
                                ssulka_us = "https://999.md/ru/profile/"+name_user
                                ja = requests.get(ssulka_us, headers={'user-agent': f'{ua.random}'})
                                soup = BeautifulSoup(ja.text , 'lxml')
                                obc = 0
                                try: 
                                    try:
                                        index = soup.find(class_ = "is-last-page").find("a").get('href')
                                        r = requests.get("https://999.md"+index, headers={'user-agent': f'{ua.random}'}) 
                                        obc = ((int(str(index).split("page=")[1].split("#")[0])-1)*30)+len(soup.find_all(class_ = "profile-ads-list-photo-item"))
                                    except:

                                        obc = soup.find(class_ = "paginator cf").text.replace(" ",'')[-1]
                                        r = requests.get(link+"?page="+obc, headers={'user-agent': f'{ua.random}'}) 
                                        obc = ((int(obc)-1)*30)+len(soup.find_all(class_ = "profile-ads-list-photo-item"))
                                        
                                except Exception as e:
                                    obc = len(soup.find_all(class_ = "profile-ads-list-photo-item"))
                                current_datetime = datetime.now()
                                cur_day=int(current_datetime.day)
                                day = int(vulojenie_tovara.split(" ")[1])
                                delta = cur_day - day
                                if int(obv) >= int(obc) and int(pros) >= int(prosmotru) :
                                    if telefon not in used_phones:
                                        bot.send_photo(id,open("photo_{}.png".format(id), 'rb'), "<b>⛓Название товара:</b> "  +"<code>" +str(name_tovara)+"</code>" +" ⛓" + "\n" + "\n" + "💵<b>Цена:</b> " + "<code>" + str(cena) +"</code>" +" 💵" +"\n" +"\n"+"🏢<b>Город:</b> " +"<code>"+str(gorod)+"</code>" + " 🏢" + "\n"  + "\n" +"🕓<b>Дата выложения товара:</b> " + str(vulojenie_tovara) +" 🕓" + "\n" + "\n" +"🎭<b>Просмотры:</b>" + str(prosmotru) + " 🎭" +  "\n" + "\n"  + "📱<b>Номер телефона:</b> "  +"<code>"+str(telefon)+"</code>"  + " 📱" + "\n" + "\n"  + "✉️<b>Количество обьявлений на сайте:</b> " + str(obc) +" ✉️" + "\n" + "\n" + "🦣<b>Ник пользвателя:</b> " + str(name_user)+" 🦣" +  "\n" +  "\n" +"🕖<b>Дата регистрации</b> " + str(data_reg)+" 🕖" + "\n" + "\n" + "⛓<b>Ссылка:</b> " + '<a href="' +str(ssulka)+'">'+"Ссылка на товар</a>" +" ⛓"+"\n" + "\n" + "⛓<b>Ссылка:</b> " + '<a href="' +str(ssulka_us)+'">'+"Ссылка на автора</a>" +" ⛓" ,parse_mode='HTML' , reply_markup=Button.but_for_phone(telefon,text,ssulka))
                                        used_phones.append(telefon)
                except Exception as E:
                           
                            pass
            tek_str += 1 
            r = requests.get(gen_link + "&page="+ str(tek_str))
            soup = BeautifulSoup(r.text , 'lxml')
        except Exception as E:
            
            pass
    if arr_stop[id] != "False":
      bot.send_message(id,"<b>✅ Парс по ссылке: {} \nЗакончился</b>".format(gen_link), reply_markup=Button.menu_users_telebot ,parse_mode='HTML')
      try:
        active_use_pars.remove(id)
      except:
        pass
      try:    
         os.remove("photo_{}.png".format(id))  
      except:
         pass      
    else:
      pass
# link = "https://999.md/ru/list/furniture-and-interior/upholstery "
# id = "5456085368"
# arr_stop = {}
# arr_stop[5456085368] = "True"
# obv = 100000
# pros = 100000
# active_use_pars = []
# text = "aboba"
# tovarka_999(link,id,arr_stop,obv,pros,active_use_pars,text)