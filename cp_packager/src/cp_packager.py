#!/usr/bin/env python

"""
General purpose packager utility for UArizona Coyote Papers
https://coyotepapers.sbs.arizona.edu/

Author & Digital Archivist: Damian Romero
Winter, 2020

Last tested on Python 3.8.5

This program was ported to Python for sustainability purposes.

TODO:
    #2 use .gitignore files or a .deldefault file to remove unwanted files
"""

import argparse
from csv import DictReader
from pathlib import Path
import shutil
import sys


def file_exception_handler(fpath: object, dryrun: bool):
    """Check files needed to create dirs. All file errors are fatal."""
    if not dryrun:
        if fpath.exists():
            print(f"*** Your file `{fpath.name}` is being procesed ***")
        else:
            print(f"\n*** WARNING: FATAL ERROR. Your file `{fpath.name}` does not exist. ***")
            print("*** Check that your file is correctly named and placed in the right folder and come back ***")
            sys.exit(1)


def dir_exception_handler(dpath: object,
                          dryrun: bool,
                          dirs_created: list = [],
                          overwrite: bool = False) -> bool:
    """Check if directories to be created exist or if user wants to overwrite them.
    
    *Note: Directories created during this session are overlooked.
    
    Parameters
    ----------
        dpath: pathlib Path object
            The path to the directory that will be checked for creation
        dirs_created
            A list of paths of previously created directories during this session
            
    Reurns
    ------
        overwrite
            A bool to be passed down to create_directory()
    """
    # If this dir was created during this session, do not create it again
    if dpath in dirs_created:
        return False
    elif dpath.exists():
        if dryrun == False:
            # Get user input
            while overwrite not in ['Y', 'y', 'N', 'n', True]:
                overwrite = input(f"\n*** WARNING: Your directory `{dpath.name}` already exists. Overwrite? Y/N:  ")
            if overwrite == True or overwrite.lower() == 'y':
                print(f"Your directory `{dpath.name}` will be overwritten\n")
                shutil.rmtree(dpath)  # shutil is necessary since path.rmdir() fails if dir is not empty
                return True
            else:
                print(f"Your directory `{dpath.name}` is safe\n")
                return False
        else:  # If dry run:
            print(f"\n*** WARNING: This is a dry run but if you run cp_packager in normal mode,")
            print(f"*** your directory `{dpath.name}` may be overwritten")
    else:
        return True


def create_directory(dirpath: object, dryrun: bool):
    """Handles the creation of directories for cp_packager

    Note
    ----------
        Always called after `dir_exception_handler()` so no exceptions are expected
    
    Parameters
    ----------
        dirpath: pathlib Path object
            The path of the directory to be created
        dryrun
            A boolean indicating if the program should be fully run or run in dry mode 
    """
    if not dryrun:
        try:
            dirpath.mkdir()
        except FileExistsError as error:
            raise error
        else:
            print(f"Creating new directory: {dirpath.name}")
            return(dirpath)


def read_tsv(ifile: str, delim: str = '\t'):
    """Reads in a tab-separated file and yields a dict for each row in table"""
    with open(ifile, mode='r') as tsv:
        reader = DictReader(tsv, delimiter= delim)  #missing values default to None
        for row in reader:
            yield row


def make_package(dict_row: dict,
                 all_created_dirs: list,
                 content: list,
                 papers_path: object,
                 out_path: object,
                 dry_run: bool = False,
                 force_create: bool = False) -> list:
    """Creates directories in `out_path` tailored for every reviewer
    
    Parameters
    ----------
        dict_row
            a dictionary row, tipically from `read_tsv()` with the keys:
                - paper: the name (and extension) of the file corresponding to a paper
                - reviewer1: the name of a reviewer assigned to this article
                - reviewer2..n: at least one reviewer is required. There is no maximum

        all_created_dirs
            full list of created directories during this session

        content: list of pathlib Path objects
            List of file paths of the common files to populate the new dirs

        *_path: pathlib Path objects
            Necessary folder structure for cp_packager to work. Defined in main()

        dry_run
            a boolean indicating if the program should be fully run or run in dry mode 
    
    Output
    ------
        X number of directories inside `out_path` where X is the total number of
        reviewers.

        Each directory will be named with the reviewer's name and will contain:
            - The paper(s) corresponding to that reviewer (stored in  `papers_path`)
            - All the files listed in content_path
        
    Note
    ----
        Any homonim files inside `out_path` will be skipped (not overwritten)

    Returns
    -------
        created_dirs_list
            A list of created directories for this table row to later be added
            to `all_created_dirs` in main()
    """

    # Check that this table row contains more than the paper file name
    assert len(dict_row) > 1, f"The {dict_row[0]} paper is missing reviewers"

    curr_paper = ''
    created_dirs_list = []

    # Loop through dictionary
    for index, k in enumerate(dict_row):
        # Tables are likely to contain extra spacing after content
        try:
            item = dict_row[k].strip()
        except AttributeError:
            raise AttributeError('Your table is not formatted correctly. ' +
                                 'Check that the tabs and spacing are '
                                 'consistant and try again.')


        # The first column should always be the file name of each paper
        # We store the path and skip the folder creation part
        if index == 0:
            curr_paper = item
            # Works only if the paper is named exactly as it is on the table
            file_exception_handler(papers_path.joinpath(curr_paper), dry_run)
            continue

        # Look for existing reviewer names to create dirs
        # Dict reader returns NONE in columns with missing values
        if item:
            newdir = out_path.joinpath(item)
            # Does newdir need to be created?
            if dir_exception_handler(dpath= newdir,
                                     dryrun= dry_run,
                                     dirs_created= all_created_dirs,
                                     overwrite= force_create):
                created_dir = create_directory(newdir, dry_run)
                created_dirs_list.append(created_dir)

            if not dry_run:
                # Copy the corresponding paper
                shutil.copyfile(papers_path.joinpath(curr_paper), newdir.joinpath(curr_paper))
                # Copy all the common files
                for f in content:
                    shutil.copyfile(f, newdir.joinpath(f.name))
    print()
    return created_dirs_list


