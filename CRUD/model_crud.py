import tkinter as tk
import tkinter.messagebox as messagebox
import mysql.connector


class Model:
    def __init__(self, model_name, car_id):
        self.model_name = model_name
        self.car_id = car_id
        self.model_id = None

    def __str__(self):
        return f"{self.model_id} {self.model_name} {self.car_id}"


class ModelDB:
    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost', user='root', password='@rsen2003', db='cartrademark')
        self.mysql_cursor = self.conn.cursor()

    def add_model(self, model):
        try:
            self.mysql_cursor.execute(f"INSERT INTO models(model, car_id) VALUES(%s, %s)",
                                      (model.model_name, model.car_id))
            self.conn.commit()
        except():
            self.mysql_cursor.execute(f"INSERT INTO models(model) VALUES(%s)", tuple([model.model_name]))
            self.conn.commit()

    def get_all_models(self):
        self.mysql_cursor.execute("SELECT * FROM models")
        rows = self.mysql_cursor.fetchall()
        models = []
        for row in rows:
            model = Model(row[1], row[2])
            model.model_id = row[0]
            models.append(model)
        return models

    def get_model_by_id(self, model_id):
        self.mysql_cursor.execute(f"SELECT * FROM models WHERE model_id={model_id}")
        row = self.mysql_cursor.fetchone()
        if row:
            model = Model(row[1], row[2])
            model.model_id = row[0]
            return model
        else:
            return None

    def update_model(self, model, model_id):
        self.mysql_cursor.execute(f"UPDATE models SET model=%s, car_id=%s WHERE model_id=%s",
                                  (model.model_name, model.car_id, model_id))
        self.conn.commit()

    def delete_model(self, model_id):
        self.mysql_cursor.execute(f"DELETE FROM models WHERE model_id={model_id}")
        self.conn.commit()


class ModelAdmin:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Admin")
        self.model_listbox = tk.Listbox(self.master, width=40, height=20)
        self.model_entry = tk.Entry(self.master)
        self.car_id_entry = tk.Entry(self.master)
        self.model_id_entry = tk.Entry(self.master)
        self.info_label = tk.Label(self.master, font="Arial 10")
        self.init_widgets()
        self.fill_model_listbox()

    def init_widgets(self):
        tk.Label(self.master, text="Model CRUD:", font="Arial 10 bold").grid(row=0, column=0)

        tk.Label(self.master, text="Model").grid(row=1, column=0)
        self.model_entry.grid(row=1, column=1)

        tk.Label(self.master, text="Car_ID").grid(row=2, column=0)
        self.car_id_entry.grid(row=2, column=1)

        tk.Label(self.master, text="Model_ID").grid(row=3, column=0)
        self.model_id_entry.grid(row=3, column=1)

        self.model_listbox.grid(row=4, column=0, columnspan=2)
        self.model_listbox.bind("<<ListboxSelect>>", self.on_select_model)

        get_button = tk.Button(self.master, text="Get model", command=self.show_model_by_id)
        get_button.grid(row=3, column=2)

        add_button = tk.Button(self.master, text="Add", command=self.add_model)
        add_button.grid(row=7, column=0)

        update_button = tk.Button(self.master, text="Update", command=self.update_model)
        update_button.grid(row=7, column=1)

        delete_button = tk.Button(self.master, text="Delete", command=self.delete_model)
        delete_button.grid(row=7, column=2)

        clear_button = tk.Button(self.master, text="Clear", command=self.clear_form)
        clear_button.grid(row=7, column=3)

        self.info_label.grid(row=6, column=1)

    def fill_model_listbox(self):
        self.model_listbox.delete(0, tk.END)
        for model in ModelDB().get_all_models():
            self.model_listbox.insert(0, model)

    def show_model_by_id(self):
        model_id = self.model_id_entry.get()
        if model_id:
            model = ModelDB().get_model_by_id(model_id)
            self.model_entry.delete(0, tk.END)
            self.model_entry.insert(0, model.model_name)
            self.car_id_entry.delete(0, tk.END)
            self.car_id_entry.insert(0, model.car_id)
            self.model_id_entry.delete(0, tk.END)
            self.model_id_entry.insert(0, model.model_name)
        else:
            messagebox.showerror("Error", "Field car_id is empty.")

    def add_model(self):
        model_name = self.model_entry.get()
        car_id = self.car_id_entry.get()
        model = Model(model_name, car_id or None)
        if model_name and car_id:
            ModelDB().add_model(model)
            self.clear_form()
            self.info_label["text"] = "Model successfully added to database"
            self.info_label["bg"] = "Green"
        elif model_name:
            ModelDB().add_model(model)
            self.clear_form()
            self.info_label["text"] = "Warning, added model without foreign key, please update it later or delete"
            self.info_label["bg"] = "Yellow"
        else:
            messagebox.showerror("Error", "At least field model is required.")
        self.fill_model_listbox()

    def update_model(self):
        model_id = self.model_id_entry.get()
        if model_id:
            model_name = self.model_entry.get()
            car_id = self.car_id_entry.get() or None
            if model_name:
                model = Model(model_name, car_id)
                model.model_id = model_id
                index = self.model_listbox.get(0, tk.END).index(str(ModelDB().get_model_by_id(model_id)))
                self.model_listbox.delete(index)
                ModelDB().update_model(model, model_id)
                self.model_listbox.insert(0, model)
                self.clear_form()
                self.info_label["text"] = "Model successfully updated"
                self.info_label["bg"] = "Green"
            else:
                messagebox.showerror("Error", "At least model field is required.")
        else:
            messagebox.showerror("Error", "Field model_id is required.")

    def delete_model(self):
        model_id = self.model_id_entry.get()
        if model_id:
            index = self.model_listbox.get(0, tk.END).index(str(ModelDB().get_model_by_id(model_id)))
            self.model_listbox.delete(index)
            ModelDB().delete_model(model_id)
            self.clear_form()
            self.info_label["text"] = "Model successfully deleted from database"
            self.info_label["bg"] = "Green"
        else:
            messagebox.showerror("Error", "Please select a car to delete.")

    def clear_form(self):
        self.model_entry.delete(0, tk.END)
        self.car_id_entry.delete(0, tk.END)
        self.model_id_entry.delete(0, tk.END)

    def on_select_model(self, event):
        index = self.model_listbox.curselection()
        if index:
            model = self.model_listbox.get(index)
            model_id, model_name, car_id = self.parse_model(model)
            self.model_entry.delete(0, tk.END)
            self.model_entry.insert(0, model_name)
            self.car_id_entry.delete(0, tk.END)
            self.car_id_entry.insert(0, car_id)
            self.model_id_entry.delete(0, tk.END)
            self.model_id_entry.insert(0, model_id)

    def parse_model(self, trademark):
        model_id, model_name, car_id = trademark.split(" ")
        return model_id, model_name, car_id


