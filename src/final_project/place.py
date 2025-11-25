import numpy as np

class Place:
    def __init__(self, place_id, host_id, city):
        self.place_id = place_id
        self.host_id = host_id
        self.city = city

        self.neighbours = []
        self.area = None
        self.rate = None
        self.price = {}
        self.occupancy = 0

    def setup(self):
        size = self.city.size
        rng = self.city.rng

        row = self.place_id // size
        col = self.place_id % size
        self.row = row
        self.col = col

        neighbours = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < size and 0 <= nc < size:
                    neighbours.append(nr * size + nc)
        self.neighbours = neighbours

        half = size // 2
        bottom = row < half
        left = col < half

        if bottom and left:
            self.area = 0
        elif bottom and not left:
            self.area = 1
        elif not bottom and left:
            self.area = 2
        else:
            self.area = 3

        low, high = self.city.area_rates[self.area]
        self.rate = rng.uniform(low, high)

        self.price = {0: 900 * self.rate}

    def update_occupancy(self):
        rng = self.city.rng

        area_rates = [p.rate for p in self.city.places if p.area == self.area]
        area_mean = float(np.mean(area_rates))

        if self.rate > area_mean:
            self.occupancy = rng.integers(5, 16)
        else:
            self.occupancy = rng.integers(10, 21)

