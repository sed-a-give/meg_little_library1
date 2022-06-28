import mysql.connector
from tabulate import tabulate
from databaseconfig import read_db_config





def retrieve_genres():
    try:
        db_config = read_db_config()
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT genre FROM meg_little_library")
            all_genres = cursor.fetchall()   

    except mysql.connector.Error as e:
        print("Error while connecting to the database", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            return all_genres
            



def books_in_genre(genre):
    records = ""
    try:
        db_config = read_db_config()
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT book_id, title, author FROM meg_little_library WHERE genre = %s"
            genreList = [genre]
            cursor.execute(query, genreList)
            records = cursor.fetchall()

    except mysql.connector.Error as e:
        print("Error while connecting to the database", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            return records

def print_books_in_genre(records):
    headers = "book_id", "title", "author"
    print(tabulate(records, headers))
    

            

def book_details(book_id):
    result = ""
    try:
        db_config = read_db_config()
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT * FROM meg_little_library WHERE book_id = %s"
            book_info = [book_id]
            cursor.execute(query, book_info)
            records = cursor.fetchall()
            headers = "book_id", "title", "author", "page_number", "genre", "goodreads_rating"
            result = tabulate(records, headers)

    except mysql.connector.Error as e:
        print("Error while connecting to the database", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            return result

def id_is_in_list(book_id, book_list):
    for book in book_list:
        if book[0] == book_id:
            return True
    return False


try_again_genre = "Y"


print("Welcome to Meg's Little Library! What kind of books are you interested in?")
print("We have the following genres: ")
print(tabulate(retrieve_genres()))
while try_again_genre.lower() != "n":
    genre = input("Please enter a genre to continue: ")
    book_list = books_in_genre(genre)
    if book_list: 
       print_books_in_genre(book_list)
       try_again_book_id = "Y"
       while try_again_book_id.lower() == "y":
           book_id = input("Please type a book id to get more details: ")
           if id_is_in_list(book_id, book_list):
               id_list = book_details(book_id)
               print(id_list)
               try_again_book_id = input("Would you like to look at another book? (Y/N) or type 'genre' to search another genre: ")
               try_again_genre = try_again_book_id
           else:
               try_again_book_id = input("Sorry, that's not a valid id. Try again? (Y/N) ")
    else:    
        try_again_genre = input("Sorry, there are no genres matching that in the library. Try again? (Y/N) ")




