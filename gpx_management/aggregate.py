from datetime import timedelta

from gpx_management.entry import Entry


class Aggregate:
    def __init__(self,min_dist_effort,
                 max_dist_effort, # whatever slope difference, aggregate have this length as minimal
                 tolerance_slope, # used to separate aggregates if the slope is very different
                 filewriterAggregate):
        self.min_dist_effort = min_dist_effort
        self.max_dist_effort = max_dist_effort
        self.tolerance_slope=tolerance_slope
        self.filewriterAggregate = filewriterAggregate
        self.reset()
        self.writeHeader(self.filewriterAggregate)

    def reset(self):
        self.count_entry = 0
        self.cumul_dist = 0
        self.cumul_elevation = 0
        self.cumul_climb = 0
        self.cumul_down = 0

        self.cumul_duration = timedelta()
        self.km_effort = 0
        self.mean_slope = 0
        self.mean_speed = 0
        self.mean_vert_speed = 0
        self.latest_entry = Entry()

    def checkSlope(self, entry):
        if entry.local_slope > self.mean_slope \
                and entry.local_slope-self.mean_slope > self.tolerance_slope:
            return False
        if entry.local_slope < self.mean_slope \
                and self.mean_slope-entry.local_slope > self.tolerance_slope:
            return False
        return True

    def addEntry(self, entry):
        self.cumul_duration += entry.local_duration
        self.cumul_dist += entry.local_dist
        if entry.local_elevation > 0:
            self.cumul_climb += entry.local_elevation
        else:
            self.cumul_down -= entry.local_elevation
        self.km_effort += entry.local_dist/1000
        self.cumul_elevation += entry.local_elevation
        if entry.local_elevation > 0:
            self.km_effort += entry.local_elevation/100

        self.count_entry += 1

        if self.km_effort > self.min_dist_effort and self.checkSlope(entry):
            self.endAggregate(entry)

        # Check and stop the aggregate if sup to max km effort
        if self.km_effort > self.max_dist_effort:
            self.endAggregate(entry)


    def endAggregate(self, entry):
        self.latest_entry = entry
        self.mean_slope = self.cumul_elevation * 100 / self.cumul_dist
        self.mean_speed = 16.6667 / (self.cumul_dist / self.cumul_duration.total_seconds())
        self.mean_vert_speed =  self.cumul_elevation / (self.cumul_duration.total_seconds()/60)

        self.writeAggregate(self.filewriterAggregate)
        self.reset()

    def writeHeader(self, writer):
        writer.writerow(['time', 'nb_entries', 'latitude', 'longitude', 'altitude', 'distance',
                             'elevation', 'climb', 'down', 'slope', 'duration', 'speed (min/km)', 'vertical speed (m/min)'])

    def writeAggregate(self, writer):
        writer.writerow([
            str(self.latest_entry.time),
            str(self.count_entry),
            str(self.latest_entry.latitude),
            str(self.latest_entry.longitude),
            str(self.latest_entry.altitude),
            str(self.cumul_dist),
            str(self.cumul_elevation),
            str(self.cumul_climb),
            str(self.cumul_down),
            str(self.mean_slope),
            str(self.cumul_duration),
            str(self.mean_speed),
            str(self.mean_vert_speed)])

