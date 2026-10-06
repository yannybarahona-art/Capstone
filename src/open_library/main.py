if __name__ == "__main__":
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
                subject=input("Enter the subject to ingest works: ")
                pages=input("Enter the number of pages to ingest: ")

            if option == "2":
                print("Search Books by Author/Title/ISBN")
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