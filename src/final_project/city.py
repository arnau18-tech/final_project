import numpy as np
import pandas as pd

class City:
    def __init__(self, size, area_rates, seed=42):
        self.size = size
        self.area_rates = area_rates
        self.step = 0
        self.rng = np.random.default_rng(seed)

        self.places = []
        self.hosts = {}

    def get_place(self, pid):
        return self.places[pid]

    def get_host(self, hid):
        return self.hosts[hid]

    def initialize(self):
        from .place import Place
        from .hosts import Host

        num = self.size * self.size
        self.places = []

        for pid in range(num):
            p = Place(pid, pid, self)
            p.setup()
            self.places.append(p)

        self.hosts = {}
        for pid, p in enumerate(self.places):
            h = Host(pid, p, self)
            self.hosts[pid] = h

    def approve_bids(self, bids):
        if not len(bids):
            return []

        df = pd.DataFrame(bids)
        df = df.sort_values("spread", ascending=False)

        approved = []
        used_buyers = set()
        used_places = set()

        for _, row in df.iterrows():
            pid = int(row["place_id"])
            buyer = int(row["buyer_id"])

            if buyer in used_buyers or pid in used_places:
                continue

            approved.append(row.to_dict())
            used_buyers.add(buyer)
            used_places.add(pid)

        return approved

    def execute_transactions(self, trans):
        for t in trans:
            pid = int(t["place_id"])
            seller = int(t["seller_id"])
            buyer = int(t["buyer_id"])
            bid_price = float(t["bid_price"])

            place = self.get_place(pid)
            s = self.get_host(seller)
            b = self.get_host(buyer)

            b.profits -= bid_price
            s.profits += bid_price

            s.assets.remove(pid)
            b.assets.add(pid)

            place.host_id = buyer
            place.price[self.step] = bid_price

    def clear_market(self):
        all_bids = []
        for h in self.hosts.values():
            all_bids.extend(h.make_bids())

        if not all_bids:
            return []

        approved = self.approve_bids(all_bids)
        if approved:
            self.execute_transactions(approved)
        return approved

    def iterate(self):
        self.step += 1

        for p in self.places:
            p.update_occupancy()

        for h in self.hosts.values():
            h.update_profits()

        return self.clear_market()

    def compute_wealth_dataframe(self):
        rows = []
        for h in self.hosts.values():
            value = 0
            for pid in h.assets:
                p = self.get_place(pid)
                latest = max(p.price.keys())
                value += p.price[latest]

            rows.append({
                "host_id": h.host_id,
                "area": h.area,
                "profits": h.profits,
                "asset_value": value,
                "wealth": h.profits + value
            })

        return pd.DataFrame(rows)
