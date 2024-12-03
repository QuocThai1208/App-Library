from unicodedata import category

from app import db, app
from sqlalchemy import func
from app.models import Category, Book, Author, OrderDetail, Order


# thống kê số lượng của từng loại sách
def category_stats():
    return db.session.query(Category.id, Category.name, func.count(Book.id)).join(Book, Category.id.__eq__(
        Book.category_id), isouter=True).group_by(Category.id, Category.name).all()


# Thống kê theo danh thu của sách
def book_stats(kw=None, from_date=None, to_date=None, author=None, category=None):
    b = db.session.query(Book.id, Book.name, func.sum(OrderDetail.quantity * OrderDetail.unit_price)).join(
        OrderDetail, OrderDetail.book_id.__eq__(Book.id), isouter=True).join(Order, Order.id.__eq__(
        OrderDetail.order_id), isouter=True).join(Author, Author.id.__eq__(Book.author_id)).join(Category,Category.id.__eq__(  Book.category_id)).group_by( Book.id, Book.name)

    if kw:
        b = b.filter(Book.name.contains(kw))
    if from_date:
        b = b.filter(Order.order_date.__ge__(from_date))  # so sánh lớn hơn
    if to_date:
        b = b.filter(Order.order_date.__le__(to_date))  # so sánh nhỏ hơn
    if author:
        b = b.filter(Author.name.contains(author))
    if category:
        b = b.filter(Category.name.contains(category))
    return b.all()

#Thống kê số lượng tồn kho
def inventory_stats(name=None):
        b = db.session.query(Book.id, Book.name, Book.units_in_stock)
        if name:
            b = b.filter(Book.name.contains(name))
        return b.all()



def load_categories():
    return Category.query.all()


def load_books(cate_id=None, kw=None, page=1):
    query = Book.query

    if kw:
        query = query.filter(Book.name.contains(kw))

    if cate_id:
        query = query.filter(Book.category_id == cate_id)

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    query = query.slice(start, start + page_size)

    return query.all()


def count_books():
    return Book.query.count()
