#library
from datetime import datetime
from datetime import date
from email import message
import imp
from pickle import GLOBAL
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import text, bold, italic, code, pre, hide_link
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo
import shutil

from pathlib import Path

import os
import sys

import re

import threading

import mysql.connector


# module

sys.path.insert(1,os.path.join(sys.path[0],'..'))
from Pars import sbazar_new
from Pars import wallpop_es
from Pars import vinted_pl_asyn
from Pars import vinted_it_asyn
from Pars import md999_async
from Pars import olxkz
import Information
import asyncio
import Button

import CheckRegToBot

import telebot
bot = Bot(token=Information.token)
dp = Dispatcher(bot)



#/start
@dp.message_handler(commands=['start'])
async def start(message : types.Message):
   ID = message.from_user.id

   
   cursor.execute('SELECT `ID` FROM check_user_id WHERE id = "'+str(message.from_user.id)+'" ;')
   info = cursor.fetchall()
   if info != []:
      if CheckRegToBot.User_Register(ID,db,cursor) is None:
         db.reconnect()
         cursor.execute('INSERT INTO `id_users` (`ID`) VALUES  ("'+str(message.from_user.id)+'") ;')
         db.commit()       
         cursor.execute('INSERT INTO `users_data` (`ID`,`Obyav`,`Prosmotru`,`text`,`UserName`,`user_reg_data`,`text2`) VALUES ( "'+str(message.from_user.id)+'","'+str("Не установленно")+'" ,"'+str("Не установленно")+'" , "'+str("Не установленно")+'","'+str(message.from_user.username)+'","'+str("Не установленно")+'","'+str("Не установленно")+'") ;')
         db.commit()
         if ID not in Information.user_admin:
            await bot.send_message(message.from_user.id, "<b>👋 Привествую  </b>"+message.from_user.first_name, reply_markup=Button.menu_users  , parse_mode=ParseMode.HTML)
            await bot.send_message(message.from_user.id, "<b>⚠️\nЕсли что-то не ворк пишите - @Nuu8rs</b>"  , parse_mode=ParseMode.HTML)
         else:
            await bot.send_message(message.from_user.id, "<b>👋 Привествую  </b>"+message.from_user.first_name, reply_markup=Button.menu_users_adm  , parse_mode=ParseMode.HTML)
            await bot.send_message(message.from_user.id, "<b>⚠️\nЕсли что-то не ворк пишите - @Nuu8rs</b>"  , parse_mode=ParseMode.HTML)
      else:
         
         if ID not in Information.user_admin:
            await bot.send_message(message.from_user.id, "<b>👋 Привествую  </b>"+message.from_user.first_name, reply_markup=Button.menu_users  , parse_mode=ParseMode.HTML)
            await bot.send_message(message.from_user.id, "<b>⚠️\nЕсли что-то не ворк пишите - @Nuu8rs</b>" , parse_mode=ParseMode.HTML)
         else:
            await bot.send_message(message.from_user.id, "<b>👋 Привествую  </b>"+message.from_user.first_name, reply_markup=Button.menu_users_adm  , parse_mode=ParseMode.HTML)
            await bot.send_message(message.from_user.id, "<b>⚠️\nЕсли что-то не ворк пишите - @Nuu8rs</b>", parse_mode=ParseMode.HTML)
   else:
      await bot.send_message(message.from_user.id, "<b>У вас нету доступа к парсеру</b>", reply_markup=None, parse_mode=ParseMode.HTML)
    

