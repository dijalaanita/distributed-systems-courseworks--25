import Pyro4

def main():
    try:
        uri = input("Enter the URI of the Auction Server (e.g., PYRONAME:sixseven.auctionserver): ")
        auction_server = Pyro4.Proxy(uri)
        auction_server._pyroBind()  # Bind to the server to check connection
        print("Connected to Auction Server.")
    except Exception as e:
        print("Error: Could not connect to Auction Server.")
        print(f"Details: {e}")
        return
    
    while True:
        print("\n--- SELLER Client ---")
        print("1. Create Auction")
        print("2. Close Auction")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                item = input("Enter item name: ")
                start = float(input("Enter start price: $"))
                reserve = float(input("Enter reserve price: $"))
                duration = int(input("Enter auction duration (in seconds): "))

                # create auction
                auction_id = auction_server.create_auction(item, start, reserve, duration)
                print(f"Auction created successfully with ID: {auction_id}")
            except Exception as e:
                print("Error: Could not create auction.")
                print(f"Details: {e}")
            except ValueError:
                print("Invalid input. Please enter numeric values for price and duration.")
        elif choice == '2':
            auction_id = input("Enter auction ID to close: ")
            try:
                #closing the auction
                result = auction_server.auto_close_auctions(auction_id)
                print(f"\n{result}")
            except Exception as e:
                print("Error: Could not close auction.")
                print(f"Details: {e}")
        elif choice == '3':
            print("Exiting client...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()