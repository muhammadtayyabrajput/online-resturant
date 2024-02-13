from models import user, orders, orders_items, contact
import pymysql

class SMDBHandler:
    def __init__(self, host, user, password, database):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

    def registerUser(self, user, contact):
        mydb = None
        mydbCursor = None
        inserted = False
        try:
            mydb = pymysql.connect(host=self.__host, user=self.__user, password=self.__password,
                                   database=self.__database)
            mydbCursor = mydb.cursor()

            # user table
            sql = "INSERT INTO user (username,email, password) VALUES (%s, %s,%s)"
            args = (user.username, user.email, user.password)
            mydbCursor.execute(sql, args)

            mydb.commit()

            # contact table
            sql = "INSERT INTO contact (email, address,phone, city) VALUES (%s,%s, %s, %s)"
            args = (contact.email, contact.address, contact.phone, contact.city)
            mydbCursor.execute(sql, args)

            mydb.commit()
            inserted = True
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor is not None:
                mydbCursor.close()

            if mydb is not None:
                mydb.close()
            return inserted

    def login(self, email, password):
        mydb = None
        mydbCursor = None
        exist = False
        try:
            # Get DB Connection
            mydb = pymysql.connect(host=self.__host, user=self.__user, password=self.__password,
                                   database=self.__database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            sql = "SELECT username FROM user WHERE email=%s AND password=%s"
            args = (email, password)
            mydbCursor.execute(sql, args)
            row = mydbCursor.fetchone()
            if row is not None:
                exist = True

        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor is not None:
                mydbCursor.close()

            if mydb is not None:
                mydb.close()
            return exist

    def validateUser(self, user):
        mydb = None
        mydbCursor = None
        exist = False
        try:
            mydb = pymysql.connect(host=self.__host, user=self.__user, password=self.__password,
                                   database=self.__database)
            mydbCursor = mydb.cursor()
            sql = "SELECT username FROM user WHERE email=%s AND password=%s"
            args = (user.email, user.password)
            mydbCursor.execute(sql, args)
            row = mydbCursor.fetchone()
            if row is not None:
                exist = True

        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor is not None:
                mydbCursor.close()

            if mydb is not None:
                mydb.close()
            return exist

    def save_cart_info(self, orders_item):
        mydb = None
        mydbCursor = None
        try:
            mydb = pymysql.connect(host=self.__host, user=self.__user, password=self.__password,
                                   database=self.__database)
            mydbCursor = mydb.cursor()
            sql = "SELECT MAX(order_id)  FROM orders;"
            mydbCursor.execute(sql)
            result = mydbCursor.fetchone()
            # print(result)
            order_id = result[0]
            query = "INSERT INTO order_items (order_id,name, price, quantity) VALUES (%s,%s, %s, %s)"
            mydbCursor.execute(query, (order_id, orders_item.item_name, orders_item.price, orders_item.quantity))
            # sql = "SELECT username FROM user WHERE email=%s AND password=%s"
            # args = (user.email, user.password)
            # mydbCursor.execute(sql, args)
            # row = mydbCursor.fetchone()
            mydb.commit()
            inserted = True
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor is not None:
                mydbCursor.close()

            if mydb is not None:
                mydb.close()
            return inserted

    def orderInfo(self, order):
        mydb = None
        mydbCursor = None
        try:
            mydb = pymysql.connect(host=self.__host, user=self.__user, password=self.__password,
                                   database=self.__database)
            mydbCursor = mydb.cursor()
            email = order.user_email
            total_amount = order.total_amount
            query = "INSERT INTO orders (user_email,total_amount) VALUES (%s, %s)"
            mydbCursor.execute(query, (email, total_amount))
            # sql = "SELECT username FROM user WHERE email=%s AND password=%s"
            # args = (user.email, user.password)
            # mydbCursor.execute(sql, args)
            # row = mydbCursor.fetchone()
            mydb.commit()
            inserted = True
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor is not None:
                mydbCursor.close()

            if mydb is not None:
                mydb.close()
            return inserted






    # Delete user data including contact information
    def delete_user_data(self, email):
        mydb = None
        mydbCursor = None
        try:
            mydb = pymysql.connect(host=self.__host, user=self.__user, password=self.__password,
                                database=self.__database)
            mydbCursor = mydb.cursor()
            args = (email,)
            #Getting order_id from orders table

            sql = "SELECT order_id FROM orders WHERE user_email=%s"
            
            mydbCursor.execute(sql, args)
            row = mydbCursor.fetchall()
            print(row)
            for item in row:
                # Delete order_items information
                print("in for loop of order_item")
                sql = "DELETE FROM order_items WHERE order_id=%s"
                value=(item[0],)
                mydbCursor.execute(sql, value)

            print("deleting order info")
            # Delete orders information
            sql = "DELETE FROM orders WHERE user_email=%s"
            
            mydbCursor.execute(sql, args)

            print("deleting contact info")
            # Delete contact information
            sql = "DELETE FROM contact WHERE email=%s"
            
            mydbCursor.execute(sql, args)

            # Delete user information
            sql = "DELETE FROM user WHERE email=%s"
            mydbCursor.execute(sql, args)

            mydb.commit()
            return True

        except Exception as e:
            print(str(e))
            return False

        finally:
            if mydbCursor is not None:
                mydbCursor.close()

            if mydb is not None:
                mydb.close()

    # Update user and contact information
    def update_user_data(self, email, username, password, phone, address, city):
        mydb = None
        mydbCursor = None
        try:
            mydb = pymysql.connect(host=self.__host, user=self.__user, password=self.__password,
                                database=self.__database)
            mydbCursor = mydb.cursor()

            # Update user information
            sql = "UPDATE user SET username=%s, password=%s WHERE email=%s"
            args = (username, password, email)
            mydbCursor.execute(sql, args)

            # Update contact information
            sql = "UPDATE contact SET address=%s, phone=%s, city=%s WHERE email=%s"
            args = (address, phone, city, email)
            mydbCursor.execute(sql, args)

            mydb.commit()
            return True

        except Exception as e:
            print(str(e))
            return False

        finally:
            if mydbCursor is not None:
                mydbCursor.close()

            if mydb is not None:
                mydb.close()



    
    def order_details(self):
        mydb = None
        mydbCursor = None
        try:
            mydb = pymysql.connect(host=self.__host, user=self.__user, password=self.__password,
                                   database=self.__database)
            mydbCursor = mydb.cursor()
            email="bcsf20a022@pucit.edu.pk"
            sql = "SELECT order_id FROM orders WHERE user_email=%s"
            mydbCursor.execute(sql, email)
            row = mydbCursor.fetchall()
            order_details=[]
            for item in row:
                print("in for loop of order_item")
                sql = "SELECT * from order_items WHERE order_id=%s"
                value=(item[0],)
                mydbCursor.execute(sql, value)
                order_details.append(mydbCursor.fetchall())
            # sql = "SELECT username FROM user WHERE email=%s AND password=%s"
            # args = (user.email, user.password)
            # mydbCursor.execute(sql, args)
            # row = mydbCursor.fetchone()
           
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor is not None:
                mydbCursor.close()

            if mydb is not None:
                mydb.close()
            return order_details



    def donate_ampunt(self, email, name,phone,amount,account):
        mydb = None
        mydbCursor = None
        inserted = False
        try:
            mydb = pymysql.connect(host=self.__host, user=self.__user, password=self.__password,
                                   database=self.__database)
            mydbCursor = mydb.cursor()

            # user table
            sql = "INSERT INTO donations (email, name,phone,amount,account) VALUES (%s, %s,%s, %s,%s)"
            args = ( email, name,phone,amount,account)
            mydbCursor.execute(sql, args)
            mydb.commit()
            inserted = True
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor is not None:
                mydbCursor.close()

            if mydb is not None:
                mydb.close()
            return inserted