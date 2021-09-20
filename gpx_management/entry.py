from gpx_management import stats


class Entry:
    def __init__(self):
        self.local_duration = 0
        self.local_dist = 0
        self.local_elevation = stats.FAKE_VALUE
        self.local_slope = 0
        self.local_speed = 0
        self.local_vert_speed = 0
        self.time = 0
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0


    def writeHeader(self, writer):
        writer.writerow(['time', 'latitude', 'longitude', 'altitude', 'distance',
                             'elevation', 'slope', 'duration', 'speed', 'vertical speed'])

    def writeEntry(self, writer):
        writer.writerow([
            str(self.time),
            str(self.latitude),
            str(self.longitude),
            str(self.altitude),
            str(self.local_dist),
            str(self.local_elevation),
            str(self.local_slope),
            str(self.local_duration),
            str(self.local_speed),
            str(self.local_vert_speed)])

    def computeEntry(self, previous_point, point):
        self.time = point.time
        self.latitude = point.latitude
        self.longitude = point.longitude

        self.local_duration = point.time - previous_point.time

        self.local_dist = previous_point.distance_2d(point)
        if self.local_duration.total_seconds() == 0:
            self.local_speed = stats.FAKE_VALUE
        else:
            self.local_speed = self.local_dist / self.local_duration.total_seconds()

        if point.has_elevation() \
                and previous_point.has_elevation() \
                and previous_point.elevation != stats.FAKE_VALUE\
                and self.local_duration.total_seconds() != 0:
            self.local_elevation = point.elevation - previous_point.elevation
            self.altitude = point.elevation
            self.local_slope = self.local_elevation * 100 / self.local_dist
            self.local_vert_speed = self.local_elevation / self.local_duration.total_seconds()
        else:
            self.local_elevation = stats.FAKE_VALUE  # to ease filtering if needed
            self.local_slope = stats.FAKE_VALUE
            self.local_vert_speed = stats.FAKE_VALUE
