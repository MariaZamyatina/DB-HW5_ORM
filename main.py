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
