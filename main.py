import sqlalchemy as sq
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import psycopg2
import models as m
import insert

load_dotenv()
login = os.getenv('login')
password = os.getenv('password')
database = os.getenv('database')
DSN = f'postgresql://{login}:{password}@localhost:5432/{database}'
engine = sq.create_engine(DSN)

# создание таблиц
m.create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()

# создание объектов
# shop1 = m.Shop(name='Лабиринт')
# shop2 = m.Shop(name='Буквоед')
# shop3 = m.Shop(name='Книжный дом')
#
# pub1 = m.Publisher(name='Пушкин')
# pub2 = m.Publisher(name='Достоевский')
# pub3 = m.Publisher(name='Джойс')
#
# book1 = m.Book(title='Капитанская дочка', publisher=pub1)
# book2 = m.Book(title='Руслан и Людмила', publisher=pub1)
# book3 = m.Book(title='Евгений Онегин', publisher=pub1)
# book4 = m.Book(title='Бесы', publisher=pub2)
# book5 = m.Book(title='Преступление и наказание', publisher=pub2)
# book6 = m.Book(title='Идиот', publisher=pub2)
# book7 = m.Book(title='Улисс', publisher=pub3)
# book8 = m.Book(title='Поминки по Финнегану', publisher=pub3)
# book9 = m.Book(title='Дублинцы', publisher=pub3)
#
# stock1 = m.Stock(count=100, shops=shop1, books=book1)
# stock2 = m.Stock(count=80, shops=shop1, books=book2)
# stock3 = m.Stock(count=100, shops=shop2, books=book2)
# stock4 = m.Stock(count=100, shops=shop3, books=book1)
# stock5 = m.Stock(count=100, shops=shop3, books=book3)
# stock6 = m.Stock(count=100, shops=shop1, books=book3)
# stock7 = m.Stock(count=100, shops=shop2, books=book3)
# stock8 = m.Stock(count=100, shops=shop3, books=book6)
# stock9 = m.Stock(count=100, shops=shop1, books=book9)
# stock10 = m.Stock(count=100, shops=shop2, books=book6)
# stock11 = m.Stock(count=100, shops=shop1, books=book4)
# stock12 = m.Stock(count=100, shops=shop2, books=book4)
# stock13 = m.Stock(count=100, shops=shop1, books=book5)
# stock14 = m.Stock(count=100, shops=shop3, books=book5)
#
# sale1 = m.Sale(price=500, date_sale="2022-11-11", count=10, stocks=stock1)
# sale2 = m.Sale(price=660, date_sale="2022-11-12", count=5, stocks=stock2)
# sale3 = m.Sale(price=520, date_sale="2022-10-30", count=10, stocks=stock3)
# sale4 = m.Sale(price=470, date_sale="2022-11-04", count=10, stocks=stock4)
# sale5 = m.Sale(price=460, date_sale="2022-11-06", count=15, stocks=stock5)
# sale6 = m.Sale(price=820, date_sale="2022-11-01", count=10, stocks=stock6)
# sale7 = m.Sale(price=510, date_sale="2022-10-29", count=15, stocks=stock7)
# sale8 = m.Sale(price=630, date_sale="2022-11-02", count=10, stocks=stock8)
# sale9 = m.Sale(price=500, date_sale="2022-11-10", count=10, stocks=stock9)
# sale10 = m.Sale(price=610, date_sale="2022-11-13", count=10, stocks=stock10)
# sale11 = m.Sale(price=510, date_sale="2022-10-29", count=15, stocks=stock11)
# sale12 = m.Sale(price=630, date_sale="2022-11-02", count=10, stocks=stock12)
# sale13 = m.Sale(price=500, date_sale="2022-11-10", count=10, stocks=stock13)
# sale14 = m.Sale(price=610, date_sale="2022-11-13", count=10, stocks=stock14)

# session.add_all([shop1, shop2, shop3, pub1, pub2, pub3, book1, book2, book3, book4, book5, book6,
#                  book7, book8, book9])
#session.commit()  # фиксируем изменения

# заполнение таблиц
insert.insert_data(session, file='fixtures/tests_data.json')
session.commit()


author = 'O’Reilly'

# запросы
subq = session.query(m.Book).join(m.Publisher.books).filter(m.Publisher.name == author).subquery()
subq1 = session.query(m.Stock).join(subq, m.Stock.id_book == subq.c.id).subquery()
q = session.query(m.Sale).join(subq1, m.Sale.id_stock == subq1.c.id)

list = []
list1 = []
i = 0
for s in q.all():
    list = []
    list.append(str(s.stocks.books.title))
    list.append(str(s.stocks.shops.name))
    list.append(str(s.price))
    list.append(str(s.date_sale))
    list1.append(list)

def print_pretty_table(data, cell_sep=' | ', header_separator=True):
    """ Метод выводит в таблице данные запроса по продажам книг определенного автора в таблице"""
    rows = len(data)
    cols = len(data[0])
    col_width = []
    for col in range(cols):
        columns = [data[row][col] for row in range(rows)]
        col_width.append(len(max((columns), key=len)))
    separator = "--+-".join('-' * n for n in col_width)
    for i, row in enumerate(range(rows)):
        if i == 1 and header_separator:
            print("\t", separator)
        result = []
        for col in range(cols):
            item = data[row][col].rjust(col_width[col])
            result.append(item)
        print(f"\t |{cell_sep.join(result)}|")


data = [['Название книги', 'Магазин', 'Цена', 'Дата продажи'], *list1]
print_pretty_table(data)

session.close()
