import Pyro4

def main():
    try:
        uri = input("Enter the URI of the Auction Server (e.g., PYRONAME:sixseven.auctionserver): ")
        auction_server = Pyro4.Proxy(uri)
        auction_server._pyroBind()  # Bind to the server to check connection
        print("Connected to Auction Server.")


    except Exception as e:
        print("Error: Could not connect to Auction Server.")
        return 

    while True:
        print("\n--- BIDDER CLIENT ---")
        print("1. get active auctions")
        print("2. Place a Bid")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Implementation for getting active auctions
            try:
                # get the list of active auctions
                auctions = auction_server.active_auctions()
                if not auctions:
                    print("No active auctions at the moment.")
                else:
                    print("\nActive Auctions:")
                    for auction_id, details in auctions.items():
                        print(f"ID: {auction_id}, Item: {details['item_name']}, Highest Bid: ${details['highest_bid']}, Time Remaining: {details['time_remaining']} seconds")
            except Exception as e:
                print("Error: Could not retrieve active auctions.")
                print(f"Details: {e}")

        elif choice == '2':
            auction_id = input("Enter auction ID to place a bid on: ")
            bidder_name = input("Enter your name: ")
            mobile = input("Enter your mobile number: ")

            try:
                bid = float(input("Enter your bid amount: $"))
                result = auction_server.place_bid(auction_id, bidder_name, mobile, bid)
                print(f"\n{result}")
            except ValueError:
                print("Invalid input. Please enter a numeric value for the bid amount.")
            except Exception as e:
                print("Error: Could not place bid.")
                print(f"Details: {e}")
        
        elif choice == '3':
            print("Exiting client...")
            break
        else: 
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()