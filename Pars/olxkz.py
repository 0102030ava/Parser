
from datetime import datetime
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

bot = telebot.TeleBot(Information.token)
def get_phone(id_add,url,tokenus):
   
    headers = {
        'authority': 'friction.olxgroup.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        # Already added when you pass json=
        # 'content-type': 'application/json',
        'origin': 'https://www.olx.kz',
        'referer': 'https://www.olx.kz/',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'x-user-tests': 'eyJidXktMjg5MyI6ImIiLCJidXktMjg5NSI6ImEiLCJkZWNpc2lvbi0yMDYiOiJiIiwiZGVjaXNpb24tMzc3IjoiYiIsImRlY2lzaW9uLTUzNiI6ImEiLCJkZWNpc2lvbi03OTAiOiJiIiwiZXItMTcwOCI6ImEiLCJlci0xNzc4IjoiYiIsImV1b25iLTQ5MyI6ImEiLCJmOG5ycC0xMjE4IjoiYyIsImpvYnMtMzcxNyI6ImIiLCJqb2JzLTM4MzciOiJjIiwiam9icy0zODQ1IjoiYSIsImpvYnMtNDE0NSI6ImQiLCJvZXN4LTE1NDciOiJhIiwib2V1MnUtMjQ0MSI6ImIifQ==',
    }

    json_data = {
        'action': 'reveal_phone_number',
        'aud': 'atlas',
        'actor': {
            'username': 'c95ba3dc-cc53-485d-8171-1279a98d7824',
        },
        'scene': {
            'origin': 'www.olx.kz',
        },
    }

    response = requests.post('https://friction.olxgroup.com/challenge', headers=headers, json=json_data).json()
    context = response.get("context")


    headers = {
        'authority': 'friction.olxgroup.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        # Already added when you pass json=
        # 'content-type': 'application/json',
        'origin': 'https://www.olx.kz',
        'referer': 'https://www.olx.kz/',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }

    json_data = {
        'context':context ,
        'response': '',
    }

    response = requests.post('https://friction.olxgroup.com/exchange', headers=headers, json=json_data).json()
    token = response.get("token")



    cookies = {
        'dfp_user_id': 'bdce835b-79e6-4c25-830e-c8d471635e47-ver2',
        'laquesisff': 'aut-716#buy-2811#decision-657#euonb-114#euonb-48#euweb-1372#euweb-451#grw-124#kuna-307#oesx-1437#oesx-1643#oesx-645#oesx-867#olxeu-29763#srt-1289#srt-1346#srt-1434#srt-1593#srt-1758#srt-627#srt-633#srt-635#srt-899',
        '__utmz': '16996198.1664298437.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        '_ga': 'GA1.2.1586618035.1664298437',
        '_gcl_au': '1.1.1511600409.1664298437',
        'user_adblock_status': 'false',
        'lister_lifecycle': '1664298438',
        '_hjSessionUser_2218931': 'eyJpZCI6ImMzNjkxYTM3LTE2ZmQtNWNiNC1iNjM2LTUwNzcwYzAxNjRkOSIsImNyZWF0ZWQiOjE2NjQyOTg0MzY2NzIsImV4aXN0aW5nIjp0cnVlfQ==',
        '__gads': 'ID=3d9753f37d71d60a:T=1664298436:S=ALNI_Ma4QHqPGhLj71oClMQ5_HYPAYtWkw',
        'mobile_default': 'desktop',
        'fingerprint': 'MTI1NzY4MzI5MTsxNjswOzA7MDsxOzA7MDswOzA7MDsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MDsxOzE7MTswOzA7MDswOzE7MDswOzE7MTsxOzE7MTswOzE7MDswOzE7MTsxOzA7MDswOzA7MDswOzE7MDsxOzA7MDswOzA7MDswOzA7MTsxOzA7MTsxOzE7MTswOzE7MDszNDEwNzc3ODI5OzI7MjsyOzI7MjsyOzU7Mjg0ODAwNjQxODsxMzU3MDQxNzM4OzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTswOzA7MDs0MTAwMjE5OTszNDY5MzA2NTUxOzM2OTE3NTk4OTY7Nzg1MjQ3MDI5OzEwMDUzMDEyMDM7MTkyMDsxMDgwOzI0OzI0OzM2MDszNjA7MzYwOzM2MDszNjA7MzYwOzM2MDszNjA7MzYwOzM2MDszNjA7MzYwOzM2MDszNjA7MzYwOzM2MDszNjA7MzYwOzM2MDszNjA7MDswOzA=',
        'from_detail': '0',
        'ldTd': 'true',
        '__utmc': '16996198',
        'newrelic_cdn_name': 'CF',
        'dfp_segment': '%5B%5D',
        'laquesis': 'buy-2893@b#buy-2895@a#decision-206@b#decision-377@b#decision-536@a#decision-790@b#er-1708@a#er-1778@b#euonb-493@a#f8nrp-1218@c#jobs-3717@b#jobs-3837@c#jobs-3845@a#jobs-4145@d#oesx-1547@a#oeu2u-2441@b',
        'laquesissu': '297@ad_page|1#297@reply_phone_1step|1',
        '_ym_uid': '1664865360100642542',
        '_ym_d': '1664865360',
        '_ym_visorc': 'w',
        '__utma': '16996198.1586618035.1664298437.1664325010.1664865362.3',
        '__utmt': '1',
        '_gid': 'GA1.2.2079208551.1664865363',
        '_ym_isad': '2',
        '__gpi': 'UID=00000b5183101bf5:T=1664298436:RT=1664865364:S=ALNI_MbAW5lfTC9uj-4tLfeOsb6NVS69FQ',
        '_hjIncludedInSessionSample': '0',
        '_hjSession_2218931': 'eyJpZCI6ImM5ZmYzMjI0LWNiYzYtNDk4Yi1iYmM1LTYzNWEzYmNkMTUzMSIsImNyZWF0ZWQiOjE2NjQ4NjUzNjQ2NjMsImluU2FtcGxlIjpmYWxzZX0=',
        '_hjAbsoluteSessionInProgress': '0',
        'tmr_lvid': 'd05bc2af964325b0c9a27f861a457a95',
        'tmr_lvidTS': '1664865365066',
        'PHPSESSID': '01n7aiggq1101sqm26nvi5elqg',
        'x-device-id': 'q2ympu0vz6gpe1%3A1664865382935',
        'user_id': '381910128',
        'lang': 'ru',
        'access_token': '61361e0a38499289a8ba3308d62b0ef510fca6e3',
        'refresh_token': 'f5e349f888f72f4315a8d947e354e69758145faf',
        'deviceGUID': '0b2dee4a-0f03-48d1-a8e6-9622dbef4b32',
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2022-10-04%2012%3A36%3A27%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.olx.kz%2Fd%2Fmyaccount%2F%23login%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.olx.kz%2Faccount%2F%3Fref%255B0%255D%255Baction%255D%3Dmyaccount%26ref%255B0%255D%255Bmethod%255D%3Dindex',
        'sbjs_first_add': 'fd%3D2022-10-04%2012%3A36%3A27%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.olx.kz%2Fd%2Fmyaccount%2F%23login%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.olx.kz%2Faccount%2F%3Fref%255B0%255D%255Baction%255D%3Dmyaccount%26ref%255B0%255D%255Bmethod%255D%3Dindex',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29',
        'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%206.1%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F104.0.0.0%20Safari%2F537.36',
        'user_business_status': 'private',
        '_gat': '1',
        '__diug': 'true',
        'criteo_hashed_email': 'd41d8cd98f00b204e9800998ecf8427e',
        'criteo_hashed_email_15': 'd41d8cd98f00b204e9800998ecf8427e',
        '__utmb': '16996198.2.10.1664865362',
        'cto_bundle': '7D1_F19rY2ZBSHdKelhWMXYzNlpRJTJCQzJBYjAwdndBTEhlZkxvUHRCdUQ2UUZKaEtJZlJmVERVRjVhczZNZUgzVHUlMkZWVHczQnBsVmkydWVLUGJLekpSNDAzejdkVGQyQUxYJTJGa1Y1dnN1SlgyVnI3dVhiejE0Qzc3YUREdSUyQkU5QVVWZFg1ZGJPa2EzaXFaJTJCVExjMkR3VVlyZWdBJTNEJTNE',
        '__gsas': 'ID=bc3f500de9911644:T=1664865402:S=ALNI_MYLS1ablE-pUscpqGN-dcbVjZfP5Q',
        'lqstatus': '1664866560|183a1b552eax18f38f2f|oeu2u-2441#buy-2895#buy-2893#er-1778||',
        'tmr_detect': '0%7C1664865414074',
        'sbjs_session': 'pgs%3D4%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.olx.kz%2Fd%2Fobyavlenie%2Frelaks-massazh-IDmVGX2.html',
        'tmr_reqNum': '13',
        'cookieBarSeenV2': 'true',
        'cookieBarSeen': 'true',
        'session_start_date': '1664867230023',
        'onap': '1837feac6f3x27c82913-3-183a1b552eax18f38f2f-19-1664867230',
        '_gat_clientNinja': '1',
    }
    ua = UserAgent()  
    headers = {
        'authority': 'www.olx.kz',
        'accept': '*/*',
        'accept-language': 'ru',
        'authorization': 'Bearer '+tokenus,
        # Requests sorts cookies= alphabetically
        # 'cookie': 'dfp_user_id=bdce835b-79e6-4c25-830e-c8d471635e47-ver2; laquesisff=aut-716#buy-2811#decision-657#euonb-114#euonb-48#euweb-1372#euweb-451#grw-124#kuna-307#oesx-1437#oesx-1643#oesx-645#oesx-867#olxeu-29763#srt-1289#srt-1346#srt-1434#srt-1593#srt-1758#srt-627#srt-633#srt-635#srt-899; __utmz=16996198.1664298437.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.1586618035.1664298437; _gcl_au=1.1.1511600409.1664298437; user_adblock_status=false; lister_lifecycle=1664298438; _hjSessionUser_2218931=eyJpZCI6ImMzNjkxYTM3LTE2ZmQtNWNiNC1iNjM2LTUwNzcwYzAxNjRkOSIsImNyZWF0ZWQiOjE2NjQyOTg0MzY2NzIsImV4aXN0aW5nIjp0cnVlfQ==; __gads=ID=3d9753f37d71d60a:T=1664298436:S=ALNI_Ma4QHqPGhLj71oClMQ5_HYPAYtWkw; mobile_default=desktop; fingerprint=MTI1NzY4MzI5MTsxNjswOzA7MDsxOzA7MDswOzA7MDsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MDsxOzE7MTswOzA7MDswOzE7MDswOzE7MTsxOzE7MTswOzE7MDswOzE7MTsxOzA7MDswOzA7MDswOzE7MDsxOzA7MDswOzA7MDswOzA7MTsxOzA7MTsxOzE7MTswOzE7MDszNDEwNzc3ODI5OzI7MjsyOzI7MjsyOzU7Mjg0ODAwNjQxODsxMzU3MDQxNzM4OzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTswOzA7MDs0MTAwMjE5OTszNDY5MzA2NTUxOzM2OTE3NTk4OTY7Nzg1MjQ3MDI5OzEwMDUzMDEyMDM7MTkyMDsxMDgwOzI0OzI0OzM2MDszNjA7MzYwOzM2MDszNjA7MzYwOzM2MDszNjA7MzYwOzM2MDszNjA7MzYwOzM2MDszNjA7MzYwOzM2MDszNjA7MzYwOzM2MDszNjA7MDswOzA=; from_detail=0; ldTd=true; __utmc=16996198; newrelic_cdn_name=CF; dfp_segment=%5B%5D; laquesis=buy-2893@b#buy-2895@a#decision-206@b#decision-377@b#decision-536@a#decision-790@b#er-1708@a#er-1778@b#euonb-493@a#f8nrp-1218@c#jobs-3717@b#jobs-3837@c#jobs-3845@a#jobs-4145@d#oesx-1547@a#oeu2u-2441@b; laquesissu=297@ad_page|1#297@reply_phone_1step|1; _ym_uid=1664865360100642542; _ym_d=1664865360; _ym_visorc=w; __utma=16996198.1586618035.1664298437.1664325010.1664865362.3; __utmt=1; _gid=GA1.2.2079208551.1664865363; _ym_isad=2; __gpi=UID=00000b5183101bf5:T=1664298436:RT=1664865364:S=ALNI_MbAW5lfTC9uj-4tLfeOsb6NVS69FQ; _hjIncludedInSessionSample=0; _hjSession_2218931=eyJpZCI6ImM5ZmYzMjI0LWNiYzYtNDk4Yi1iYmM1LTYzNWEzYmNkMTUzMSIsImNyZWF0ZWQiOjE2NjQ4NjUzNjQ2NjMsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; tmr_lvid=d05bc2af964325b0c9a27f861a457a95; tmr_lvidTS=1664865365066; PHPSESSID=01n7aiggq1101sqm26nvi5elqg; x-device-id=q2ympu0vz6gpe1%3A1664865382935; user_id=381910128; lang=ru; access_token=61361e0a38499289a8ba3308d62b0ef510fca6e3; refresh_token=f5e349f888f72f4315a8d947e354e69758145faf; deviceGUID=0b2dee4a-0f03-48d1-a8e6-9622dbef4b32; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2022-10-04%2012%3A36%3A27%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.olx.kz%2Fd%2Fmyaccount%2F%23login%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.olx.kz%2Faccount%2F%3Fref%255B0%255D%255Baction%255D%3Dmyaccount%26ref%255B0%255D%255Bmethod%255D%3Dindex; sbjs_first_add=fd%3D2022-10-04%2012%3A36%3A27%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.olx.kz%2Fd%2Fmyaccount%2F%23login%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.olx.kz%2Faccount%2F%3Fref%255B0%255D%255Baction%255D%3Dmyaccount%26ref%255B0%255D%255Bmethod%255D%3Dindex; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%206.1%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F104.0.0.0%20Safari%2F537.36; user_business_status=private; _gat=1; __diug=true; criteo_hashed_email=d41d8cd98f00b204e9800998ecf8427e; criteo_hashed_email_15=d41d8cd98f00b204e9800998ecf8427e; __utmb=16996198.2.10.1664865362; cto_bundle=7D1_F19rY2ZBSHdKelhWMXYzNlpRJTJCQzJBYjAwdndBTEhlZkxvUHRCdUQ2UUZKaEtJZlJmVERVRjVhczZNZUgzVHUlMkZWVHczQnBsVmkydWVLUGJLekpSNDAzejdkVGQyQUxYJTJGa1Y1dnN1SlgyVnI3dVhiejE0Qzc3YUREdSUyQkU5QVVWZFg1ZGJPa2EzaXFaJTJCVExjMkR3VVlyZWdBJTNEJTNE; __gsas=ID=bc3f500de9911644:T=1664865402:S=ALNI_MYLS1ablE-pUscpqGN-dcbVjZfP5Q; lqstatus=1664866560|183a1b552eax18f38f2f|oeu2u-2441#buy-2895#buy-2893#er-1778||; tmr_detect=0%7C1664865414074; sbjs_session=pgs%3D4%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.olx.kz%2Fd%2Fobyavlenie%2Frelaks-massazh-IDmVGX2.html; tmr_reqNum=13; cookieBarSeenV2=true; cookieBarSeen=true; session_start_date=1664867230023; onap=1837feac6f3x27c82913-3-183a1b552eax18f38f2f-19-1664867230; _gat_clientNinja=1',
        'friction-token': token,
        'referer': url,
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent':f'{ua.random}' ,
        'x-client': 'DESKTOP',
        'x-device-id': '0b2dee4a-0f03-48d1-a8e6-9622dbef4b32',
        'x-platform-type': 'mobile-html5',
    }
    f = open('http_kz.txt', 'r')
    l = [line.strip() for line in f] 
    random.shuffle(l)
    proxies = {"http":f"{':'.join(l[0].split(':')[:-2])}"}
    auth = HTTPProxyAuth(f"{l[0].split(':')[-2:][0]}", f"{l[0].split(':')[-2:][1]}")      
     
    phone = requests.get(f'https://www.olx.kz/api/v1/offers/{id_add}/limited-phones/', proxies=proxies, auth=auth,cookies=cookies, headers=headers).json()
    time.sleep(random.randint(6,9))
    print(phone)
    try:
      phone = "+"+phone.get("data").get("phones")[0].replace(" ","").replace("-","").replace("+","")
      return phone
    except:
      return None





