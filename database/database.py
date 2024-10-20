import mysql.connector
from datetime import datetime

def insert_data(user,password,email,api,path):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="hobbists"
    )

    mycursor = mydb.cursor()

    sql = f"INSERT INTO users(id,username,password,email,created_at,api_key,profile_path) VALUES(0,'{user}','{password}','{email}','{datetime.today().strftime('%Y-%m-%d')}','{api}','{path}');"
    mycursor.execute(sql)

    mydb.commit()
    mydb.close()

    print(mycursor.rowcount, "record inserted.")

def reterieve_username(username):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="hobbists"
    )

    mycursor = mydb.cursor()

    mycursor.execute(f"SELECT * FROM users where username='{username}';")

    myresult = mycursor.fetchall()

    #[(3, 'root', 'root', 'root@root', datetime.datetime(2024, 9, 15, 0, 0), 'root', '/KSfMRgd2EooJb2.jpg')], ... 

    return myresult 

def create_interest_database_for_user(username):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="hobbists"
    )

    mycursor = mydb.cursor()
    mycursor.execute(f'create table {username}_interests(interests varchar(20) PRIMARY KEY);')
    mydb.commit()
    mydb.close()

def new_interest(username,value):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="hobbists"
    )

    mycursor = mydb.cursor()
    query = f'insert into {username}_interests(interests) values("{value}");'
    print(query)
    mycursor.execute(query)
    mydb.commit()
    mydb.close()

def find_interests(username):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="hobbists"
    ) 

    mycursor = mydb.cursor()

    mycursor.execute(f"SELECT * FROM {username}_interests;")

    myresult = mycursor.fetchall()

    return myresult

def delete_interest(username,interest):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="hobbists"
    ) 

    mycursor = mydb.cursor()
    mycursor.execute(f'delete from {username}_interests where interests="{interest}"')
    mydb.commit()
    mydb.close()
