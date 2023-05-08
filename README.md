# Modular gravity-based suspension system for gilt leather wall hangings
This repository is included in a paper named:  "Modular gravity-based suspension system for gilt leather wall hangings", published in september 2023 by ICOM-CC and contains information about the suspension system, including detailed drawings as well as data that has been collected, describing the behaviour of the leater over a period of a year.

The suspension and monitoring system is open access and distributed under the terms of the CC BY-SA 4.0 license. https://creativecommons.org/licenses/by-sa/4.0/

Structure
------------
This repository contains the following directories:

* **materials_suppliers**: 14 detailed drawings (in DXF-format) of the mounting system, including size and dimensions. More information can be found in the directory (info.pdf).

* **data**: file (.csv) containing data describing the behaviour of wall hangings mounted on the suspension system in the Regentessenkamer at Voormalig Weeshuis Enkhuizen, including the displacement of the leather (in horizontal and vertical direction), as well as temperature and relative humidity.

* **scripts**: custom scripts written in Python. One script can be used to extract the information in the .csv file and convert it to a Pandas dataframe (read_data.py). The other two scripts reproduce Figure 7 (fig7_mm.py) and 8 (fig8_40perc.py) in Brands et al. (2023), visualizing the behaviour of the leather over time. 

* **plots**: files containing the outputs from the custom scripts used to visualize the data.

## Installation
Clone the git repository to create a local copy with the following command:

    $ git clone git@github.com:ABra1993/LeatherAnalysis.git

Supplementary info
------------
Additional information about the analysis about the leather can be found here:
https://docs.google.com/document/d/1wCsgwAU4O0nHiB8O62IX6cypKUmrL2wZS21t7bLyCXc/edit#

Disclaimer
------------
We have made every attempt to ensure the accuracy and reliability of the information provided on this website. However, the information provided is “as is” without warranty of any kind. We do not accept any responsibility or liability for the accuracy, content, completeness, legality, or reliability of the information contained on this repository.
