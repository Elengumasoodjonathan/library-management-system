import json

    # Book's class
class Book:
    def __init__(self, title, author, book_id, category, available=True):
        self.title = title
        self.author = author
        self.book_id = book_id
        self.category = category
        self.available = available
# Member's class
class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    # Library's class
class Library:
    def __init__(self):
        self.books = []
        self.members = []

        # Method to save the books
    def save_books(self):
        book_data = []

        for book in self.books:
            book_info = {
                'title': book.title,
                'Author': book.author,
                'ID': book.book_id,
                'Category': book.category,
                'Available': book.available
            }
            book_data.append(book_info)

        with open('books.json', 'w') as file:
                json.dump(book_data, file)
        # Method to save members
    def save_member(self):
        member_data = []

        for member in self.members:
            borrowed_book_ids = []

            for book in member.borrowed_books:
                borrowed_book_ids.append(book.book_id)

            member_info = {
                'name': member.name,
                'member_id': member.member_id,
                'borrowed_books': borrowed_book_ids
            }
            member_data.append(member_info)

        with open('member.json', 'w') as file:
            json.dump(member_data, file)



        # Method to add a book
    def add_book(self, book):
        self.books.append(book)

        # Method to add a member
    def add_member(self, member):
        self.members.append(member)

        # Method to find a book 
    def find_book(self, book_id):
        for book in self.books:
            if book_id == book.book_id:
                return book
        return None
        # Method to find a member
    def find_member(self, member_id):
        for member in self.members:
            if member_id == member.member_id:
                return member
        return None
        # Method to borrow a book 
    def borrow_book(self, member_id, book_id):
            # Find a member if he is missing
        find_the_member = self.find_member(member_id)

        if find_the_member is None:
            print('Member not found')
            return
            # Finf a book if it is missing
        find_the_book = self.find_book(book_id)

        if find_the_book is None:
            print('Book not found')
            return 
            # Check wether the book is lready borrowed. if so we stop
        if find_the_book.available is False:
            print(f'Sorry, this book is already borrowed by {find_the_member.name}')
            return
            # changing the availability to false
        find_the_book.available = False
            # Add the book object to the member's borrowed-book list
        find_the_member.borrowed_books.append(find_the_book)
        print(f'The book {find_the_book.title} was borrowed by {find_the_member.name}')

    def return_book(self, member_id, book_id):

            # Find the member 
        find_the_member = self.find_member(member_id)

        if find_the_member is None:
            print('Member not found')
            return

            # Finf the book
        find_the_book = self.find_book(book_id)

        if find_the_book is None:
            print('Book not found')
            return

        if find_the_book not in find_the_member.borrowed_books:
            print('This member has not borrowed this book')
            return

        find_the_member.borrowed_books.remove(find_the_book)
        find_the_book.available = True

        print(f'The book {find_the_book.title} has been returned by {find_the_member.name}')


    def display_books(self):

        if not self.books:
            print('No books in the library')
            return
        for book in self.books:
            print(f'TITLE: {book.title}')
            print(f'AUTHOR: {book.author}')
            print(f'BOOK ID: {book.book_id}')
            print(f'category: {book.category}')
            print(f'AVAILABILITY: {book.available}')
            print('-----------------------')

    def display_members(self):

        if not self.members:
            print('No members in the library')
            return
        for member in self.members:
            print(f'NAME: {member.name}')
            print(f'ID: {member.member_id}')
            print(f'BORROWED BOOKS: {len(member.borrowed_books)}')    
            print('-----------------------')

    def load_books(self):

        try:
            with open('books.json', 'r') as file:
                book_data = json.load(file)

                for dictionary in book_data:

                    new_book_object = Book(
                        dictionary['title'],
                        dictionary['Author'],
                        dictionary['ID'],
                        dictionary['Category'],
                        dictionary['Available']
                    )
                    self.books.append(new_book_object)
        except FileNotFoundError:
            print('No saved books found yet.')

    def load_members(self):
        try:
            with open('member.json', 'r') as file:
                member_data = json.load(file)

                for dictionary in member_data:

                    new_member_object = Member(
                        dictionary['name'],
                        dictionary['member_id']
                    )
                    for book_id in dictionary['borrowed_books']:
                        new_member_object.borrowed_books.append(self.find_book(book_id))
                    self.members.append(new_member_object)
        except FileNotFoundError:
            print("No saved members found yet.")
            


def menu():

    my_library = Library()
    my_library.load_books()
    my_library.load_members()
    while True:
            print('===========================')
            print('        LIBRARY            ')
            print('===========================')
            print('')
            print('1. ADD BOOK')
            print('2. ADD MEMBER')
            print('3. BORROW BOOK')
            print('4. RETURN BOOK')
            print('5. DISPLAY BOOKS')
            print('6. DISPLAY MEMBERS')
            print('7. EXIT')


            user = int(input('Enter one of the choices to acccess the library: '))

            if user == 1:
                title = input('Book name: ')
                author = input('Book author: ')
                book_id = int(input('Book ID: '))
                category = input('Book category: ')
                new_book = Book(title, author, book_id, category)
                my_library.add_book(new_book)
                my_library.save_books()
            elif user == 2:
                name = input('Member name: ')
                member_id = int(input('Member ID: '))
                new_member = Member(name, member_id)
                my_library.add_member(new_member)
                my_library.save_member()
            elif user == 3:
                member_id = int(input('Provide the member ID: '))
                book_id = int(input('Provide the book ID: '))
                my_library.borrow_book(member_id, book_id)
                my_library.save_member()
                my_library.save_books()
            elif user == 4:
                member_id = int(input('Provide the member ID: '))
                book_id = int(input('Provide the book ID: '))
                my_library.return_book(member_id, book_id)
                my_library.save_member()
                my_library.save_books()
            elif user == 5:
                my_library.display_books()
            elif user == 6:
                my_library.display_members()
            elif user == 7:
                print('SHUTTIN DWON...')
                break
            else:
                print('Invalid choice, please chose from 1 to 7')

menu()

