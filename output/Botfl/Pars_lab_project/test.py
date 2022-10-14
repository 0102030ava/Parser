import requests
import random
import mysql.connector
from bs4 import BeautifulSoup
from requests.auth import HTTPProxyAuth


# config = {                                     
#          'user': 'Nursyka',                     
#          'password': '3y@CB%8D)sNkv56!Bj+9',         
#          'host': 'DESKTOP-S95L17M',                
#          'port': '3306',                    
#          'database': "parsfl",                  
#                }
# print("Connect SQL Done")                                  
# db = mysql.connector.connect(**config)  
# cursor = db.cursor()   
# db.reconnect()
# cursor.execute('SELECT `ID` FROM users_data ;')
# information_user = cursor.fetchall()

# for i in information_user:
#    print(i[0])




# def proxy_request( url, **kwargs):
#    a = 0
#    with open('http.txt', 'r') as f:
      
#       proxys = f.read().splitlines()
#       for proxy in proxys:
#          proxies = {
#       'http': 'http://'+proxy,
#       'https': 'http://'+proxy,
#          }
#          try:
#             response = requests.get( url, proxies=proxies,timeout=5)
#             soup = BeautifulSoup(response.text , 'lxml')#сonnect to  link
#             ip = soup.find(class_ = "ip").text.strip()
#             city  = soup.find(class_ = "result").text.strip()
#             print(f"ip :{ip} : city :{city} : proxy:{proxy}")
#          except:
#             pass

# def proxy_request1( url, **kwargs):

#       proxies = {"http":"163.198.111.52:8000"}
#       auth = HTTPProxyAuth("GGPLHq", "ryFn17")
#       r = requests.get(url, proxies=proxies, auth=auth)      
#       soup = BeautifulSoup(r.text , 'lxml')#сonnect to  link
#       ip = soup.find(class_ = "ip").text.strip()
#       city  = soup.find(class_ = "result").text.strip()
#       print(f"ip :{ip} : city :{city} : proxy:{proxies}")
 
   
# proxy_request1("https://2ip.ua/ru/")




# config = {                                     
#          'user': 'Nursyka',                     
#          'password': '3y@CB%8D)sNkv56!Bj+9',         
#          'host': 'DESKTOP-S95L17M',                
#          'port': '3306',                    
#          'database': "parsfl",                  
#                }
# print("Connect SQL Done")                                  
# db = mysql.connector.connect(**config)  
# cursor = db.cursor()  

# cursor.execute('SELECT `UserName` FROM users_data ;')
# information_user = cursor.fetchall()
# for i in information_user:
#    print("@"+i[0])
f = open('http.txt', 'r')
l = [line.strip() for line in f] 
random.shuffle(l)
print(l)
