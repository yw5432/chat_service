import pymysql


db = pymysql.connect(
    host="localhost",
    user="root",
    password="123456",
    database="chat_service"
)