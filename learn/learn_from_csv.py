import csv


def learn_from_csv(filename_to_open_aggregate) -> None:
    csv_aggregate = open(filename_to_open_aggregate, newline='')
    aggregate_reader = csv.reader(csv_aggregate)

    for row in aggregate_reader:

        print('{0} '.format(row[2]))
