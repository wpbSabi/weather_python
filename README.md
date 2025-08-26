# Weather Data Analyses with Python

    .
    ├── data                    # Data files are CSV since that ensures easy github reability; the data files are not large, so CSV are okay for this repository- and can be easily read on github
    ├── images                  # Images saved from the notebooks to use in this README
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
1. Gather data and save the data in the data folder
- For US postal codes, go to [NOAA](https://www.ncdc.noaa.gov/cdo-web/search)
- Read more about this data at [climate.gov](https://www.climate.gov/maps-data/dataset/past-weather-zip-code-data-table)
- Read my tutorial at [medium's Towards Data Science archive](https://towardsdatascience.com/democratizing-historical-weather-data-with-r-cc3c76dde7c5/)

2. Navigate to the `notebooks` folder for some prepared analyses
- Open `exploratory_data_analysis.ipynb` for some initial data exploration and wrangling.  For example, explore the date ranges of each weather station in the data and display the weather stations on a map.
- Compare temperature data`compare_temperature.ipynb`
- (WIP) Compare precipitation data `compare_rainfall_across_locations.ipynb`

## Highlights

### Temperature

#### Maximum Temperature

First let's look at the maximum temperatures between two locations for a year.
![TMAX_COMPARE](https://github.com/wpbSabi/weather_python/blob/main/images/tmax_compare.png)

And then, let's count the number of "Great Days" where the maximum temperature is in between my favorite range.  The range is a parameter so we can experiment with other ranges too.
![TMAX_GREAT_DAYS](https://github.com/wpbSabi/weather_python/blob/main/images/tmax_great_days.png)

#### Minimum Temperature

The USDA Plant Hardiness Zones are calculated using minimum annual temperatures over a 30 year period, averaged.  You may explore and download maps created with that data from 2023 at [planthardiness.ars.usda.gov/](https://planthardiness.ars.usda.gov/).

You may also download the shapefiles and create your own maps from [PRISM](https://prism.oregonstate.edu/), as long as you provide credit to Oregon State University and the USDA like this:
![usda_plant_hardiness_map](https://github.com/wpbSabi/weather_python/blob/main/images/usda_plant_hardiness_zones_map_with_highways.png)

The map is a good reference, but it is also helpful to see the yearly variation of minimum temperature for each year by location:
![TMIN](https://github.com/wpbSabi/weather_python/blob/main/images/tmin.png)

And then, we can calculate the hardiness zones over a rolling average of 30 years. PRISM updated their maps in 2023, and previously in 2012, but you may perform the most up-to-date calculations if you have the data:
![USDA_Zones](https://github.com/wpbSabi/weather_python/blob/main/images/usda_hardiness_zone.png)
