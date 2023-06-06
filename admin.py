from tkinter import *
from CRUD import car_crud, trademark_crud, model_crud
import psycopg2
import mysql.connector
import sqlite3


def call_car_crud():
    car_crud_interface = Tk()
    car_crud.CarAdmin(car_crud_interface)
    car_crud_interface.mainloop()


def call_trademark_crud():
    trademark_crud_interface = Tk()
    trademark_crud.TrademarkAdmin(trademark_crud_interface)
    trademark_crud_interface.mainloop()


def call_model_crud():
    model_crud_interface = Tk()
    model_crud.ModelAdmin(model_crud_interface)
    model_crud_interface.mainloop()


def transfer_data_to_mysql():
    mysql_conn = mysql.connector.connect(host='localhost', user='root', password='password', db='cartrademark')
    postgres_conn = psycopg2.connect(host='localhost', user='postgres', password='@rsen2003', dbname='cartrademarks')

    mysql_cursor = mysql_conn.cursor()

    mysql_cursor.execute("SELECT * FROM cartrademarks")
    table1_data = mysql_cursor.fetchall()

    mysql_cursor.execute("SELECT * FROM cars")
    table2_data = mysql_cursor.fetchall()

    mysql_cursor.execute("SELECT * FROM models")
    table3_data = mysql_cursor.fetchall()

    postgres_cursor = postgres_conn.cursor()

    postgres_cursor.execute("TRUNCATE cartrademarks, cars, models")
    for row in table1_data:
        postgres_cursor.execute(
            "INSERT INTO cartrademarks(trademark_id, trademark) VALUES (%s, %s)",
            row
        )
    postgres_conn.commit()

    for row in table2_data:
        postgres_cursor.execute(
            "INSERT INTO cars(car_id, make, year, price, trademark_id) VALUES (%s, %s, %s, %s, %s)",
            (row[0], row[1], row[3], row[4], row[5])
        )
    postgres_conn.commit()

    for row in table3_data:
        postgres_cursor.execute(
            "INSERT INTO models(model_id, model, car_id) VALUES (%s, %s, %s)",
            row
        )
    postgres_conn.commit()

    for row in table2_data:
        postgres_cursor.execute(
            f"UPDATE cars SET model_id={row[2]} WHERE car_id={row[0]}"
        )
    postgres_conn.commit()

    mysql_cursor.close()
    mysql_conn.close()

    postgres_cursor.close()
    postgres_conn.close()


def transfer_data_to_sqlite():
    postgres_conn = psycopg2.connect(host='localhost', user='postgres', password='@rsen2003', dbname='cartrademarks')
    sqlite_conn = sqlite3.connect('cartrademarks.db')

    postgres_cursor = postgres_conn.cursor()
    sqlite_cursor = sqlite_conn.cursor()

    sqlite_cursor.execute("DROP TABLE IF EXISTS cars")
    sqlite_conn.commit()

    sqlite_cursor.execute("CREATE TABLE IF NOT EXISTS cars(car_id INT PRIMARY KEY, model VARCHAR(40),"
                          "price INT)")
    sqlite_conn.commit()

    postgres_cursor.execute("SELECT cars.car_id, models.model, cars.price FROM "
                            "cars JOIN models ON cars.model_id = models.model_id WHERE cars.car_id IN "
                            "(SELECT car_id FROM cars WHERE cars.year > 2019);")
    table11_data = postgres_cursor.fetchall()

    for row in table11_data:
        sqlite_cursor.execute(
            "INSERT INTO cars(car_id, model, price) VALUES (?, ?, ?)", (row[0], row[1], row[2])
        )
    sqlite_conn.commit()

    postgres_cursor.close()
    postgres_conn.close()

    print(sqlite_cursor.execute("SELECT * FROM cars").fetchall())
    sqlite_cursor.close()
    sqlite_conn.close()


class AdminInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Admin")
        self.master["bg"] = 'blue'
        self.init_widgets()

    def init_widgets(self):
        Label(self.master, text='Головна сторінка', font='Arial 24', bg='yellow').grid(row=0, column=1)

        car_interface_button = Button(self.master, text="Операції CRUD з авто", command=call_car_crud, height=2,
                                      bg='yellow')
        car_interface_button.grid(row=1, column=0)

        trademark_interface_button = Button(self.master, text="Операції CRUD з компаніями", height=2,
                                            command=call_trademark_crud, bg='yellow')
        trademark_interface_button.grid(row=1, column=1)

        model_interface_button = Button(self.master, text="Операції CRUD з моделями авто", height=2,
                                        command=call_model_crud, bg='yellow')
        model_interface_button.grid(row=1, column=2)

        transfer_db_button = Button(self.master, text="Перенести дані з MySQL до PostgreSQL", height=2,
                                    command=transfer_data_to_mysql, bg='yellow')
        transfer_db_button.grid(row=2, column=0)

        transfer_db_button = Button(self.master, text="Перенести дані з PostgreSQL до SQLite", height=2,
                                    command=transfer_data_to_sqlite, bg='yellow')
        transfer_db_button.grid(row=2, column=2)


root = Tk()
admin_interface = AdminInterface(root)
root.mainloop()
