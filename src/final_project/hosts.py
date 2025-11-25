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
        """
        Host identifies neighbouring listings and bids on any it can afford.

        Regla v0 (original):
            - si profits >= ask_price -> puja con todo self.profits

        Regla v1 (modificada):
            - el host solo puede usar como máximo el 70% de sus profits para pujar
            - así conserva liquidez y se reduce la expansión agresiva
        """

        bids = []
        city = self.city
        opps = set()

        # Oportunidades: vecinos de todas las propiedades que posee
        for pid in self.assets:
            place = city.get_place(pid)
            for n in place.neighbours:
                if n not in self.assets:
                    opps.add(n)

        for pid in opps:
            place = city.get_place(pid)
            latest = max(place.price.keys())
            ask = place.price[latest]

            if city.rule_version == 0:
                # -------- REGLA ORIGINAL (v0) --------
                if self.profits >= ask:
                    bids.append({
                        "place_id": pid,
                        "seller_id": place.host_id,
                        "buyer_id": self.host_id,
                        "spread": self.profits - ask,
                        "bid_price": self.profits,
                    })
            else:
                # -------- REGLA MODIFICADA (v1) --------
                max_budget = self.profits * 0.7
                if max_budget >= ask:
                    bids.append({
                        "place_id": pid,
                        "seller_id": place.host_id,
                        "buyer_id": self.host_id,
                        "spread": max_budget - ask,
                        "bid_price": max_budget,
                    })

        return bids

