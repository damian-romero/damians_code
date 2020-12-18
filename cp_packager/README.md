# Coyote Papers packager tool

## About

This code was originally created by me for my editing needs as part of the University of Arizona [Coyote Papers](https://coyotepapers.sbs.arizona.edu/) editorial team. The code is referenced in the [*Coyote Papers Proceedings* OSF project](https://osf.io/xk2n6/) and its private OSF projects.

If the code needs refactoring or if you find a bug, please [start a new issue](https://github.com/damian-romero/damians_code/issues) or feel free to [fork and contribute](https://guides.github.com/activities/forking/).

## Overview

The code in this repository automatically creates directory (folder) packages with all the necessary files for article reviewers. Those folders are then placed either in an online storage platform usually an [OSF private project](https://osf.io/) where reviewers can be given editing access so that they can view the articles they must review and upload their reviews according to the instructions.

Note that all files here are sample files. To actually run the program you must download it to your computer and replace the files with the most up-to-date versions in [*Coyote Papers Proceedings* OSF project](https://osf.io/xk2n6/).

To run the code you can either `git clone` this repository or you can [download it](https://github.com/damian-romero/damians_code/archive/main.zip), unzip it and run it. You will need the following folder structure:

```markdown
.
├── .gitignore                              #  Not needed
├── LICENSE                                 #  Not needed
├── README.md                               #  Not needed
└── cp_packager                             #
    ├── README.md                           #
    ├── content                             # Any files that need to be part of each reviewer's package must live here
    │   ├── Author_General_Guidelines.pdf   #
    │   └── Reviewer_Guidelines.pdf         # 
    ├── input                               # A [tab-separated table file](https://en.wikipedia.org/wiki/Tab-separated_values)
    │   └── Papers-and-reviewers.tsv        #   with the file names of the articles and the names of the reviewers for each article
    ├── output                              # The pakages (folders) with the reviewer names will be created here
    ├── papers                              # The articles that need reviewing
    │   ├── Author1_ALCx.pdf                #   - Sample paper, pdf
    │   ├── Author2_ALCx.docx               #   - Sample paper, MSWord
    │   └── Author3_ALCx.pdf                #   - Sample paper, pdf
    └── src
        └── cp_packager.py                  # Run the script from here
```

## Changelog

v0.1.0
    * First GH release
    * Used in the ALC 14 Proceedings
    * Works on MacOS and Linux

## Author

Damian Romero (@damian-romero)

## Contributors

See the contributors [list](https://github.com/damian-romero/damians_code/graphs/contributors)