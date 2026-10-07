from src.api.sync_client import SyncClient
from src.processing.cleaner import DataCleaner
while True:
    try:
        print("[1] Ingest Works by Subject")
        print("[2] Search Books by Author/Title/ISBN")
        print("[3] Process $ Deduplicate Local Catalog File")
        print("[4] Generate Analytical Report")
        print("[5] System Health, Cache Maintenance & Database Administration")
        print("[6] Run Quality Checks & Test Suite Dianostics")
        print("[0] Exit")
        option = input("Enter the option:") 
        if option == "1":
           client = SyncClient()
           subject=input("Enter the subject to ingest works: ")
           pages=input("Enter the number of pages to ingest: ")
           
           response = client.get_works_by_subject(subject, pages)

           print(f"\nTotal Works Found: {response['work_count']}\n")
           print("Titles of Works:")
           for work in response["works"]:
               print(work["title"])
        if option == "2":
            author_title_isbn = input("Enter the author, title, or ISBN to search for books: [")
            cleaned_query = author_title_isbn.strip()
            cleaner=DataCleaner()

            if cleaner.is_valid_isbn(cleaned_query) == "Valid ISBN-10" or cleaner.is_valid_isbn(cleaned_query) == "Valid ISBN-13":
                client = SyncClient()
                response = client.search_books_by_author_title_isbn(cleaned_query)
                print(f"\nTotal Books Found: {response['numFound']}\n")
                print("Titles of Books:")
                for book in response["docs"]:
                    print(book.get("title", "No title available"))

            if cleaner.is_valid_isbn(cleaned_query) == "Valid text input":
                client = SyncClient()
                response = client.search_books_by_author(cleaned_query)
                print(f"\nTotal Books Found: {response['numFound']}\n")
                id=response["docs"][0]["author_key"][0]
                #id=response['docs'][0].get('author_key', 'No author ID available')
                response = client.search_books_by_author_id(id)

                print(f"ID of the first book found: {id}\n")
                print("Titles of Books:")
                for book in response["docs"]:
                    print(book.get("title", "No title available"))
            
            input("Press Enter to continue...")
        if option == "3":
           print("Process $ Deduplicate Local Catalog File")
        if option == "4":
           print("Generate Analytical Report")
        if option == "5":
           print("System Health, Cache Maintenance & Database Administration")
        if option == "6":
           print("Run Quality Checks & Test Suite Diagnostics")
        if option == "0":
           print("Exiting the program.")
           break
    except KeyboardInterrupt:
        print("\nExiting the program.")
        break