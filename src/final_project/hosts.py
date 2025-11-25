from dataclasses import dataclass, field

@dataclass
class Host:
    host_id: int
    place: "Place"
    city: "City"
    profits: float = 0.0
    assets: set = field(default_factory=set)

    def __post_init__(self):
        self.area = self.place.area
        self.assets.add(self.place.place_id)

    def update_profits(self):
        total = 0
        for pid in self.assets:
            place = self.city.get_place(pid)
            monthly = place.rate * place.occupancy
            total += monthly
        self.profits += total

    def make_bids(self):
        bids = []
        city = self.city
        opps = set()

        for pid in self.assets:
            place = city.get_place(pid)
            for n in place.neighbours:
                if n not in self.assets:
                    opps.add(n)

        for pid in opps:
            place = city.get_place(pid)
            latest = max(place.price.keys())
            ask = place.price[latest]

            if self.profits >= ask:
                bids.append({
                    "place_id": pid,
                    "seller_id": place.host_id,
                    "buyer_id": self.host_id,
                    "spread": self.profits - ask,
                    "bid_price": self.profits
                })

        return bids
