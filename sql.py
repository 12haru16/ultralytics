import mysql.connector
conn=mysql.connector.connect(host='127.0.0.1',user='root',password="Choco12.16haru")
cnx = None

def database_create():
    try:
        cnx = mysql.connector.connect(
            user='root',  # ユーザー名
            password='Choco12.16haru',  # パスワード
            host='127.0.0.1'  # ホスト名(IPアドレス）
        )

        cursor = cnx.cursor()

        cursor.execute("CREATE DATABASE kyuri")

        cursor.execute("SHOW DATABASES")
        print(cursor.fetchall())

        cursor.close()

    except Exception as e:
        print(f"Error Occurred: {e}")

    finally:
        if cnx is not None and cnx.is_connected():
            cnx.close()

def tabel_create():
    try:
        cnx = mysql.connector.connect(
            user='root',  # ユーザー名
            password='Choco12.16haru',  # パスワード
            host='127.0.0.1',  # ホスト名(IPアドレス）
            database='kyuri'  # データベース名
        )

        if cnx.is_connected:
            print("Connected!")

        cursor = cnx.cursor()

        # cursor.execute("DROP TABLE IF EXISTS hantei")#データベースを消すやつ

        sql = '''
        CREATE TABLE hantei (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        magari VARCHAR(50) NULL,
        sakibutori VARCHAR(50) NULL,
        seijyo VARCHAR(50) NULL
        )'''
        cursor.execute(sql)

        cursor.execute("SHOW TABLES")
        print(cursor.fetchall())

        cursor.close()

    except Exception as e:
        print(f"Error Occurred: {e}")


    finally:
        if cnx is not None and cnx.is_connected():
            conn.close()


def data_insert(A,B,C):
    try:
        cnx = mysql.connector.connect(
            user='root',  # ユーザー名
            password='Choco12.16haru',  # パスワード
            host='127.0.0.1',  # ホスト名(IPアドレス）
            database='kyuri'  # データベース名
        )

        if cnx.is_connected:
            print("Connected!")

        cursor = cnx.cursor()

        sql = ('''
        INSERT INTO hantei
            (magari, sakibutori, seijyo)
        VALUES 
            (%s, %s, %s)
        ''')

        data = [
            (A, B, C)
        ]

        cursor.executemany(sql, data)
        cnx.commit()

        
        print(f"{cursor.rowcount} records inserted.")

        cursor.close()

    except Exception as e:
        print(f"Error Occurred: {e}")

    finally:
        if cnx is not None and cnx.is_connected():
            cnx.close()

def retu():
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



#tabel_create()