import json

from models import Publisher, Shop, Book, Stock, Sale


def insert_data(session, file):
    """Метод заполняет таблицы данными из файла json"""
    with open(file, 'r') as fd:
        data = json.load(fd)

        for record in data:
            model = {
                'publisher': Publisher,
                'shop': Shop,
                'book': Book,
                'stock': Stock,
                'sale': Sale,
                }[record.get('model')]
            session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()
