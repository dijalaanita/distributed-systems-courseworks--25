import Pyro4
import time
import uuid

@Pyro4.expose
class AuctionServer(object):
    def __init__(self):
        self.auctions = {}

    def create_auction(self, item_name, starting_price, reserve_price, duration):
        auction_id = str(uuid.uuid4())[:6] # Generate a unique auction ID
        end_time = time.time() + duration

        self.auctions[auction_id] = {
            "item_name": item_name,
            "starting_price": starting_price,
            "reserve_price": reserve_price, # will be kept secret from buyers
            "active": True,
            "highest_bid": 0,
            "highest_bidder": None,
            "highest_bidder_name": None,
            "end_time": end_time
        }
        return auction_id
    
    def active_auctions(self):
        self._auto_close_auctions() # Ensure we close any auctions that have ended before listing active ones
        active = {}
        for auction_id, details in self.auctions.items():
            if details["active"]:
                active[auction_id] = {
                    "item_name": details["item_name"],
                    "starting_price": details["starting_price"],
                    "highest_bid": details["highest_bid"],
                    "time_remaining": max(0, int(details["end_time"] - time.time()))
                    }
        return active
    
    def place_bid(self, auction_id, bidder_name, mobile, bid_amount):
        self._auto_close_auctions() # Ensure we close any auctions that have ended before accepting new bids

        if auction_id not in self.auctions:
            return "Auction not found."
        
        auction = self.auctions[auction_id]

        if not auction["active"]:
            return "Auction has ended."
        
        if bid_amount <= auction["highest_bid"] or bid_amount < auction["starting_price"]:
            return "Bid must be higher than the current highest bid and starting price."
        
        # Update the highest bid and bidder information
        auction["highest_bid"] = bid_amount
        auction["highest_bidder"] = mobile
        auction["highest_bidder_name"] = bidder_name

        return "Bid placed successfully."
    
    def _auto_close_auctions(self, auction_id):
        if auction_id not in self.auctions:
            return "Error: Auction ID not found."
        
        auction = self.auctions[auction_id]
        auction["active"] = False #seller can also manually close the auction by calling this method with the auction_id

        # creating daemon and register the server object
        if auction["highest_bid"] >= auction["reserve_price"]:
            return (f"Auction closed.\n"
                    f"Winner: {auction['highest_bidder_name']} with a bid of {auction['highest_bid']}.")
        else:
            return (f"Auction closed. Reserve price ${auction['reserve_price']} not met, no winner.")
        

    def _auto_close_expired(self):
        current_time = time.time()
        for auction_id, details in self.auctions.items():
            if details["active"] and current_time >= details["end_time"]:
                details["active"] = False


# creating daemon and register the server object
try:
    daemon = Pyro4.Daemon()
    name_server = Pyro4.locateNS()

    uri = daemon.register(AuctionServer)
    name_server.register("sixseven.auctionserver", uri)

    print("Auction Server is ready.")
    daemon.requestLoop()

except Exception as e:
    print(f"An error occurred while starting the Auction Server: {e}")