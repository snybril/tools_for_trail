from gpx_management import stats


class Filter:

    def checkFakeValue(entry):
        return Filter.checkValue(entry.local_dist,stats.FAKE_VALUE, 2, stats.FAKE_VALUE) and\
               Filter.checkValue(entry.local_elevation, stats.FAKE_VALUE, -stats.FAKE_VALUE, stats.FAKE_VALUE) and \
               Filter.checkValue(entry.local_speed, stats.FAKE_VALUE, 0, 6) and \
               Filter.checkValue(entry.local_vert_speed, stats.FAKE_VALUE, -1.5, 1.2)

    def checkValue(entry,fake_value, lower_limit, upper_limit):
        return entry != fake_value and\
               entry > lower_limit and\
               entry < upper_limit



