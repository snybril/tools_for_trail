import tkinter

INPUTGPX_Types = [ ( "Fichier GPX" , ".gpx" )  ]
OUTPUTCSV_Types = [ ( "Fichier CSV" , ".csv" )  ]

base_directory_example = "C:/Dev/perso/tools_for_trail/examples/"
base_filename = "court-course"
prefix_export = "export-"
suffix_dropped = "-dropped"
suffix_aggregate = "-aggregate"
example_file_to_open = base_directory_example+base_filename+INPUTGPX_Types[0][1]
example_file_to_save = base_directory_example+prefix_export+base_filename+OUTPUTCSV_Types[0][1]
example_file_to_save_dropped = base_directory_example\
                               +prefix_export+base_filename+suffix_dropped+OUTPUTCSV_Types[0][1]
example_file_to_save_aggregate = base_directory_example\
                               +prefix_export+base_filename+suffix_aggregate+OUTPUTCSV_Types[0][1]
#associated stats by strava Saint Max Trail (SMT16) 27/09/20:  16,07 km,  1034m deniv, 1:55:19


def get_gui_input_file():
    return tkinter.filedialog.askopenfilename (
        title ="Open file ...",
        filetypes = INPUTGPX_Types)


def get_gui_output_file():
    return tkinter.filedialog.asksaveasfilename(
        title="Save as ...",
        filetypes=OUTPUTCSV_Types,
        defaultextension=".csv")
