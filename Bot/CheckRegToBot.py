import mysql.connector
import Information
def User_Register(ID,db,cursor):
   try:
      db.reconnect()
      cursor.execute('SELECT ID FROM users_data WHERE id = "'+str(ID)+'" ;')
      return cursor.fetchone()
   except Exception as E:
      pass