def get_params(link):
   params_const = {
    'offset': '0',
    'limit': '40',
    'filter_refiners': 'spell_checker',
   }
   try:
      #Получаем значения для категории
      if link[-2:] == "d/":
         link =link.split("https://www.olx.kz/")[1][:-1].replace("d/",'').replace("kk/",'').replace("/",",")
      else:   
         link = link.split("https://www.olx.kz/")[1].replace("d/",'').replace("kk/",'').replace("/",",")
      #Проверка
      if link[-1] == "/":
         link = link[:-1]

      #Генирация ссылки
      url = "https://www.olx.kz/api/v1/friendly-links/query-params/"+link

      f = open('http_kz.txt', 'r')
      l = [line.strip() for line in f] 
      random.shuffle(l)
      proxies = {"http":f"{':'.join(l[0].split(':')[:-2])}"}
      auth = HTTPProxyAuth(f"{l[0].split(':')[-2:][0]}", f"{l[0].split(':')[-2:][1]}")  


      response = requests.get(url, proxies=proxies, auth=auth).json()

      #Возврат params для запроса
      params = response.get("data")
      params.update(params_const)
      #Проверка если ответа нету
      if params is None:
         return "Введены некорректные данные."
      else:
         return params
   except Exception as e:
      print(e)
      return "Введены некорректные данные."