@dp.message_handler()
async def obrabotka(message: types.Message):
   try:
      current_datetime = datetime.now()

      #adm_panel
      if message.text =="🔱 Админ панель":
         if message.from_user.id == 5489731156 or message.from_user.id == 5456085368:
             await bot.send_message(message.from_user.id, "➖➖Админ панель➖➖", reply_markup=Button.adm_user_l)
         else:
            await bot.send_message(message.from_user.id, "➖➖Админ панель➖➖", reply_markup=Button.adm_user)

      #error
      if message.text == "⚠️ Сообщить о ошибке":
         await bot.send_message(message.from_user.id, "<b>🪓 Напишите подробно о ошибки , мы моментально отреагируем и исправим ее</b>", parse_mode=ParseMode.HTML)
         Information.arr_users[message.from_user.id] = "Error"

      #settings
      if message.text == "🔗 Настройки профиля":
         db.reconnect()
         cursor.execute('SELECT `Obyav`,`Prosmotru`,`text`,`user_reg_data`,`text2` FROM users_data WHERE id = "'+str(message.from_user.id)+'" ;')
         information_user = cursor.fetchall()
         await bot.send_message(message.from_user.id, "<b>🔗 Настройки профиля 🔗</b>\n\n<b>🫵🏿 Твой id: <code>{}</code></b>\n<b>🧿 Кол-во обьяв: <code>{}</code></b>\n<b>👁‍🗨 Кол-во просмотров: <code>{}</code></b>\n<b>💿 Дата рег аккаунта: <code>{}</code></b>\n\n<b>💾 Текст вотса: <code>{}</code></b>\n<b>💾 Текст вотса #2: <code>{}</code></b>".format(message.from_user.id ,information_user[0][0] ,information_user[0][1],information_user[0][3] ,information_user[0][2] ,information_user[0][4] ), reply_markup=Button.Butt_pars  , parse_mode=ParseMode.HTML)
    
      #// Parsing 
      if message.text == "❌ Остановить парсинг обьявлений":
         Information.arr_stop[message.from_user.id] = "False"
         await asyncio.sleep(1.2) 
         if message.from_user.id not in Information.user_admin:
            await bot.send_message(message.from_user.id, "✅ Парсинг обьявлений закончен", reply_markup=Button.menu_users)
         else:
            await bot.send_message(message.from_user.id, "✅ Парсинг обьявлений закончен", reply_markup=Button.menu_users_adm)
         Information.active_use_pars.remove(message.from_user.id)
         try:
            os.remove("photo_{}.png".format(message.from_user.id))
            os.remove("result_{}.json".format(id))  
         except:
            pass

      if message.text == "🖇 Парсить":
         try:
            Information.active_use_pars.remove(message.from_user.id)
         except:
            pass
         if message.from_user.id not in Information.active_use_pars: 
            await bot.send_message(message.from_user.id, "<b>🌐 Выберете сайт для парса</b>", reply_markup=Button.pars_choise_but , parse_mode=ParseMode.HTML)   

      #token
      if Information.arr_users[message.from_user.id] == "olxkztoken": 
         Information.arr_users[message.from_user.id] = Information.arr_users[message.from_user.id]+"_"+message.text
         await bot.send_message(message.from_user.id,"➡️➖➖➖➖➖➖⬅️\n\n❌ На данной плошадке нет количества <b>просмотров</b>\n❌ На данной плошадке нет количества <b>обьявлений у автора</b>\n\n<b>Введите ccылку для парса\nПример : https://www.olx.kz/d/dom-i-sad/</b>", parse_mode=ParseMode.HTML)



      if Information.arr_users[message.from_user.id].split("_")[0] == "olxkztoken" and Information.arr_users[message.from_user.id].split("_")[1] != message.text: 
         Information.arr_users[message.from_user.id] = Information.arr_users[message.from_user.id]+"_"+message.text
         if "olx.kz" in message.text:
            #execute information
            db.reconnect()
            cursor.execute('SELECT `Obyav`,`Prosmotru`,`text`,`user_reg_data`,`text` FROM users_data WHERE id = "'+str(message.from_user.id)+'" ;')
            information_user = cursor.fetchall()            
            await bot.send_message(message.from_user.id, "<b>✅ Парсинг по ссылке: <code>{}</code> начался</b>".format(message.text), reply_markup=Button.stop_pars  , parse_mode=ParseMode.HTML)  
            id,link,obv,pros,text,user_reg,text2,token = message.from_user.id, message.text,information_user[0][0],information_user[0][1],information_user[0][2],information_user[0][3],information_user[0][4],Information.arr_users[message.from_user.id].split("_")[1].split("_")[0]
            try:
               if type(int(user_reg)) == int:
                  pass
            except:
               user_reg = 1
            print(token)
            # if user settings = None
            if obv == "Не установленно":
               obv = 10000
            if pros == "Не установленно":
               pros = 1000
            #append information to arr
            Information.active_use_pars.append(message.from_user.id)
            Information.arr_stop[id] = "True"
            await bot.send_message(-1001626222956,"<b>Time</b> - {}/{}:{}\n<b>id user</b> - <code>{}</code>\n<b>username</b> - @{}\n\n<b>Start parsing</b> - {}".format(date.today(),current_datetime.hour,current_datetime.minute,id,message.from_user.username,link), parse_mode=ParseMode.HTML)
            #start thread
            Pars_flow = threading.Thread(target=olxkz.main , args=(link,id,Information.arr_stop,text,text2,token))
            Pars_flow.start()         
         
         
      if Information.arr_users[message.from_user.id] == "Link_pars_sbazar":
         if "https://www.sbazar.cz/" in message.text:
            await bot.send_message(message.from_user.id, "<b>✅ Парсинг по ссылке: <code>{}</code> начался</b>".format(message.text), reply_markup=Button.stop_pars , parse_mode=ParseMode.HTML)  
            db.reconnect()
            cursor.execute('SELECT `text`,`user_reg_data`,`text2` FROM users_data WHERE id = "'+str(message.from_user.id)+'" ;')
            information_user = cursor.fetchall()
            id,link,text,user_reg,text2 = message.from_user.id, message.text,information_user[0][0],information_user[0][1],information_user[0][2]
            try:
               if type(int(user_reg)) == int:
                  pass
            except:
               user_reg = 1
            Information.active_use_pars.append(message.from_user.id)
            Information.arr_stop[id] = "True"
            await bot.send_message(-1001626222956,"<b>Time</b> - {}/{}:{}\n<b>id user</b> - <code>{}</code>\n<b>username</b> - @{}\n\n<b>Start parsing</b> - {}".format(date.today(),current_datetime.hour,current_datetime.minute,id,message.from_user.username,link), parse_mode=ParseMode.HTML)
            #start thread
            Pars_flow = threading.Thread(target=sbazar_new.sbazar_pars , args=(link,id,Information.arr_stop,text,Information.active_use_pars,user_reg,text2))
            Pars_flow.start()

      if Information.arr_users[message.from_user.id] == "Link_pars_wallpop_es":
         if "es.wallapop.com" in message.text:
            #execute information
            db.reconnect()
            cursor.execute('SELECT `Obyav`,`Prosmotru` FROM users_data WHERE id = "'+str(message.from_user.id)+'" ;')
            information_user = cursor.fetchall()            
            await bot.send_message(message.from_user.id, "<b>✅ Парсинг по ссылке: <code>{}</code> начался</b>".format(message.text), reply_markup=Button.stop_pars  , parse_mode=ParseMode.HTML)  
            id,link,obv,pros = message.from_user.id, message.text,information_user[0][0],information_user[0][1]
            # if user settings = None
            if obv == "Не установленно":
               obv = 10000
            if pros == "Не установленно":
               pros = 1000
            #append information to arr
            Information.active_use_pars.append(message.from_user.id)
            Information.arr_stop[id] = "True"
            await bot.send_message(-1001626222956,"<b>Time</b> - {}/{}:{}\n<b>id user</b> - <code>{}</code>\n<b>username</b> - @{}\n\n<b>Start parsing</b> - {}".format(date.today(),current_datetime.hour,current_datetime.minute,id,message.from_user.username,link), parse_mode=ParseMode.HTML)
            #start thread
            Pars_flow = threading.Thread(target=wallpop_es.wallpop_es_pars , args=(link,id,Information.arr_stop,obv,pros,Information.active_use_pars))
            Pars_flow.start()

      if Information.arr_users[message.from_user.id] == "Link_pars_vinted_it":
         
         if "vinted.it" in message.text:
            #execute information
            db.reconnect()
            cursor.execute('SELECT `Obyav`,`Prosmotru` FROM users_data WHERE id = "'+str(message.from_user.id)+'" ;')
            information_user = cursor.fetchall()            
            await bot.send_message(message.from_user.id, "<b>✅ Парсинг по ссылке: <code>{}</code> начался</b>".format(message.text), reply_markup=Button.stop_pars  , parse_mode=ParseMode.HTML)  
            id,link,obv,pros = message.from_user.id, message.text,information_user[0][0],information_user[0][1]
            # if user settings = None
            if obv == "Не установленно":
               obv = 10000
            if pros == "Не установленно":
               pros = 1000
            #append information to arr
            Information.active_use_pars.append(message.from_user.id)
            Information.arr_stop[id] = "True"
            
            await bot.send_message(-1001626222956,"<b>Time</b> - {}/{}:{}\n<b>id user</b> - <code>{}</code>\n<b>username</b> - @{}\n\n<b>Start parsing</b> - {}".format(date.today(),current_datetime.hour,current_datetime.minute,id,message.from_user.username,link), parse_mode=ParseMode.HTML)
            #start thread
            Pars_flow = threading.Thread(target=vinted_it_asyn.mainv ,name=f"vinted_it_{id}", args=(link,id,Information.arr_stop,obv,pros))
            Pars_flow.start()
            Information.arr_users[message.from_user.id] = None
      if Information.arr_users[message.from_user.id] == "Link_pars_vinted_pl":
         if "vinted.pl" in message.text:
            db.reconnect()
            cursor.execute('SELECT `Obyav`,`Prosmotru` FROM users_data WHERE id = "'+str(message.from_user.id)+'" ;')
            information_user = cursor.fetchall()            
            await bot.send_message(message.from_user.id, "<b>✅ Парсинг по ссылке: <code>{}</code> начался</b>".format(message.text), reply_markup=Button.stop_pars  , parse_mode=ParseMode.HTML)  
            id,link,obv,pros = message.from_user.id, message.text,information_user[0][0],information_user[0][1]
            # if user settings = None
            if obv == "Не установленно":
               obv = 10000
            if pros == "Не установленно":
               pros = 1000
            #append information to arr
            Information.active_use_pars.append(message.from_user.id)
            Information.arr_stop[id] = "True"
            
            await bot.send_message(-1001626222956,"<b>Time</b> - {}/{}:{}\n<b>id user</b> - <code>{}</code>\n<b>username</b> - @{}\n\n<b>Start parsing</b> - {}".format(date.today(),current_datetime.hour,current_datetime.minute,id,message.from_user.username,link), parse_mode=ParseMode.HTML)
            #start thread
            Pars_flow = threading.Thread(target=vinted_pl_asyn.mainv ,name=f"vinted_pl_{id}", args=(link,id,Information.arr_stop,obv,pros))
            Pars_flow.start()

      if Information.arr_users[message.from_user.id] == "Link_pars_md999":
         if "999.md" in message.text:
            #execute information
            db.reconnect()
            cursor.execute('SELECT `Obyav`,`Prosmotru`,`text`,`user_reg_data`,`text` FROM users_data WHERE id = "'+str(message.from_user.id)+'" ;')
            information_user = cursor.fetchall()            
            await bot.send_message(message.from_user.id, "<b>✅ Парсинг по ссылке: <code>{}</code> начался</b>".format(message.text), reply_markup=Button.stop_pars  , parse_mode=ParseMode.HTML)  
            id,link,obv,pros,text,user_reg,text2 = message.from_user.id, message.text,information_user[0][0],information_user[0][1],information_user[0][2],information_user[0][3],information_user[0][4]
            try:
               if type(int(user_reg)) == int:
                  pass
            except:
               user_reg = 1
            # if user settings = None
            if obv == "Не установленно":
               obv = 10000
            if pros == "Не установленно":
               pros = 1000
            #append information to arr
            Information.active_use_pars.append(message.from_user.id)
            Information.arr_stop[id] = "True"
            if "m.999.md" in link:
               link = link.replace("m.",'')
            await bot.send_message(-1001626222956,"<b>Time</b> - {}/{}:{}\n<b>id user</b> - <code>{}</code>\n<b>username</b> - @{}\n\n<b>Start parsing</b> - {}".format(date.today(),current_datetime.hour,current_datetime.minute,id,message.from_user.username,link), parse_mode=ParseMode.HTML)
            #start thread
            Pars_flow = threading.Thread(target=md999_async.main ,name=f"md999_{id}", args=(link,id,Information.arr_stop,obv,pros,Information.active_use_pars,text,user_reg,text2))
            Pars_flow.start()                

      #// Ad setting
      if Information.arr_users[message.from_user.id] == "Obv":
         if type(int(message.text))  == int:
            db.reconnect()
            cursor.execute("UPDATE `users_data` SET `Obyav` = '"+str(message.text)+"' WHERE `ID` LIKE '"+str(message.from_user.id)+"' ;")
            db.commit()
            Information.arr_users[message.from_user.id] == None
            cursor.execute('SELECT `Obyav`,`Prosmotru`,`text`,`user_reg_data`,`text2` FROM users_data WHERE id = "'+str(message.from_user.id)+'" ;')
            information_user = cursor.fetchall()
            await bot.send_message(message.from_user.id, "<b>🔗 Настройки профиля 🔗</b>\n\n<b>🫵🏿 Твой id: <code>{}</code></b>\n<b>🧿 Кол-во обьяв: <code>{}</code></b>\n<b>👁‍🗨 Кол-во просмотров: <code>{}</code></b>\n<b>💿 Дата рег аккаунта: <code>{}</code></b>\n\n<b>💾 Текст вотса: <code>{}</code></b>\n<b>💾 Текст вотса #2: <code>{}</code></b>".format(message.from_user.id ,information_user[0][0] ,information_user[0][1],information_user[0][3] ,information_user[0][2] ,information_user[0][4] ), reply_markup=Button.Butt_pars  , parse_mode=ParseMode.HTML)
            Information.arr_users[message.from_user.id] = None
         else:
            await bot.send_message(message.from_user.id, "<b>❌ Введите коректные данные</b>" , parse_mode=ParseMode.HTML)   

      if Information.arr_users[message.from_user.id] == "Pros":
         if type(int(message.text))  == int:
            db.reconnect()
            cursor.execute("UPDATE `users_data` SET `Prosmotru` = '"+str(message.text)+"' WHERE `ID` LIKE '"+str(message.from_user.id)+"' ;")
            db.commit()
            Information.arr_users[message.from_user.id] == None
            cursor.execute('SELECT `Obyav`,`Prosmotru`,`text`,`user_reg_data`,`text2` FROM users_data WHERE id = "'+str(message.from_user.id)+'" ;')
            information_user = cursor.fetchall()
            await bot.send_message(message.from_user.id, "<b>🔗 Настройки профиля 🔗</b>\n\n<b>🫵🏿 Твой id: <code>{}</code></b>\n<b>🧿 Кол-во обьяв: <code>{}</code></b>\n<b>👁‍🗨 Кол-во просмотров: <code>{}</code></b>\n<b>💿 Дата рег аккаунта: <code>{}</code></b>\n\n<b>💾 Текст вотса: <code>{}</code></b>\n<b>💾 Текст вотса #2: <code>{}</code></b>".format(message.from_user.id ,information_user[0][0] ,information_user[0][1],information_user[0][3] ,information_user[0][2] ,information_user[0][4] ), reply_markup=Button.Butt_pars  , parse_mode=ParseMode.HTML)
            Information.arr_users[message.from_user.id] = None
         else:
            await bot.send_message(message.from_user.id, "<b>❌ Введите коректные данные</b>" , parse_mode=ParseMode.HTML)    

      if Information.arr_users[message.from_user.id] == "Text":
         db.reconnect()
         cursor.execute("UPDATE `users_data` SET `Text` = '"+str(message.text)+"' WHERE `ID` LIKE '"+str(message.from_user.id)+"' ;")
         db.commit()
         Information.arr_users[message.from_user.id] == None
         cursor.execute('SELECT `Obyav`,`Prosmotru`,`text`,`user_reg_data`,`text2` FROM users_data WHERE id = "'+str(message.from_user.id)+'" ;')
         information_user = cursor.fetchall()
         await bot.send_message(message.from_user.id, "<b>🔗 Настройки профиля 🔗</b>\n\n<b>🫵🏿 Твой id: <code>{}</code></b>\n<b>🧿 Кол-во обьяв: <code>{}</code></b>\n<b>👁‍🗨 Кол-во просмотров: <code>{}</code></b>\n<b>💿 Дата рег аккаунта: <code>{}</code></b>\n\n<b>💾 Текст вотса: <code>{}</code></b>\n<b>💾 Текст вотса #2: <code>{}</code></b>".format(message.from_user.id ,information_user[0][0] ,information_user[0][1],information_user[0][3] ,information_user[0][2] ,information_user[0][4] ), reply_markup=Button.Butt_pars  , parse_mode=ParseMode.HTML)
         Information.arr_users[message.from_user.id] = None

      if Information.arr_users[message.from_user.id] == "Text2":
         db.reconnect()
         cursor.execute("UPDATE `users_data` SET `Text2` = '"+str(message.text)+"' WHERE `ID` LIKE '"+str(message.from_user.id)+"' ;")
         db.commit()
         Information.arr_users[message.from_user.id] == None
         cursor.execute('SELECT `Obyav`,`Prosmotru`,`text`,`user_reg_data`,`text2` FROM users_data WHERE id = "'+str(message.from_user.id)+'" ;')
         information_user = cursor.fetchall()
         await bot.send_message(message.from_user.id, "<b>🔗 Настройки профиля 🔗</b>\n\n<b>🫵🏿 Твой id: <code>{}</code></b>\n<b>🧿 Кол-во обьяв: <code>{}</code></b>\n<b>👁‍🗨 Кол-во просмотров: <code>{}</code></b>\n<b>💿 Дата рег аккаунта: <code>{}</code></b>\n\n<b>💾 Текст вотса: <code>{}</code></b>\n<b>💾 Текст вотса #2: <code>{}</code></b>".format(message.from_user.id ,information_user[0][0] ,information_user[0][1],information_user[0][3] ,information_user[0][2] ,information_user[0][4] ), reply_markup=Button.Butt_pars  , parse_mode=ParseMode.HTML)

         Information.arr_users[message.from_user.id] = None

      if Information.arr_users[message.from_user.id] == "user_reg":

         db.reconnect()
         cursor.execute("UPDATE `users_data` SET `user_reg_data` = '"+str(message.text)+"' WHERE `ID` LIKE '"+str(message.from_user.id)+"' ;")
         db.commit()
         Information.arr_users[message.from_user.id] == None
         cursor.execute('SELECT `Obyav`,`Prosmotru`,`text`,`user_reg_data` FROM users_data WHERE id = "'+str(message.from_user.id)+'" ;')
         information_user = cursor.fetchall()
         await bot.send_message(message.from_user.id, "<b>🔗 Настройки профиля 🔗</b>\n\n<b>🫵🏿 Твой id: <code>{}</code></b>\n<b>🧿 Кол-во обьяв: <code>{}</code></b>\n<b>👁‍🗨 Кол-во просмотров: <code>{}</code></b>\n<b>💿 Дата рег аккаунта: <code>{}</code></b>\n\n<b>💾 Текст вотса: <code>{}</code></b>".format(message.from_user.id ,information_user[0][0] ,information_user[0][1],information_user[0][3] ,information_user[0][2] ), reply_markup=Button.Butt_pars  , parse_mode=ParseMode.HTML)
         Information.arr_users[message.from_user.id] = None         

      if Information.arr_users[message.from_user.id] == "Error" and message.text != "⚠️ Сообщить о ошибке" and message.text != "🔗 Настройки профиля" and message.text != "🔱 Админ панель" :
         await bot.send_message(-1001761872781, "<b>Произошла ошибка у пользователя</b> : @{}\n \n\n<b>Описание ошбики</b> : {}".format(message.from_user.username,message.text) , parse_mode=ParseMode.HTML)
         await bot.send_message(message.from_user.id, "<b>Ваше сообщение было отправленно</b>" , parse_mode=ParseMode.HTML)
         Information.arr_users[message.from_user.id] = None
      
      if Information.arr_users[message.from_user.id] == "addtouser":
         try:
            if type(int(message.text)) == int:
               db.reconnect()
               cursor.execute('INSERT INTO `check_user_id` (`ID`) VALUES  ("'+str(message.text)+'") ;')
               db.commit()  
               if message.from_user.id == 5489731156 or message.from_user.id == 5456085368:
                  await bot.send_message(message.from_user.id, "<b>✅Пользователь {} был добавлен</b>".format(message.text), reply_markup=Button.adm_user_l , parse_mode=ParseMode.HTML)
               else:
                  await bot.send_message(message.from_user.id, "<b>✅Пользователь {} был добавлен</b>".format(message.text), reply_markup=Button.adm_user , parse_mode=ParseMode.HTML)
               Information.arr_users[message.from_user.id] = None
         except:
            pass

      if Information.arr_users[message.from_user.id] == "deletetouser":
         try:
            if type(int(message.text)) == int:
               db.reconnect()
               cursor.execute("DELETE FROM check_user_id where ID  = '" + str(message.text) + "';")
               db.commit()   
               if message.from_user.id == 5489731156 or message.from_user.id == 5456085368:
                  await bot.send_message(message.from_user.id, "<b>✅Пользователь {} был удален</b>".format(message.text) , reply_markup=Button.adm_user, parse_mode=ParseMode.HTML)
               else:
                  await bot.send_message(message.from_user.id, "<b>✅Пользователь {} был удален</b>".format(message.text) , reply_markup=Button.adm_user, parse_mode=ParseMode.HTML)
               Information.arr_users[message.from_user.id] = None
         except:
            pass
      if Information.arr_users[message.from_user.id] == "addadm": 
         try:
            if type(int(message.text)) == int:
               db.reconnect()
               cursor.execute('INSERT INTO `user_adm` (`id`) VALUES  ("'+str(message.text)+'") ;')
               db.commit()   
               Information.user_admin.append(int(message.text))
               await bot.send_message(message.from_user.id, "<b>✅Пользователь {} была выданна админ панель</b>".format(message.text), reply_markup=Button.adm_user_l , parse_mode=ParseMode.HTML)
               Information.arr_users[message.from_user.id] = None
         except:
            pass    

      if Information.arr_users[message.from_user.id] == "send_text":
         db.reconnect()
         cursor.execute('SELECT `ID` FROM users_data ;')
         id_users = cursor.fetchall()
         for id_user in id_users:
            try:
               await bot.send_message(id_user[0], f"<b>{message.text}</b>" ,parse_mode=ParseMode.HTML)
            except:
               pass


   except Exception as E:
      print(E)
      pass


