FAKE_VALUE = 2000  # a numeric value that cannot be real in order to spot anomalies

class GpxStats:

    def __init__(self):
        self.cumul_dist = 0
        self.cumul_climb = 0
        self.cumul_down = 0
        self.count_tracks = 0
        self.count_segments = 0
        self.max_dist = 0
        self.min_dist = 1000
        self.count_strange_dist = 0
        self.count_speed_sup_25 = 0
        self.count_speed_inf_2 = 0
        self.total_points = 0
        self.dropped_points = 0

    def incrementTracks(self):
        self.count_tracks += 1

    def incrementSegments(self):
        self.count_segments += 1

    def incrementTotalPoints(self):
        self.total_points += 1

    def incrementDroppedPoints(self):
        self.dropped_points += 1

    def computeGlobalStats(self, entry):
        if entry.local_dist > self.max_dist:
            self.max_dist = entry.local_dist
        if entry.local_dist < self.min_dist:
            self.min_dist = entry.local_dist

        self.incrementDistance(entry.local_dist)
        if entry.local_elevation > 0 \
                and entry.local_elevation != FAKE_VALUE:
            self.incrementClimb(entry.local_elevation)
        elif entry.local_elevation < 0:
            self.incrementDown(entry.local_elevation)

    def incrementDistance(self, distance):
        self.cumul_dist += distance

    def incrementClimb(self, climb):
        self.cumul_climb += climb

    def incrementDown(self, down):
        self.cumul_down += down
