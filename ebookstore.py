import sqlite3


def create_book_table():
    """
    Creates a table called "book" in the database "books.db" if it doesn't exist.
    Inserts some initial book data into the table if it's empty.
    """
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY,
        Title TEXT NOT NULL,
        Author TEXT NOT NULL,
        qty INTEGER
    )''')
    try:
        # Insert initial book data
        cursor.executemany('''INSERT INTO book (id, Title, Author, qty) 
            VALUES(?,?,?,?)''',
            [(3001, "A Tale of Two Cities", "Charles Dickens", 30),
            (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
            (3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
            (3004, "The Lord of the Rings", "J.R.R. Tolkien", 37),
            (3005, "Alice in Wonderland", "Lewis Caroll", 12)]) 
        conn.commit()
    
    except sqlite3.IntegrityError:
        print("Error: Duplicate data found. Skipping insertion.")
    # Print the existing books in the table
    cursor.execute("SELECT * FROM book")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()


def add_book():
    """
    Adds a new book to the "book" table in the "books.db" database.
    Prompts the user for book details (ID, title, author, quantity) and inserts them into the table.
    Handles potential errors like invalid input and duplicate data.
    """
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    try:  
      id = int(input("Enter book ID: "))
    except ValueError:
      print("Invalid quantity. Please enter a number.")
      return
  
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    try:
        qty = int(input("Enter the quantity of the book: "))
    except ValueError:
        print("Invalid quantity. Please enter a number.")
        return
    
    try:
        cursor.execute('''INSERT INTO book (id, Title, Author, qty) VALUES (?, ?, ?, ?)''', 
              (id, title, author, qty))
        conn.commit()
        print("Book added successfully!")
    except sqlite3.IntegrityError:
        print("Error: Duplicate data found. Skipping insertion.")
    finally:
        conn.close()


def update_book():
    """
    Updates an existing book in the "book" table in the "books.db" database.
    Prompts the user for the book ID and new details (title, author, quantity).
    Allows partial updates (updating only some fields).
    Handles potential errors like invalid input and database operation errors.
    """
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    
    try:
        id = int(input("Enter the ID of the book to update: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return
    
    title = input("Enter the new title of the book (leave blank if unchanged): ")
    author = input("Enter the new author of the book (leave blank if unchanged): ")
    try:
        qty = int(input("Enter the new quantity of the book (leave blank if unchanged): "))
    except ValueError:
        print("Invalid quantity. Please enter a number.")
        return
    
    update_query = "UPDATE book SET "
    update_params = []
    if title:
        update_query += "Title = ?, "
        update_params.append(title)
    if author:
        update_query += "Author = ?, "
        update_params.append(author)
    if qty is not None:
        update_query += "qty = ?, "
        update_params.append(qty)
    
    # Remove trailing comma and space
    update_query = update_query[:-2]
    update_query += " WHERE id = ?"
    update_params.append(id)
    
    try:
        cursor.execute(update_query, update_params)
        conn.commit()
        print("Book updated successfully!")
    except sqlite3.OperationalError as e:
        print("Error updating book:", e)
    finally:
        conn.close()


def delete_book():
    """
    Deletes a book from the "book" table in the "books.db" database.
    Prompts the user for the book ID to delete.
    Handles potential errors like invalid input and database operation errors.
    """
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    
    try:
        id = int(input("Enter the ID of the book to delete: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return
    
    try:
        cursor.execute("DELETE FROM book WHERE id = ?", (id,))
        conn.commit()
        print("Book deleted successfully!")
    except sqlite3.OperationalError as e:
        print("Error deleting book:", e)
    finally:
        conn.close()


def search_book():
    """
    Searches for a book in the "book" table in the "books.db" database based on its ID.
    Prompts the user for the book ID to search.
    Prints the book details if found, otherwise indicates that the book is not found.
    Handles potential errors like invalid input and database operation errors.
    """
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    try:
        id = int(input("Enter the ID of the book to search for: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    try:
        cursor.execute("SELECT * FROM book WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            print("Book found:")
            print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Quantity: {row[3]}")
        else:
            print("Book not found.")
    except sqlite3.OperationalError as e:
        print("Error searching for book:", e)
    finally:
        conn.close()

# Database management menu
create_book_table()
while True:
    menu = input('''
1. Enter book
2. Update book
3. Delete book
4. Search book
0. Exit
: ''')

    if menu == '1':
        add_book()
    elif menu == '2':
        update_book()
    elif menu == '3':
        delete_book()
    elif menu == '4':
        search_book()
    elif menu == '0':
        print("Goodbye!!")
        break
    else:
        print("Invalid input. Please try again")                