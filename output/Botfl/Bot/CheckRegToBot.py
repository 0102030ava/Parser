import mysql.connector
def User_Register(ID,db,cursor):
   try:
      db.reconnect()
      cursor.execute('SELECT ID FROM ID_users WHERE id = "'+str(ID)+'" ;')
      return cursor.fetchone()
   except Exception as E:
      pass
