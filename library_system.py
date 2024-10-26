class Node:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_available = True
        self.left = None
        self.right = None

class BSTBooks:
    def __init__(self):
        self.root = None
    
    def insert(self, book_id, title, author):
        if not self.root:
            self.root = Node(book_id, title, author)
        else:
            self._insert_recursive(self.root, book_id, title, author)
    
    def _insert_recursive(self, node, book_id, title, author):
        if book_id < node.book_id:
            if node.left is None:
                node.left = Node(book_id, title, author)
            else:
                self._insert_recursive(node.left, book_id, title, author)
        else:
            if node.right is None:
                node.right = Node(book_id, title, author)
            else:
                self._insert_recursive(node.right, book_id, title, author)
    
    def search(self, book_id):
        return self._search_recursive(self.root, book_id)
    
    def _search_recursive(self, node, book_id):
        if node is None or node.book_id == book_id:
            return node
        if book_id < node.book_id:
            return self._search_recursive(node.left, book_id)
        return self._search_recursive(node.right, book_id)
    
    def get_all_books(self):
        books = []
        self._inorder_traversal(self.root, books)
        return books
    
    def _inorder_traversal(self, node, books):
        if node:
            self._inorder_traversal(node.left, books)
            books.append({
                'id': node.book_id,
                'title': node.title,
                'author': node.author,
                'available': node.is_available
            })
            self._inorder_traversal(node.right, books)

class BorrowingRecord:
    def __init__(self, user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id
        self.next = None

class BorrowingList:
    def __init__(self):
        self.head = None
    
    def add_borrowing(self, user_id, book_id):
        new_record = BorrowingRecord(user_id, book_id)
        if not self.head:
            self.head = new_record
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_record
    
    def remove_borrowing(self, user_id, book_id):
        if not self.head:
            return
        
        if self.head.user_id == user_id and self.head.book_id == book_id:
            self.head = self.head.next
            return
        
        current = self.head
        while current.next:
            if current.next.user_id == user_id and current.next.book_id == book_id:
                current.next = current.next.next
                return
            current = current.next
    
    def get_all_borrowings(self):
        borrowings = []
        current = self.head
        while current:
            borrowings.append({
                'user_id': current.user_id,
                'book_id': current.book_id
            })
            current = current.next
        return borrowings

class WaitingQueue:
    def __init__(self):
        self.queue = []
    
    def add_to_waitlist(self, user_id, book_id):
        self.queue.append((user_id, book_id))
    
    def remove_from_waitlist(self):
        if self.queue:
            return self.queue.pop(0)
        return None
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def get_waitlist(self):
        return self.queue.copy()

class LibrarySystem:
    def __init__(self):
        self.books = BSTBooks()
        self.borrowings = BorrowingList()
        self.waiting_list = WaitingQueue()
    
    def add_book(self, book_id, title, author):
        """Add a new book to the library"""
        self.books.insert(book_id, title, author)
        return f"Added book: {title} by {author} (ID: {book_id})"
    
    def borrow_book(self, user_id, book_id):
        """Process a book borrowing request"""
        book = self.books.search(book_id)
        if book and book.is_available:
            book.is_available = False
            self.borrowings.add_borrowing(user_id, book_id)
            return f"User {user_id} has borrowed book {book.title}"
        else:
            self.waiting_list.add_to_waitlist(user_id, book_id)
            return f"Book not available. User {user_id} added to waiting list"
    
    def return_book(self, user_id, book_id):
        """Process a book return"""
        book = self.books.search(book_id)
        if book:
            book.is_available = True
            self.borrowings.remove_borrowing(user_id, book_id)
            message = f"User {user_id} has returned book {book.title}"
            
            # Check waiting list
            if not self.waiting_list.is_empty():
                next_user, next_book = self.waiting_list.remove_from_waitlist()
                if next_book == book_id:
                    self.borrow_book(next_user, next_book)
                    message += f"\nBook automatically borrowed by next user in waiting list: {next_user}"
            return message
        return "Book not found"
    
    def get_all_books(self):
        """Get list of all books"""
        return self.books.get_all_books()
    
    def get_all_borrowings(self):
        """Get list of all current borrowings"""
        return self.borrowings.get_all_borrowings()
    
    def get_waitlist(self):
        """Get current waiting list"""
        return self.waiting_list.get_waitlist()