def generate_json(params,link,id,token):
   ua = UserAgent() #Fake user Agent
   headers = {
      'authority': 'www.olx.kz',
      'accept': '*/*',
      'accept-language': 'ru',
      'authorization': 'Bearer '+token,

      'dnt': '1',
      'referer': link,
      'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': f'{ua.random}',
      'x-client': 'DESKTOP',
      'x-device-id': 'd5ac779d-8d4e-4256-b3a6-8b1cf700e218',
      'x-platform-type': 'mobile-html5',
   }

   #Создание json'a
   response = requests.get('https://www.olx.kz/api/v1/offers/', params=params, headers=headers).json()
   items = response.get("data")
   with open(f'result_{id}.json','w', encoding="utf-8") as file:
      json.dump(items,file,indent=4,ensure_ascii=False)#Сохранение json

def get_information_for_json(id,arr_stop,token,text,text2,link):
   try:
      with open(f'result_{id}.json', encoding="utf-8") as f:
         Information = json.load(f)
         for item in Information:
            if arr_stop[id] == "False": #! Поменять на arrstop
               break
            else:
               #Проверка есть ли телефон на обьяве

               if item.get("contact").get("phone") == True:
                  curent_time = item.get("last_refresh_time")
                  #получение даты с json
                  data_MosYear_OLX = "-".join(curent_time.split("T")[0].split("-")[:-1])
                  day_OLX = curent_time.split("T")[0].split("-")[-1:][0]
                  #Получение сегодн. даты
                  data_MosYear_Current = datetime.now().strftime("%Y-%m")
                  day_curr = datetime.now().strftime("%d")
                  #Проверка по времени
                  if data_MosYear_OLX == data_MosYear_Current:
                     if abs(int(day_curr)-int(day_OLX)) <= 2:
                        #Получение данных
                        create_time = item.get("last_refresh_time").replace("T"," ").split("+")[0]
                        title = item.get("title")
                        url = item.get("url")
                        price = item.get("params")[0].get("value").get("label")
                        name_user = item.get("user").get("name")
                        create_user = item.get("user").get("created").replace("T"," ").split("+")[0]
                        location = item.get("location").get("city").get("name") + " " + item.get("location").get("region").get("name")
                        id_user = item.get("user").get("id")
                        id_add = item.get("id")
                        if 1==1:
                           url_to_photo = item.get("photos")[0].get("link")
                           width = str(item.get("photos")[0].get("width"))
                           height = str(item.get("photos")[0].get("height"))
                           url_to_photo = url_to_photo.replace("width",width).replace("height",height).replace("{","").replace("}","")

                           response = urlopen(url_to_photo)
                           content = response.read()
                           file = open('photo_'+str(id)+'.png', 'wb')
                           file.write(content)
                           file.close()

                        if url_to_photo is not None:
                           phone = get_phone(id_add,url,token)
                           if phone is None:
                              bot.send_message(id,"<b>❌ Токен неверный</b>", reply_markup=Button.menu_users_telebot ,parse_mode='HTML')
                              break
                           else:
                              try:
                                 bot.send_photo(id,open("photo_{}.png".format(id), 'rb'),\
f"<b>⛓ Название товара</b> : {title} \n\n\
<b>💵 Цена товарa</b> : {price} \n\
<b>🏢 Город</b> : {location}\n \
<b>👤 Ник пользователя</b> : {name_user} \n \
<b>🕓 Дата выложения товара</b> : {create_time} \n\n \
<b>⚙️ Номер телефона</b> : {phone} \n\n \
<b>🔗 Ссылка на товар</b> : <a href ='{url}'>Ссылка</a> \n\n"\
,parse_mode='HTML', reply_markup=Button.but_for_phone(phone,text,link,text2,title.replace(" ","+")))#send photo
                              except:
                                 pass
         if arr_stop[id] != "False":
            bot.send_message(id,"<b>✅ Парс по ссылке: {} \nЗакончился</b>".format(link) ,parse_mode='HTML')
   except Exception as e:
      print(e)
      pass



def main(link,id,arr_stop,text,text2,tokenus):
   #Получение params для json
   params = get_params(link)
   #Проверка
   if params != "Введены некорректные данные.":
      generate_json(params,link,id,tokenus)
      #-------
      get_information_for_json(id,arr_stop,tokenus,text,text2,link)
   else:
      bot.send_message(id,"<b>❌ Неверная ссылка</b>", reply_markup=Button.menu_users_telebot ,parse_mode='HTML')

