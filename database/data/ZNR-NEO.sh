#!/bin/bash

# fetches standard format ZNR - NEO

python3 ../data-scraper/scraper.py ZNR ZNR.csv
python3 ../data-scraper/scraper.py KHM KHM.csv
python3 ../data-scraper/scraper.py STX STX.csv
python3 ../data-scraper/scraper.py STA STA.csv
python3 ../data-scraper/scraper.py AFR AFR.csv
python3 ../data-scraper/scraper.py MID MID.csv
python3 ../data-scraper/scraper.py VOW VOW.csv
python3 ../data-scraper/scraper.py NEO NEO.csv