def main(table_path: object,
         content_path: object,
         papers_path: object,
         output_path: object,
         test: bool = False,
         force: bool = False,
         ):
    """Main function for cp_packager.py

    Parameters
    ----------
    table_path: pathlib Path object
        Path to tsv with name of paper file and names of reviewers

    content_path: pathlib Path object
        The path to the content directory. Typically `../content/`

    papers_path: pathlib Path object
        The path to the papers directory. Typically `../papers/`

    output_path: pathlib Path object
        The path to the directory where reviewer subdirectories will be created.
        Typically `../output/`. If it doesn't exist this function will create it.

    test:
        Dry run flag

    force:
        Flag to bypass safe folder overwriting
    """
    all_created_dirs = []

    # Check if table exists
    file_exception_handler(fpath= table_path, dryrun= test)

    # Check if `output_path` exists, otherwise, create it
    if dir_exception_handler(dpath= output_path, dryrun= test, overwrite= force):
        create_directory(output_path, test)

    # Create dictionary generator from local tsv
    dict_gen = read_tsv(table_path)

    # Get file paths in `content_path`
    content_list = []
    for f in content_path.glob('*'):
        print(f)
        content_list.append(f)
        file_exception_handler(f, test)
    print()

    # Main loop for creating and populating directories
    while True:
        try:
            next_row = next(dict_gen)
        except StopIteration:
            print('Process completed')
            break

        new_dirs= make_package(next_row,
                     all_created_dirs = all_created_dirs,
                     content= content_list,
                     papers_path= papers_path,
                     out_path= output_path,
                     dry_run= test)

        for d in new_dirs:
            all_created_dirs.append(d)


if __name__ == "__main__":
    aparser = argparse.ArgumentParser(description= "Command-line tool for creating folders for CP reviewers")
    aparser.add_argument('--run',
                         required= True,
                         action= 'store_true',
                         help= "You can test this script by adding --test when running it")
    aparser.add_argument('--test',
                         required= False,
                         action= 'store_true',
                         help= "Perform a dry run where no folders are created")
    aparser.add_argument('--force',
                         required= False,
                         action= 'store_true',
                         help= "*-*WARNING*-*: this setting will overwrite folders without prompting")

    args = aparser.parse_args()
    print("\n*** Starting cp_packager ***")    

    # Name of the tsv file and its folder. Modify as needed.
    table_file = 'Papers-and-reviewers.tsv'  # Contains paper file names and reviewer names

    # Name of the directories to be used by cp_packager. Modify as-needed.
    input_folder = 'input'  # Contains tsv file.
    content_folder = 'content'  # Contains common files to be added to all packages
    papers_folder = 'papers'  # Contains articles (papers) to be added under specific reviewer names
    output_folder = 'output'  # Where packages will be created

    # Deal with directories placed in parent directory
    parent_dir = Path.cwd().parent

    input_path = parent_dir.joinpath(input_folder)
    content_path = parent_dir.joinpath(content_folder)
    paperst_path = parent_dir.joinpath(papers_folder)
    output_path = parent_dir.joinpath(output_folder)
    table_path = input_path.joinpath(table_file)

    main(table_path= table_path,
         test= args.test,
         force= args.force,
         content_path= content_path,
         papers_path= paperst_path,
         output_path= output_path)