@dp.callback_query_handler()
async def obs4et_kategorii(call: types.CallbackQuery):
   try:
      #// Callb Settings
      callb = call.data
      if callb == "add_user":
         await call.message.edit_text("<b>▶️ Введите id пользователя , которого хотите добавить</b>", parse_mode=ParseMode.HTML)
         Information.arr_users[call.message.chat.id] = "addtouser"
      
      if callb == "delete_user":
         await call.message.edit_text("<b>▶️ Введите id пользователя , которого хотите удалить</b>", parse_mode=ParseMode.HTML)
         Information.arr_users[call.message.chat.id] = "deletetouser"

      if callb == "send_message_all_users":
         await call.message.edit_text("<b>▶️ Введите текст для рассылки сообщений</b>", parse_mode=ParseMode.HTML)
         Information.arr_users[call.message.chat.id] = "send_text"         

      if callb == "add_adm_l":
         await call.message.edit_text("<b>▶️ Введите id пользователя , которому хотите дать админ панель</b>", parse_mode=ParseMode.HTML)
         Information.arr_users[call.message.chat.id] = "addadm"         

      
#PARS
      if callb == "sbazar":
         await call.message.edit_text("➡️➖➖➖➖➖➖⬅️\n\n❌ На данной плошадке нет количества <b>просмотров</b>\n❌ На данной плошадке нет количества <b>обьявлений у автора</b>\n\n<b>Введите ccылку для парса\nПример : https://www.sbazar.cz/29-detsky-bazar</b>", parse_mode=ParseMode.HTML)
         Information.arr_users[call.message.chat.id] = "Link_pars_sbazar"

      if callb == "md999":
         await call.message.edit_text("➡️➖➖➖➖➖➖⬅️\n\n<b>Введите ccылку для парса\nПример : https://999.md/ru/list/furniture-and-interior/upholstery</b>", parse_mode=ParseMode.HTML)
         Information.arr_users[call.message.chat.id] = "Link_pars_md999"

      if callb == "wallpop_es":
         await call.message.edit_text("➡️➖➖➖➖➖➖⬅️\n\n❌ На данной плошадке нет <b>номеров телефонов</b>\n\n<b>Введите ccылку для парса\nПример : https://es.wallapop.com/otros</b>", parse_mode=ParseMode.HTML)
         Information.arr_users[call.message.chat.id] = "Link_pars_wallpop_es"   

      if callb == "vinted_it":
         await call.message.edit_text("➡️➖➖➖➖➖➖⬅️\n\n❌ На данной плошадке нет <b>номеров телефонов</b>\n\n<b>Введите ccылку для парса\nПример : https://www.vinted.it/intrattenimento/videogiochi-e-console/xbox-one</b>", parse_mode=ParseMode.HTML)
         Information.arr_users[call.message.chat.id] = "Link_pars_vinted_it"   

      if callb == "vinted_pl":
         await call.message.edit_text("➡️➖➖➖➖➖➖⬅️\n\n❌ На данной плошадке нет <b>номеров телефонов</b>\n\n<b>Введите ccылку для парса\nПример : https://www.vinted.pl/vetements?search_text=iphone&search_id=6295293111&time=1662186927</b>", parse_mode=ParseMode.HTML)
         Information.arr_users[call.message.chat.id] = "Link_pars_vinted_pl"      

      if callb == "vinted_nl":
         await call.message.edit_text("➡️➖➖➖➖➖➖⬅️\n\n❌ На данной плошадке нет <b>номеров телефонов</b>\n\n<b>Введите ccылку для парса\nПример : https://www.vinted.nl/vetements?search_text=iphone&search_id=6295293111&time=1662186927</b>", parse_mode=ParseMode.HTML)
         Information.arr_users[call.message.chat.id] = "Link_pars_vinted_nl"
      if callb == "Olxtoken":
         await call.message.edit_text("➡️➖➖➖➖➖➖⬅️\n\n<b>Введите токен для OLX.KZ\n\nКак получить токен? - <a href='https://telegra.ph/Kak-poluchit-token-OLXKZ-10-06'> Информация</a></b>", parse_mode=ParseMode.HTML)
         #await call.message.edit_text("➡️➖➖➖➖➖➖⬅️\n\n❌ На данной плошадке нет количества <b>просмотров</b>\n❌ На данной плошадке нет количества <b>обьявлений у автора</b>\n\n<b>Введите ccылку для парса\nПример : https://www.olx.kz/d/dom-i-sad/</b>", parse_mode=ParseMode.HTML)
         Information.arr_users[call.message.chat.id] = "olxkztoken"               

