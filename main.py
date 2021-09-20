# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import gpx_management.create_csv_from_gpx
import gui.file_helper

# Press the green button in the gutter to run the script.
import learn.learn_from_csv

if __name__ == '__main__':
    filename_to_open=gui.file_helper.example_file_to_open
    print(f"file to open {filename_to_open}")

    filename_to_save=gui.file_helper.example_file_to_save
    print(f"file to save {filename_to_save}")

    filename_to_save_dropped=gui.file_helper.example_file_to_save_dropped
    print(f"file to save {filename_to_save_dropped}")

    filename_to_save_aggregate=gui.file_helper.example_file_to_save_aggregate
    print(f"file to save {filename_to_save_aggregate}")

    gpx_management.create_csv_from_gpx.compute_gpx(
        filename_to_open,
        filename_to_save,
        filename_to_save_dropped,
        filename_to_save_aggregate)

    learn.learn_from_csv.learn_from_csv(filename_to_save_aggregate)

