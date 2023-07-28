# セッション変数の取得
from setting import session
# Userモデルの取得
from user import *
cnx = None
import mysql.connector
conn=mysql.connector.connect(host='127.0.0.1',user='root',password="Choco12.16haru")
from sql import retu
# DBにレコードの追加
user = User()

# Userテーブルのnameカラムをすべて取得
# users = session.query(User).all()
# for user in users:
#     print(user.id)

#retu()

try:
    cnx = mysql.connector.connect(
        user='root',  # ユーザー名
        password='Choco12.16haru',  # パスワード
        host='127.0.0.1',  # ホスト名(IPアドレス）
        database='kyuri'  # データベース名
    )

    if cnx.is_connected:
        print("Connected!")

    cursor = cnx.cursor(buffered=True)

    # cursor.execute("DROP TABLE IF EXISTS hantei")#データベースを消すやつ

    sql = 'SELECT count(id) FROM '+'hantei'
    cursor.execute(sql)
    result = cursor.fetchall()
    print (result)

    record_max = result[0][0]
    print ('登録されている総レコード数 ==> ', record_max)
        

    cursor.close()

except Exception as e:
    print(f"Error Occurred: {e}")


finally:
    if cnx is not None and cnx.is_connected():
        conn.close()

for i in range(1,record_max+1):
    users = session.query(User).\
    filter(User.id==i).\
    all()

for i in range(1,record_max+1):
    users = session.query(User).\
    filter(User.id==i).\
    all()
    a=[]
    a[i]=users.A
    print(a[i])
    #for user in users:
    #    print(user.id,user.A,user.B,user.C)