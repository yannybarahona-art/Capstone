import subprocess
from pathlib import Path

from src.api.sync_client import SyncClient
from src.config import settings
from src.db.manager import DatabaseManager
from src.processing.analytics import DataProcessor
from src.processing.catalog_processor import CatalogProcessor
from src.processing.cleaner import DataCleaner
from src.reporting.generator import ReportGenerator


class CLIApp:
    def process_local_catalog(self) -> None:
        catalog_path = Path("data/sample_catalog.csv")
        database_path = Path("data/open_library.db")

        if not catalog_path.exists():
            print(f"Catalog file not found: {catalog_path}")
            return

        database = DatabaseManager(database_path)
        database.create_tables()

        unique_entries = CatalogProcessor.get_unique_entries(catalog_path)

        processed = database.upsert_many(unique_entries)

        print(f"\nSuccessfully processed records: {processed}")

    def database_administration_menu(self):
        while True:
            print("\n=== System Health & Database Administration ===")
            print("[1] Show Database Metrics")
            print("[2] Purge Expired Cache")
            print("[3] Show Runtime Configuration")
            print("[0] Back")

            option = input("Enter the option: ")

            if option == "1":
                self.clear_screen()
                self.show_database_metrics()

            elif option == "2":
                self.clear_screen()
                self.purge_expired_cache()

            elif option == "3":
                self.clear_screen()
                self.show_runtime_configuration()

            elif option == "0":
                self.clear_screen()
                break

            else:
                print("Invalid option.")

    def clear_screen(self):
        subprocess.run("cls", check=False, shell=True)

    def show_database_metrics(self) -> None:
        database = DatabaseManager(Path("data/open_library.db"))

        metrics = database.get_database_metrics()

        size_mb = metrics["database_size"] / (1024 * 1024)

        print("\n=== Database Metrics ===")
        print(f"Total Works: {metrics['works_count']}")
        print(f"Database Size: {size_mb:.2f} MB")

        input("\nPress Enter to continue...")

    def purge_expired_cache(self) -> None:
        database = DatabaseManager(Path("data/open_library.db"))

        database.create_tables()

        deleted = database.purge_expired_cache()

        print("\n=== Purge Expired Cache ===")
        print(f"Expired cache entries deleted: {deleted}")

        input("\nPress Enter to continue...")

    def show_runtime_configuration(self) -> None:
        print("\n=== Runtime Configuration ===")

        print(f"Database Path: {settings.database_path}")
        print(f"Cache TTL: {settings.cache_ttl} seconds")
        print(f"Log Level: {settings.log_level}")

        input("\nPress Enter to continue...")

    def generate_analytical_reports(self) -> None:
        database_path = Path("data/open_library.db")
        output_folder = Path("data/outputs")

        # Process data
        processor = DataProcessor(database_path)

        dataframe = processor.load_works()

        if dataframe.empty:
            print("\nNo data available to generate reports.")
            input("\nPress Enter to continue...")
            return

        dataframe = processor.clean_data(dataframe)

        # Analytics
        metrics = processor.get_key_metrics(dataframe)

        top_years = processor.get_top_publication_years(dataframe)

        top_languages = processor.get_top_languages(dataframe)

        # Generate reports
        generator = ReportGenerator(output_folder)

        excel_file = generator.generate_excel(dataframe, metrics)

        csv_file = generator.generate_csv_summary(top_years, top_languages)

        json_file = generator.generate_json(dataframe)

        print("\n=== Analytical Reports Generated ===")
        print(f"Excel: {excel_file}")
        print(f"CSV:   {csv_file}")
        print(f"JSON:  {json_file}")

        input("\nPress Enter to continue...")

    def run_diagnostic_command(self, command: list[str], title: str) -> bool:

        print(f"\n=== {title} ===")

        result = subprocess.run(command, text=True, capture_output=True, check=False)

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

        if result.returncode == 0:
            print(f"{title}: PASSED")
            return True

        print(f"{title}: FAILED")
        return False

    def run_quality_checks(self) -> None:
        print("\n=== Quality Checks & Test Suite Diagnostics ===")

        ruff_check = self.run_diagnostic_command(
            ["uv", "run", "ruff", "check", "."], "Ruff Check"
        )

        ruff_format = self.run_diagnostic_command(
            ["uv", "run", "ruff", "format", "--check", "."], "Ruff Format Check"
        )

        pytest_check = self.run_diagnostic_command(["uv", "run", "pytest"], "Pytest")

        print("\n=== Diagnostic Summary ===")
        print(f"Ruff Check:        {'PASSED' if ruff_check else 'FAILED'}")
        print(f"Ruff Format Check: {'PASSED' if ruff_format else 'FAILED'}")
        print(f"Pytest:            {'PASSED' if pytest_check else 'FAILED'}")

        input("\nPress Enter to continue...")

def run_menu():
    app = CLIApp()
    
    while True:
        try:
            app.clear_screen()
            print("[1] Ingest Works by Subject")
            print("[2] Search Books by Author/Title/ISBN")
            print("[3] Process $ Deduplicate Local Catalog File")
            print("[4] Generate Analytical Report")
            print("[5] System Health, Cache Maintenance & Database Administration")
            print("[6] Run Quality Checks & Test Suite Dianostics")
            print("[0] Exit")
            option = input("Enter the option: [")
            if option == "1":
                client = SyncClient()
                subject = input("Enter the subject to ingest works: ")
                pages = input("Enter the number of pages to ingest: ")

                response = client.get_works_by_subject(subject, pages)

                print(f"\nTotal Works Found: {response['num_found']}\n")
                print("Author and Titles of Works:")
                for work in response["docs"]:
                    print(f"{work.get('author_name', 'No author available')} - {work.get('title', 'No title available')}")
                input("Press Enter to continue...")
            if option == "2":
                author_title_isbn = input(
                    "Enter the author, title, or ISBN to search for books: ["
                )
                cleaned_query = author_title_isbn.strip()
                cleaner = DataCleaner()

                if (
                    cleaner.is_valid_isbn(cleaned_query) == "Valid ISBN-10"
                    or cleaner.is_valid_isbn(cleaned_query) == "Valid ISBN-13"
                ):
                    client = SyncClient()
                    response = client.search_books_by_isbn(cleaned_query)
                    print(f"\nTotal Books Found: {response['numFound']}\n")
                    print("Titles of Books:")
                    for book in response["docs"]:
                        print(book.get("author_name", "No author available"))
                        print(book.get("title", "No title available"))

                if cleaner.is_valid_isbn(cleaned_query) == "Valid text input":
                    client = SyncClient()
                    response = client.search_books_by_author(cleaned_query)
                    print(f"\nTotal Books Found: {response['numFound']}\n")
                    id = response["docs"][0]["author_key"][0]
                    # id=response['docs'][0].get('author_key', 'No author ID available')
                    response = client.search_books_by_author_id(id)

                    print(f"ID of the first book found: {id}\n")
                    print("Titles of Books:")
                    for book in response["entries"]:
                        print(book.get("title", "No title available"))

                input("Press Enter to continue...")
            if option == "3":
                app.process_local_catalog()
                print("Process $ Deduplicate Local Catalog File")
                input("Press Enter to continue...")

            if option == "4":
                app.generate_analytical_reports()

            if option == "5":
                app.database_administration_menu()

            if option == "6":
                app.run_quality_checks()
            if option == "0":
                print("Exiting the program.")
                break
        except KeyboardInterrupt:
            print("\nExiting the program.")
            break
