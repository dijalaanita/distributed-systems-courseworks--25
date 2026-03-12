import Pyro4
import time
import uuid

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class AuctionServer(object):
    def __init__(self):
        self.auctions = {}
        print("Auction Server initialized. Ready to accept auctions and bids.")

    def create_auction(self, item_name, starting_price, reserve_price, duration):
        auction_id = str(uuid.uuid4())[:6] # Generate a unique auction ID
        end_time = time.time() + duration

        self.auctions[auction_id] = {
            "item_name": item_name,
            "starting_price": starting_price,
            "reserve_price": reserve_price, # will be kept secret from buyers
            "active": True,
            "highest_bid": starting_price,
            "highest_bidder": 'N/A',
            "highest_bidder_name": 'None',
            "end_time": end_time
        }
        print(f"{item_name}, {auction_id} created successfully with starting price ${starting_price} and reserve price ${reserve_price}. Duration: {duration} seconds.")
        print(f"{len(self.auctions)} total auctions currently in the system.")
        return auction_id
    
    def active_auctions(self):
        # self._auto_close_expired() # Ensure we close any auctions that have ended before listing active ones
        current_time = time.time()
        active = {}
        print(f"Checking for active auctions... {len(self.auctions)} total auctions found.")
        
        for auction_id, details in self.auctions.items():
            time_left = details["end_time"] - current_time
            print(f"{auction_id}, {time_left} seconds left, active: {details['active']}")
            
            if details["active"] and time_left > 0:
                active[auction_id] = {
                    "item_name": details["item_name"],
                    "highest_bid": details["highest_bid"],
                    "time_remaining": int(time_left)
                    }
        return active
    
    def place_bid(self, auction_id, bidder_name, mobile, bid_amount):
        # self._auto_close_expired() # Ensure we close any auctions that have ended before accepting new bids

        if auction_id not in self.auctions:
            return "Auction ID not found."
        
        auction = self.auctions[auction_id]

        if not auction["active"]:
            return "Auction has ended."
        
        if bid_amount <= auction["highest_bid"]:
            return "Bid must be higher than the current highest bid."
        
        # Update the highest bid and bidder information
        auction["highest_bid"] = bid_amount
        auction["highest_bidder_mobile"] = mobile
        auction["highest_bidder_name"] = bidder_name
        print(f"New bid placed on {auction['item_name']} (ID: {auction_id}) by {bidder_name} with a bid of ${bid_amount}.")
        return "Bid placed successfully."
    
    def auto_close_auctions(self, auction_id):
        if auction_id not in self.auctions:
            return "Error: Auction ID not found."
        
        auction = self.auctions[auction_id]
        auction["active"] = False #seller can also manually close the auction by calling this method with the auction_id

        highest_bid = auction["highest_bid"]
        reserve_price = auction["reserve_price"]
        print(f"Closing auction {auction_id} for item {auction['item_name']}. Highest bid: ${highest_bid}, Reserve price: ${reserve_price}.")

        # creating daemon and register the server object
        if highest_bid >= reserve_price:
            # Successful Sale
            return (f"--- AUCTION CLOSED: SUCCESS ---\n"
                    f"Item: {auction['item_name']}\n"
                    f"Winner: {auction['highest_bidder_name']}\n"
                    f"Winning Bid: ${highest_bid}\n"
                    f"Contact Mobile: {auction['highest_bidder_mobile']}\n"
                    f"Status: Reserve price of ${reserve_price} was met.")
        else:
            # Unsuccessful Sale
            return (f"--- AUCTION CLOSED: NO SALE ---\n"
                    f"Item: {auction['item_name']}\n"
                    f"Highest Bid: ${highest_bid}\n"
                    f"Status: The highest bid did not meet the secret reserve of ${reserve_price}.")
        

    # def _auto_close_expired(self):
    #     current_time = time.time()
    #     for auction_id in self.auctions:
    #         if self.auctions[auction_id]["active"] and current_time > self.auctions[auction_id]["end_time"]:
    #             self.auctions[auction_id]["active"] = False


# creating daemon and register the server object
try:
    daemon = Pyro4.Daemon()
    name_server = Pyro4.locateNS()
    server_instance = AuctionServer()
    uri = daemon.register(server_instance, objectId="sixseven.auctionserver")
    name_server.register("sixseven.auctionserver", uri)

    print("Auction Server is ready.")
    print(f"SERVER URI: {uri}")
    print("COPY THE LINE ABOVE AND PASTE IT INTO THE CLIENTS")
    daemon.requestLoop()

except Exception as e:
    print(f"An error occurred while starting the Auction Server: {e}")