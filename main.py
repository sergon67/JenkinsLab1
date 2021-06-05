from peewee import *
from data import names, cities, addresses
import random
import datetime
from sys import argv

db = SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = db

class Clients(BaseModel):
    name = CharField()
    city = CharField()
    address = CharField()

class Orders(BaseModel):
    clients = ForeignKeyField(Clients)
    date = DateField()
    amount = IntegerField()
    description = TextField()

def init():
    if not (Clients.table_exists() and Orders.table_exists()):
        db.create_tables([Clients, Orders])
    else:
        db.drop_tables([Clients, Orders])
        db.create_tables([Clients, Orders])
    db.close()

def fill():
    for i in range(10):
        client = Clients.create(
            name = random.choice(names),
            city = random.choice(cities),
            address = random.choice(addresses)
        )
    for i in range(10):
        order = Orders.create(
            clients = Clients.get_by_id(random.randint(1,10)),
            date = datetime.datetime.now(),
            amount = random.randint(1,10),
            description = "Hello"
        )

def show(Model):
    data = Model.select()
    for inf in data:
        if (Model is Clients):
            print(*("{:<30}".format(str(i)) for i in [inf.id, inf.name, inf.city, inf.address]))
        else:
            print(*("{:<30}".format(str(i)) for i in [inf.clients, inf.date, inf.amount, inf.description]))

def help():
    print("""
    Запуск программы командой -> python main.py [параметр]
    Параметры:
        1) init - создает базу данных
        2) fill - заполняет базу случайными данными
        3) show [название таблицы(Clients или Orders)] - показывает содержащиеся в данной таблице данные
    """)

if __name__ == "__main__":

    try:
        arg = argv[1]
        if arg == "init":
            init()
        elif arg == "fill":
            fill()
        elif arg == "show":
            try:
                if argv[2] == "Clients":
                    show(Clients)
                elif argv[2] == "Orders":
                    show(Orders)
                else:
                    print("Некотректное название таблицы")
            except:
                print("Введите название таблицы")
    except IndexError:
        help()

db.close()
