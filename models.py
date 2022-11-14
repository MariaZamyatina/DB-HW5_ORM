import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False, unique=True)

    books = relationship("Book", back_populates="publisher")

    def __str__(self):
        return f'{self.name}'


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship("Publisher", back_populates="books")
    stock = relationship("Stock", back_populates="books")

    def __str__(self):
        return f'{self.title}, {self.publisher}, {self.stock}'


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False)

    def __str__(self):
        return f'{self.name}, {self.stock}'

    stock = relationship("Stock", back_populates="shops")


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer, nullable=False)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)

    shops = relationship("Shop", back_populates="stock")
    books = relationship("Book", back_populates="stock")
    sale = relationship("Sale", back_populates="stocks")

    def __str__(self):
        return f'{self.books} | {self.shops} {self.sale}'


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float(2), nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)

    stocks = relationship("Stock", back_populates="sale")
    #stock = relationship(Stock, backref="sales")

    def __str__(self):
        return f'{self.stocks} | {self.price} | {self.date_sale} '

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)