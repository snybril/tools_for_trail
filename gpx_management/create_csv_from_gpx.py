import gpxpy.gpx
import csv

import gpx_management.stats
from gpx_management.aggregate import Aggregate
from gpx_management.entry import Entry
from gpx_management.filter import Filter


def compute_gpx(filename_to_open,
                filename_to_save,
                filename_to_save_dropped,
                filename_to_save_aggregate
                ) -> None:
    gpx_file = open(filename_to_open, 'r')
    gpx = gpxpy.parse(gpx_file)

    stats = gpx_management.stats.GpxStats()
    entry = Entry()

    csvfile = open(filename_to_save, 'w', newline='')
    csvfile_dropped = open(filename_to_save_dropped, 'w', newline='')
    filewriter = csv.writer(csvfile, dialect='excel')
    filewriter_dropped = csv.writer(csvfile_dropped, dialect='excel')

    csvfile_aggregate = open(filename_to_save_aggregate, 'w', newline='')
    filewriter_aggregate = csv.writer(csvfile_aggregate, dialect='excel')

    entry.writeHeader(filewriter)
    entry.writeHeader(filewriter_dropped)

    aggregate = Aggregate(0.15,0.5,10,filewriter_aggregate)

    print('total distance(2d) {0}, total distance(3d) {1}, {2}'.format(
        gpx.length_2d(), gpx.length_3d(), gpx.get_uphill_downhill()))

    for track in gpx.tracks:
        stats.incrementTracks()
        for segment in track.segments:
            stats.incrementSegments()
            previous_point = segment.points[0]

            for point in segment.points:
                entry.computeEntry(previous_point, point)
                stats.incrementTotalPoints()
                if not Filter.checkFakeValue(entry):
                    stats.incrementDroppedPoints()
                    entry.writeEntry(filewriter_dropped)

                    print('Drop Point at {0}, ({1},{2}) alt: {3}, local distance: {4}, duration: {5}, local speed: {6}, local vert speed: {7}'
                       .format(point.time, point.latitude, point.longitude, point.elevation, entry.local_dist, entry.local_duration, entry.local_speed, entry.local_vert_speed))
                else:
                    stats.computeGlobalStats(entry)
                    entry.writeEntry(filewriter)
                    aggregate.addEntry(entry)
                previous_point = point

    print('nb tracks : {0}, nb segments : {1}'.format(stats.count_tracks, stats.count_segments))
    print('min dist : {0}, max dist : {1}, count less than 2 km/h: {2}, more than 25 km/h: {3}'.format(
        stats.min_dist,
        stats.max_dist,
        stats.count_speed_inf_2,
        stats.count_speed_sup_25))

    print('total distance {0}, total uphill {1}'.format(gpx.length_2d(),
                                                        gpx.get_uphill_downhill()))
    print('cumulated distance {0}, cumul climb {1}, cumul down {2}'.format(
        stats.cumul_dist,
        stats.cumul_climb,
        stats.cumul_down))
    print('dropped points {0} / {1} -> {2}%'.format(stats.dropped_points,
                                            stats.total_points,
                                            round(100*stats.dropped_points/stats.total_points,2)))
