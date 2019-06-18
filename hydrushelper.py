"""
Hydrus helper is module containing various functions for working with Hydrus
output files and processing them in Jupyter Notebooks

For now the functions are:

- copy_output():
    It will copy the selected files from temporary working directory of a
    Hydrus project to a Hydrus/project_name subdirectory.
"""
# some imports first
import glob
import os
import sys
import pathlib
from shutil import copyfile
import pandas as pd
from tkinter import *
from tkinter.filedialog import askopenfilename


def copy_output():
    """
    Copy specified Hydrus output file(s) for a specified project
    to a working folder of this function (script),
    (if other destination is not specified. #should be implemented later)
    Works only for Temp working directory,
    which exists only if some project is open.

    Parameters
    ----------
    (project_name) : string
        Need to be entered after a prompt of this function.
        All avaible projet names will be listed.
    (file_name) : string
        Need to be entered after a prompt of this function.
        All avaible output files will be listed

    Returns
    -------
    copy of the original file(s)
    """

    working_path = "C:\\HYDRUS\\Temp\\~Hydrus3D_2xx\\"
    cwd = os.getcwd()

    # creating and printing list of all projects in Hydrus working folder
    out_p = [p.split("\\")[-1] for p in glob.glob(working_path + "*")]
    out_p.remove('Hydrus3D_2xx.tmp')
    print("List of projects in the Hydrus working directory:")
    for p in out_p:
        print(p)
    print("")

    # choice of project with desired output files
    project = input("Enter the projet name from the printed list: ")
    print("")

    while project not in out_p:
        print("There is no such project name %s" % project)
        project = input(
            "Check the list again and enter an existing projet name: "
            )
        print("")

    # creating and printing list of all output files
    out_f = [f.split("\\")[-1] for f in glob.glob(
                                    working_path + project + "\\" + "*.out")]
    print("List of output files in the %s working directory" % project)
    for f in out_f:
        print(f.split("\\")[-1])
    print("")

    # creating the list of files to copy from user input
    files = input("Enter the file name(s) you want to copy: ")
    if "," in files:
        files = [x.strip() for x in files.split(',')]
    else:
        files = [x.strip() for x in files.split(' ')]

    # check if all the file names are right
    result = all(elem in out_f for elem in files)
    print("")

    # if not run it again with check
    while not result:
        print("Some error is in file(s) name(s)")
        files = input(
            "Check the list again and enter the output files names: ")
        print("")
        if "," in files:
            files = [x.strip() for x in files.split(',')]
        else:
            files = [x.strip() for x in files.split(' ')]

        result = all(elem in out_f for elem in files)

    # finally the copy of files will be done
    for name in files:
        print("Filename: %s" % name)
        source = working_path + project + "\\" + name
        print("Source: %s" % source)
        pathlib.Path(
            cwd + "\\hydrus\\" + project + "\\"
                ).mkdir(parents=True, exist_ok=True)
        destination = cwd + "\\hydrus\\" + project + "\\" + name
        print("Destination: %s" % destination)
        copyfile(source, destination)
        print("file %s succesefuly copied to %s" % (name, destination))


