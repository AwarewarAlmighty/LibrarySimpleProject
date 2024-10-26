import streamlit as st
from library_system import LibrarySystem

# Initialize the library system
if 'library' not in st.session_state:
    st.session_state.library = LibrarySystem()
    # Add some sample books
    st.session_state.library.add_book(1, "Python Programming", "John Smith")
    st.session_state.library.add_book(2, "Data Structures", "Jane Doe")
    st.session_state.library.add_book(3, "Algorithms", "Bob Wilson")

def main():
    st.title("Library Management System")
    
    # Sidebar for navigation
    menu = st.sidebar.selectbox(
        "Choose an action",
        ["View Books", "Add Book", "Borrow Book", "Return Book", "View Borrowings", "View Waitlist"]
    )
    
    if menu == "View Books":
        st.header("Available Books")
        books = st.session_state.library.get_all_books()
        for book in books:
            status = "Available" if book['available'] else "Borrowed"
            st.write(f"ID: {book['id']} - {book['title']} by {book['author']} ({status})")
    
    elif menu == "Add Book":
        st.header("Add New Book")
        book_id = st.number_input("Book ID", min_value=1, step=1)
        title = st.text_input("Title")
        author = st.text_input("Author")
        
        if st.button("Add Book"):
            if title and author:
                message = st.session_state.library.add_book(book_id, title, author)
                st.success(message)
            else:
                st.error("Please fill in all fields")
    
    elif menu == "Borrow Book":
        st.header("Borrow a Book")
        user_id = st.number_input("User ID", min_value=1, step=1)
        book_id = st.number_input("Book ID", min_value=1, step=1)
        
        if st.button("Borrow"):
            message = st.session_state.library.borrow_book(user_id, book_id)
            if "not available" in message:
                st.warning(message)
            else:
                st.success(message)
    
    elif menu == "Return Book":
        st.header("Return a Book")
        user_id = st.number_input("User ID", min_value=1, step=1)
        book_id = st.number_input("Book ID", min_value=1, step=1)
        
        if st.button("Return"):
            message = st.session_state.library.return_book(user_id, book_id)
            st.success(message)
    
    elif menu == "View Borrowings":
        st.header("Current Borrowings")
        borrowings = st.session_state.library.get_all_borrowings()
        if borrowings:
            for borrowing in borrowings:
                st.write(f"User {borrowing['user_id']} has borrowed Book {borrowing['book_id']}")
        else:
            st.info("No current borrowings")
    
    elif menu == "View Waitlist":
        st.header("Current Waitlist")
        waitlist = st.session_state.library.get_waitlist()
        if waitlist:
            for user_id, book_id in waitlist:
                st.write(f"User {user_id} is waiting for Book {book_id}")
        else:
            st.info("No users in waitlist")

if __name__ == "__main__":
    main()