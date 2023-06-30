import random

from django.core.management.base import BaseCommand
import requests
import random
from books.models import Book, Publisher
import django


class Command(BaseCommand):
    help = 'Загрузка книг из другого источника'

    def handle(self, *args, **options):
        print('команда запустилась')
        url = 'http://libgen.rs/json.php?fields=Title,Author,Year,publisher&ids=1,2,3,4,5,6,7'
        response = requests.get(url)

        languages = ['ru', 'en', 'fr']
        for book in response.json():
            # print(book['title'])
            # print(book['author'])
            # print(book['year'])
            # print(book['publisher'])
            # print(book['publisher'])
            language = random.choices(languages)
            if not Publisher.objects.filter(title=book['publisher']).last():
                publisher = Publisher.objects.create(title=book['publisher'],
                                                     language=language)
            else:
                publisher = Publisher.objects.filter(title=book['publisher']).last()
                random1 = random.randint(5,10)
            try:
                if not Book.objects.filter(title=book['title']).last():
                    Book.objects.create(title=book['title'],
                                        autor=book['author'],
                                        year=book['year'],
                                        publisher=publisher,
                                        raiting=random1)
            except django.db.utils.IntegrityError:
                Book.objects.create(title=book['title'],
                                    autor=book['author'],
                                    year=book['year'],
                                    raiting=random1
                                    )