def read_file(proc_type='flow'):
    """
    Function will read the specific composition of a hydrus output file and
    convert it to a dataframe.
    Now it works only for the "v_Mean.out" file type

    args:
    proc_type: string
        Optional argument for better processing of the Hydrus output according
        your simulation type.
        Values for choice are:
            - flow - only flow simulation (default value)
            - tracer - solution simulation with one solute (tracer)
            - cwm1 - biokinetic simulation with CWM1 model
            - cw2d - biokinetic simulation with CW2D model

    Parameters
    ----------
    filepath : string
        Full or relative path to the file

    Returns
    -------
    pandas dataframe
    """
    proc_types = ['flow', 'tracer', 'cwm1', 'cw2d']
    if proc_type not in proc_types:
        raise ValueError(
            "Invalid process type. Expected one of: %s" % proc_types
            )

    root = Tk()
    root.update()
    filepath = askopenfilename()
    root.destroy()

    filepath = filepath.replace('/', '\\')

    # dictionaries for renaming columns in the returned dataframe
    v_mean_col = {
        "Time": "time",
        "rAtm": "pot_surface_flux_atm",
        "rRoot": "pot_transp_rate",
        "vAtm": "act_surface_flux_atm",
        "vRoot": "act_transp_rate",
        "vKode3": "total_bottom flux",
        "vKode1": "total_boundary_flux",
        "vSeep": "total_seepage_flux",
        "vKode5": "total_b_node_flux",
        "Runoff": "average_surface_ runoff",
        "Evapor": "average_evapor_flux",
        "Infiltr": "average_infil_flux",
        "SnowLayer": "surface_snow_layer"
    }

    cum_q_col = {
        "Time": "time",
        "CumQAP": "c_pot_surface_flux_atm",
        "CumQRP": "c_pot_transp_rate",
        "CumQA": "c_act_surface_flux_atm",
        "CumQR": "c_act_transp_rate",
        "CumQ3": "c_total_bottom flux",
        "CumQ1": "c_total_boundary_flux",
        "CumQS": "c_total_seepage_flux",
        "CumQ5": "c_total_b_node_flux",
        "cRunoff": "c_surface_ runoff",
        "cEvapor": "c_evapor_flux",
        "cInfiltr": "c_infil_flux",
    }

    obsnode_col = {
        "hNew": "hNew.0",
        "theta": "theta.0",
        "Temp": "Temp.0",
        "Conc": "Conc.0",
        "Sorb": "Sorb.0"
    }

    col_cwm1 = {
        "Conc.0": "oxygen.1",
        "Conc.1": "readillyCOD.1",
        "Conc.2": "acetat.1",
        "Conc.3": "in_sol_COD.1",
        "Conc.4": "NH4.1",
        "Conc.5": "NO3.1",
        "Conc.6": "SSO4.1",
        "Conc.7": "H2S.1",
        "Conc.8": "slowlyCOD.1",
        "Conc.9": "in_part_COD.1",
        "Sorb.10": "heterotrophic.1",
        "Sorb.11": "autotrophic.1",
        "Sorb.12": "fermenting.1",
        "Sorb.13": "methanogenic.1",
        "Sorb.14": "sulphate_reducing.1",
        "Sorb.15": "sulphide_oxidising.1",
    }

    if "v_Mean.out" in filepath:
        data = pd.read_csv(filepath,
                           engine='python',
                           skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12],
                           sep=" ",
                           skipinitialspace=True,
                           skipfooter=1
                           )

        data = data.loc[:, (data != 0).any(axis=0)]
        data = data.rename(v_mean_col, axis='columns')

        print("Data from %s were read into the Pandas DataFrame" % filepath)
        return data

    elif "Cum_Q.out" in filepath:
        data = pd.read_csv(filepath,
                           engine='python',
                           skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12],
                           sep=" ",
                           skipinitialspace=True,
                           skipfooter=1
                           )

        data = data.loc[:, (data != 0).any(axis=0)]
        data = data.rename(cum_q_col, axis='columns')

        print("Data from %s were read into the Pandas DataFrame" % filepath)
        return data

    elif "ObsNod.out" in filepath:

        if proc_type == "cwm1":
            data = pd.read_csv(filepath,
                               engine='python',
                               skiprows=[0, 1, 2, 3, 4],
                               sep=" ",
                               skipinitialspace=True,
                               skipfooter=1
                               )

            data = data.rename(obsnode_col, axis='columns')
            data = data.rename(col_cwm1, axis='columns')
            data = data.loc[:, (data != 0).any(axis=0)]

        else:
            data = pd.read_csv(filepath,
                               engine='python',
                               skiprows=[0, 1, 2, 3, 4],
                               sep=" ",
                               skipinitialspace=True,
                               skipfooter=1
                               )

            data = data.rename(obsnode_col, axis='columns')
            data = data.loc[:, (data != 0).any(axis=0)]

        print("Data from %s were read into the Pandas DataFrame" % filepath)
        return data

    else:
        print("Sorry, data reader for this file type is not yet implemented.")
