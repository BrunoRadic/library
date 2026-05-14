from django.core.management.base import BaseCommand

from books.models import Author, Book, Genre


GENRES = [
    'Fiction', 'Non-Fiction', 'Science', 'History', 'Mystery',
    'Romance', 'Fantasy', 'Biography', 'Thriller', 'Science Fiction',
]

AUTHORS = [
    ('George', 'Orwell'),
    ('J.R.R.', 'Tolkien'),
    ('Agatha', 'Christie'),
    ('Stephen', 'King'),
    ('J.K.', 'Rowling'),
    ('Ernest', 'Hemingway'),
    ('Toni', 'Morrison'),
    ('Gabriel', 'García Márquez'),
    ('Leo', 'Tolstoy'),
    ('Franz', 'Kafka'),
    ('Ursula', 'Le Guin'),
    ('Philip', 'Dick'),
    ('Cormac', 'McCarthy'),
    ('Donna', 'Tartt'),
    ('Haruki', 'Murakami'),
]

# (title, first_name, last_name, genre_names, year, copies)
BOOKS = [
    ('Nineteen Eighty-Four', 'George', 'Orwell', ['Fiction', 'Science Fiction'], 1949, 7),
    ('Animal Farm', 'George', 'Orwell', ['Fiction'], 1945, 5),
    ('The Fellowship of the Ring', 'J.R.R.', 'Tolkien', ['Fantasy', 'Fiction'], 1954, 6),
    ('The Two Towers', 'J.R.R.', 'Tolkien', ['Fantasy', 'Fiction'], 1954, 5),
    ('The Return of the King', 'J.R.R.', 'Tolkien', ['Fantasy', 'Fiction'], 1955, 5),
    ('The Hobbit', 'J.R.R.', 'Tolkien', ['Fantasy', 'Fiction'], 1937, 8),
    ('Murder on the Orient Express', 'Agatha', 'Christie', ['Mystery', 'Thriller'], 1934, 6),
    ('And Then There Were None', 'Agatha', 'Christie', ['Mystery', 'Thriller'], 1939, 5),
    ('Death on the Nile', 'Agatha', 'Christie', ['Mystery'], 1937, 4),
    ('The ABC Murders', 'Agatha', 'Christie', ['Mystery'], 1936, 3),
    ('The Shining', 'Stephen', 'King', ['Thriller', 'Fiction'], 1977, 7),
    ('It', 'Stephen', 'King', ['Thriller', 'Fiction'], 1986, 6),
    ('Misery', 'Stephen', 'King', ['Thriller'], 1987, 5),
    ('Pet Sematary', 'Stephen', 'King', ['Thriller', 'Fiction'], 1983, 4),
    ('The Stand', 'Stephen', 'King', ['Fiction', 'Science Fiction'], 1978, 3),
    ("Harry Potter and the Philosopher's Stone", 'J.K.', 'Rowling', ['Fantasy', 'Fiction'], 1997, 10),
    ('Harry Potter and the Chamber of Secrets', 'J.K.', 'Rowling', ['Fantasy', 'Fiction'], 1998, 9),
    ('Harry Potter and the Prisoner of Azkaban', 'J.K.', 'Rowling', ['Fantasy', 'Fiction'], 1999, 9),
    ('Harry Potter and the Goblet of Fire', 'J.K.', 'Rowling', ['Fantasy', 'Fiction'], 2000, 8),
    ('Harry Potter and the Order of the Phoenix', 'J.K.', 'Rowling', ['Fantasy', 'Fiction'], 2003, 7),
    ('The Old Man and the Sea', 'Ernest', 'Hemingway', ['Fiction'], 1952, 5),
    ('A Farewell to Arms', 'Ernest', 'Hemingway', ['Fiction', 'History'], 1929, 4),
    ('For Whom the Bell Tolls', 'Ernest', 'Hemingway', ['Fiction', 'History'], 1940, 4),
    ('The Sun Also Rises', 'Ernest', 'Hemingway', ['Fiction'], 1926, 3),
    ('Beloved', 'Toni', 'Morrison', ['Fiction', 'History'], 1987, 6),
    ('Song of Solomon', 'Toni', 'Morrison', ['Fiction'], 1977, 5),
    ('The Bluest Eye', 'Toni', 'Morrison', ['Fiction'], 1970, 4),
    ('Sula', 'Toni', 'Morrison', ['Fiction'], 1973, 3),
    ('One Hundred Years of Solitude', 'Gabriel', 'García Márquez', ['Fiction', 'Fantasy'], 1967, 7),
    ('Love in the Time of Cholera', 'Gabriel', 'García Márquez', ['Fiction', 'Romance'], 1985, 6),
    ('Chronicle of a Death Foretold', 'Gabriel', 'García Márquez', ['Fiction', 'Mystery'], 1981, 4),
    ('War and Peace', 'Leo', 'Tolstoy', ['Fiction', 'History'], 1869, 5),
    ('Anna Karenina', 'Leo', 'Tolstoy', ['Fiction', 'Romance'], 1878, 6),
    ('The Death of Ivan Ilyich', 'Leo', 'Tolstoy', ['Fiction'], 1886, 3),
    ('The Trial', 'Franz', 'Kafka', ['Fiction'], 1925, 5),
    ('The Metamorphosis', 'Franz', 'Kafka', ['Fiction', 'Science Fiction'], 1915, 6),
    ('The Castle', 'Franz', 'Kafka', ['Fiction'], 1926, 4),
    ('The Left Hand of Darkness', 'Ursula', 'Le Guin', ['Science Fiction', 'Fantasy'], 1969, 5),
    ('The Dispossessed', 'Ursula', 'Le Guin', ['Science Fiction'], 1974, 4),
    ('A Wizard of Earthsea', 'Ursula', 'Le Guin', ['Fantasy', 'Fiction'], 1968, 6),
    ('The Tombs of Atuan', 'Ursula', 'Le Guin', ['Fantasy', 'Fiction'], 1971, 4),
    ('Do Androids Dream of Electric Sheep?', 'Philip', 'Dick', ['Science Fiction'], 1968, 7),
    ('The Man in the High Castle', 'Philip', 'Dick', ['Science Fiction', 'History'], 1962, 5),
    ('Ubik', 'Philip', 'Dick', ['Science Fiction'], 1969, 4),
    ('VALIS', 'Philip', 'Dick', ['Science Fiction', 'Fiction'], 1981, 3),
    ('The Road', 'Cormac', 'McCarthy', ['Fiction', 'Thriller'], 2006, 7),
    ('No Country for Old Men', 'Cormac', 'McCarthy', ['Fiction', 'Thriller'], 2005, 6),
    ('Blood Meridian', 'Cormac', 'McCarthy', ['Fiction', 'History'], 1985, 5),
    ('All the Pretty Horses', 'Cormac', 'McCarthy', ['Fiction'], 1992, 5),
    ('The Secret History', 'Donna', 'Tartt', ['Fiction', 'Mystery'], 1992, 7),
    ('The Goldfinch', 'Donna', 'Tartt', ['Fiction'], 2013, 6),
    ('The Little Friend', 'Donna', 'Tartt', ['Fiction', 'Mystery'], 2002, 4),
    ('Norwegian Wood', 'Haruki', 'Murakami', ['Fiction', 'Romance'], 1987, 7),
    ('Kafka on the Shore', 'Haruki', 'Murakami', ['Fiction', 'Fantasy'], 2002, 6),
    ('The Wind-Up Bird Chronicle', 'Haruki', 'Murakami', ['Fiction', 'Mystery'], 1994, 5),
    ('1Q84', 'Haruki', 'Murakami', ['Fiction', 'Science Fiction'], 2009, 5),
]


class Command(BaseCommand):
    help = 'Seed the database with genres, authors and books'

    def handle(self, *args, **options):
        genres = {}
        for name in GENRES:
            obj, created = Genre.objects.get_or_create(name=name)
            genres[name] = obj
            if created:
                self.stdout.write(f'  Genre: {name}')

        authors = {}
        for first, last in AUTHORS:
            obj, created = Author.objects.get_or_create(first_name=first, last_name=last)
            authors[(first, last)] = obj
            if created:
                self.stdout.write(f'  Author: {first} {last}')

        books_created = 0
        for title, first, last, genre_names, year, copies in BOOKS:
            author = authors[(first, last)]
            book, created = Book.objects.get_or_create(
                title=title,
                author=author,
                defaults={
                    'year': year,
                    'copies_available': copies,
                },
            )
            if created:
                book.genres.set([genres[g] for g in genre_names])
                books_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. {len(GENRES)} genres, {len(AUTHORS)} authors, {books_created} books created.'
        ))
