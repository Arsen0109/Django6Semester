from tkinter import *
from CRUD import car_crud, trademark_crud, model_crud
import psycopg2
import mysql.connector


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
    mysql_conn = mysql.connector.connect(host='localhost', user='root', password='@rsen2003', db='cartrademark')
    postgres_conn = psycopg2.connect(host='localhost', user='postgres', password='@rsen2003', dbname='cartrademarks')

    # Retrieve data from MySQL tables
    mysql_cursor = mysql_conn.cursor()

    # Retrieve data from first table
    mysql_cursor.execute("SELECT * FROM cartrademarks")
    table1_data = mysql_cursor.fetchall()

    # Retrieve data from second table
    mysql_cursor.execute("SELECT * FROM cars")
    table2_data = mysql_cursor.fetchall()

    # Retrieve data from third table
    mysql_cursor.execute("SELECT * FROM models")
    table3_data = mysql_cursor.fetchall()

    # Insert data into PostgreSQL tables
    postgres_cursor = postgres_conn.cursor()

    # print(table1_data)
    postgres_cursor.execute("TRUNCATE cartrademarks, cars, models")
    # Insert data into first table
    for row in table1_data:
        postgres_cursor.execute(
            "INSERT INTO cartrademarks(trademark_id, trademark) VALUES (%s, %s)",
            row
        )
    postgres_conn.commit()

    # Insert data into second table
    for row in table2_data:
        postgres_cursor.execute(
            "INSERT INTO cars(car_id, make, year, price, trademark_id) VALUES (%s, %s, %s, %s, %s)",
            (row[0], row[1], row[3], row[4], row[5])
        )
    postgres_conn.commit()

    # Insert data into third table
    for row in table3_data:
        postgres_cursor.execute(
            "INSERT INTO models(model_id, model, car_id) VALUES (%s, %s, %s)",
            row
        )
    postgres_conn.commit()

    # Update cars table with foreign keys
    for row in table2_data:
        postgres_cursor.execute(
            f"UPDATE cars SET model_id={row[2]} WHERE car_id={row[0]}"
        )
    postgres_conn.commit()

    # Close connections
    mysql_cursor.close()
    mysql_conn.close()

    postgres_cursor.close()
    postgres_conn.close()


class AdminInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Admin")
        self.init_widgets()

    def init_widgets(self):
        car_interface_button = Button(self.master, text="Car CRUD interface", command=call_car_crud,
                                      width=20, height=3)
        car_interface_button.grid(row=0, column=0)

        trademark_interface_button = Button(self.master, text="Trademark CRUD interface", width=20, height=3,
                                            command=call_trademark_crud)
        trademark_interface_button.grid(row=1, column=0)

        model_interface_button = Button(self.master, text="Model CRUD interface", width=20, height=3,
                                        command=call_model_crud)
        model_interface_button.grid(row=2, column=0)

        transfer_db_button = Button(self.master, text="Transfer from MySQL to PostgreSQL", width=30, height=3,
                                    command=transfer_data_to_mysql)
        transfer_db_button.grid(row=1, column=2)


root = Tk()
admin_interface = AdminInterface(root)
root.mainloop()
