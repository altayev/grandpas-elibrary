from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import math
import os
from dotenv import load_dotenv



def get_books_catalogue():
    catalogue_file = os.getenv('CATALOGUE_FILE')
    with open(catalogue_file, "r") as my_file:
      books_json = my_file.read()
    books_catalogue = json.loads(books_json)
    return books_catalogue


def get_template():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    return template


def render_pages():
    template = get_template()
    books_catalogue = get_books_catalogue()  
    books_amount = len(books_catalogue)
    books_amount_on_page = 20
    pages_amount = math.ceil(books_amount/books_amount_on_page)
    folder = os.getenv('PAGES_FOLDER')
    os.makedirs(folder, exist_ok=True)

    for num in range(0,books_amount,books_amount_on_page):
        current_page = num//books_amount_on_page+1
        filename='index{}.html'.format(current_page)

        rendered_page = template.render(
            books_catalogue=books_catalogue[num:books_amount_on_page+num],
            pages_amount = pages_amount,
            current_page = current_page,
        )
        with open(os.path.join(folder, filename), 'w', encoding="utf8") as file:
            file.write(rendered_page)

if __name__ == "__main__":
    load_dotenv()
    render_pages()