#---
      if callb == "Obv":
         await call.message.edit_text("<b>▶️ Введите максимальный порог количества обьявлений у автора</b>", parse_mode=ParseMode.HTML)
         Information.arr_users[call.message.chat.id] = "Obv" 

      if callb == "Pros":
         await call.message.edit_text("<b>▶️ Введите максимальный порог количества просмотров на обьявление</b>", parse_mode=ParseMode.HTML)
         Information.arr_users[call.message.chat.id] = "Pros"

      if callb == "Text":
         await call.message.edit_text("<b>▶️ Введите свой текст для вотсапа , который будет использоваться при переходе в вотс</b>\n\n⚙️ <b>Чтобы ставить ссылку в сообщение напишите: <code>-ссылка-</code></b>\n\n⚙️ <b>Чтобы ставить название товара  в сообщение напишите: <code>-товар-</code></b>\n\n<b>Пример : <code>Здравствуйте -товар- по данной -ссылка- еще актуален?</code></b>", parse_mode=ParseMode.HTML)
         Information.arr_users[call.message.chat.id] = "Text"        

      if callb == "Text2":
         await call.message.edit_text("<b>▶️ Введите свой текст для вотсапа , который будет использоваться при переходе в вотс</b>\n\n⚙️ <b>Чтобы ставить ссылку в сообщение напишите: <code>-ссылка-</code></b>\n\n⚙️ <b>Чтобы ставить название товара  в сообщение напишите: <code>-товар-</code></b>\n\n<b>Пример : <code>Здравствуйте -товар- по данной -ссылка- еще актуален?</code></b>", parse_mode=ParseMode.HTML)
         Information.arr_users[call.message.chat.id] = "Text2"   

      if callb == "data_reg_pl":
         await call.message.edit_text("<b>▶️ Введите порог даты регистрации аккаунта пользователя</b> ", parse_mode=ParseMode.HTML)
         Information.arr_users[call.message.chat.id] = "user_reg" 
  
   except Exception as E:
      print({E})


if __name__ == '__main__':
   config = {                                     
         'user': 'Nursyka',                     
         'password': '3y@CB%8D)sNkv56!Bj+9',         
         'host': 'DESKTOP-S95L17M',                
         'port': '3306',                    
         'database': "parsfl",                  
               }
   print("Connect SQL Done")                                  
   db = mysql.connector.connect(**config)  
   cursor = db.cursor()   

   db.reconnect()
   cursor.execute('SELECT id FROM user_adm;')
   adm_user = cursor.fetchall()
   for user in  adm_user:
            Information.user_admin.append(int(user[0]))


   executor.start_polling(dp)