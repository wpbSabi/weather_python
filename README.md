# Weather Data Analyses with Python

    .
    ├── data                    # Data files are CSV since that ensures easy github reability; the data files are not large, so CSV are okay for this repository- and can be easily read on github
    ├── notebooks               # The analyses are conducted and results are shown in the notebooks 
    ├── LICENSE
    ├── README.md
    ├── functions.py            # The functions used in the notebook are stored in functions.py
    ├── poetry.lock             # poetry file for package version management
    └── pyproject.toml          # poetry file for package version management


## Repository Setup
- [poetry](https://python-poetry.org/) is used for package dependency management


## Background
Gardening is the inspiration for this repo.  I'm planning to move my garden more than an hour away, in a different micro climate, and I want to explore the differences.  Rather than ad hoc analyses, this time I'd like to build out standardized analyses that others could also reuse when importing data for different locations.

## How to run
1. Gather data
- For US postal codes, go to [NOAA](https://www.ncdc.noaa.gov/cdo-web/search)
- Read more about this data at [climate.gov](https://www.climate.gov/maps-data/dataset/past-weather-zip-code-data-table)
- Read my tutorial at [medium's Towards Data Science archive](https://towardsdatascience.com/democratizing-historical-weather-data-with-r-cc3c76dde7c5/)

2. Navigate to the `notebooks` folder and open `exploratory_data_analysis.ipynb`
- Append new data to existing locations' data file
- Explore the date ranges of each weather station in the data
- Explore the weather stations on a map

3. `compare_temperature.ipynb`
- Pick two locations to compare along the same date range
- Plot maximum temperature 
- Plot minimum temperatur

4. `compare_rainfall_across_locations.ipynb`
- WIP

## Highlights

# Temperature

The USDA Plant Hardiness Zones are calculated using minimum annual temperatures over a 30 year period, averaged.  You may explore and download maps created with that data from 2023 at [planthardiness.ars.usda.gov/](https://planthardiness.ars.usda.gov/).  

Using temperature data in this github repository, we can also see changes over time.
![USDA_Zones](https://github.com/wpbSabi/weather_python/blob/main/images/usda_hardiness_zone_pdx_clatskanie.png)