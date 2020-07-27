# Hackathon csv
During the first week of [osoc](https://osoc.be/), there is a small hackathon. This repo was one of the results of this hackathon.
The goal of this repo was to analyze the infomation from a csv file. Most of this code is later used in the `shmdoc-analyzer-service`.

The analysis result gets stored in a `report.json`.

## Running
### Install requirements
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
### Running
The input file is specified at line `121`. Since this was only for the hackathon, there was only a hardcoded version of the input file.
Once this file is specified to a csv file you want to analyse, you can run with the folowing code:
```bash
python3 main.py
```