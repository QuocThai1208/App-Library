import math
from flask import render_template, session
from unicodedata import category

from app import app
import utils


@app.route("/")
def index():
    cates = utils.load_categories()
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    page = request.args.get('page', 1)
    books = utils.load_books(cate_id=cate_id, kw=kw, page=int(page))

    page_size = app.config['PAGE_SIZE']
    total = utils.count_books()
    return render_template('index.html', books = books, pages=math.ceil(total/page_size), categories=cates)

if __name__ == "__main__":
    from app.admin import *
    app.run(debug=True)