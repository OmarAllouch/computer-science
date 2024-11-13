# Practical Work 1

This practical work is made up of 4 parts, each of which is a separate task.
I included a Makefile in the root of this project to allow running each task that contains something to run.
**Please ensure you're in the root of the project when running the commands, otherwise the python scripts will fail (due to the relative paths).**

## 01 - LoRaWAN sensor payload

The first task is to decode a LoRaWAN sensor payload.
The `main.py` script reads different types of inputs and outputs the status, battery level, temperature, and events count.
The script is run by executing the following command:
```bash
make 1
```

## 02 - ENTSOE

The second task consists of loading csv files and computing the sum of values in column LengthOfCircuits in both files.
The results are in `results.md`, and a video showing the import is also available (in the `02` folder).

## 03 - GeoNames

In the third task, we first load a txt file in Calc and separate the columns by the tab character.
Then, we do some parsing of the files to extract some data.
In the first part, we extract data from the `admin1CodesASCII.txt` and `countryInfo.txt` files to write a csv files containing the country code, country name, and the number of admin1 regions in the country.
In the second part, we get a place name from the user as input, and we need to get some information about the place with the least number of file parsing possible.
The scripts for the first and second parts are respectively `main.py` and `geo-info.py`, and can both be run at the same time using:
```bash
make 3
```
Also a video showing the import and a quick execution of the scripts is available in the `03` folder.

## 04 - GitHub issues

In this final task I first need to show my ability to format, validate and syntax highlight JSON files, online and in my preferred text editor (see video).
Then, I need to write a script that fetches the issues of a GitHub repository and writes them to a csv file.
The first part is demonstrated in the video in the `04` folder, and the script for the second part is `main.py`.
The script can be run using:
```bash
make 4
```
Make sure you add your GitHub token in the `main.py` file before running the script, and if you wish to test out repositories other than the one I used, you can change the `REPO` variable in the Makefile.

If you wish to run all the tasks at once, you can use the following command:
```bash
make all
```
