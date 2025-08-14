import folium
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def update_data(
    new_data_path: str, existing_data_path: str, overwrite: str = "yes"
) -> pd.DataFrame:
    """
    1. Import new data
    2. Check the format of the data
    3. Append the data to existing data
    4. Remove duplicates
    5. Overwrite the existing data if overwrite = 'yes'

    Args:
        new_data_path (string) - used to read the CSV file in the path
        existing_data_path (string) - used to read the CSV file in the path
        overwrite (string) - the default option to overwrite can be disabled

    Returns:
        df (data frame) - updated data frame with the results
        Also overwrites the existing_data_path
    """
    # Import new data
    new = pd.read_csv(new_data_path)
    existing = pd.read_csv(existing_data_path)

    # Check that the columns match between the data frames
    assert (new.columns == existing.columns).all()

    # Append the data to existing data and remove duplicates
    combined = pd.concat([new, existing]).drop_duplicates()

    # Overwrite the existing data
    if overwrite == "yes":
        combined.to_csv(existing_data_path, index=False)

    return combined


def view_station_date_ranges(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a data frame that shows the min and max date for each
        station in the data.

    Args:
        df (data frame) - raw weather data

    Returns:
        return_df (data frame) - filtered data frame that meets the criteria

    """
    station_list = pd.DataFrame()
    for station in df.STATION.unique():
        a = df[df["STATION"] == station]
        a = a.assign(min_date=pd.to_datetime(min(a["DATE"])))
        a = a.assign(max_date=pd.to_datetime(max(a["DATE"])))
        station_list = pd.concat([station_list, a])
    return_df = (
        station_list[["STATION", "NAME", "min_date", "max_date"]]
        .drop_duplicates()
        .sort_values("STATION")
        .reset_index(drop=True)
    )
    return return_df


def map_stations(
    df: pd.DataFrame,
    default_lat: float = 45.9,
    default_long: float = -122.3,
    default_zoom: float = 9,
) -> folium.map:
    """
    Maps the stations on a folium map

    Args:
        df (data frame) - geospatial data by station, such as latitude
        default_lat (float) - the latitude that the map starts at
        default_long (float) - the longitude that the map starts at
        default_zoom (float) - the zoom that the map starts at

    Returns:
        m (folium.Map) - displays the results_df on a folium map
    """

    # Create the folium map and center on the default location
    m = folium.Map(
        [default_lat, default_long],
        zoom_start=default_zoom,
    )

    # Add darkgreen circles for destinations
    for j in range(len(df)):
        folium.CircleMarker(
            location=[df.iloc[j]["LATITUDE"], df.iloc[j]["LONGITUDE"]],
            tooltip=df.iloc[j][["STATION", "ELEVATION"]],
            color="darkblue",
            fill=True,
            fill_opacity=0.7,
            radius=8,
        ).add_to(m)

    folium.TileLayer("OpenTopoMap").add_to(m)
    folium.TileLayer("OpenStreetMap").add_to(m)
    folium.LayerControl().add_to(m)
    return m


def plot_temp_compare(df: pd.DataFrame, metric: str, year: int):
    """
    Plots of the temperature for two locations, on a lineplot, for a year

    Args:
        df (data frame) - weather data
        metric (string) - choose a metric in the weather data: TMAX, TMIN, or TAVG
        year (integer) - filter on a year

    Returns:
        p (figure) - plot of the temperature comparison for a year
    """
    # Stack the metric of the locations; make the wide data long
    x = pd.melt(
        df[df["year"] == year],
        id_vars="DATE",
        value_vars=list(df.columns[df.columns.str.contains(metric)]),
    )
    x["DATE"] = pd.to_datetime(x["DATE"])
    ax = sns.set(rc={"figure.figsize": (30, 20)})
    p = sns.lineplot(x, x="DATE", y="value", hue="variable", linewidth=4)
    ax = p.tick_params(axis="x", labelsize=20)
    ax = p.tick_params(axis="y", labelsize=20)
    ax = p.set_xlabel("\n Months \n", fontsize=20, rotation=0)
    ax = p.set_ylabel("\n Temparature (F) \n", fontsize=20, rotation=90)
    ax = p.set_title("\nTemperature Comparison %s\n" % year, fontsize=30)
    ax = plt.xticks(rotation=90)
    ax = plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax = plt.legend(fontsize=20)
    return p


def plot_monthly_temp_plots(
    df: pd.DataFrame, metric: str, ylim_low: int = -20, ylim_high: int = 120
):
    """
    Plots of the temperature for two locations, on a lineplot, for a year

    Args:
        df (data frame) - weather data
        metric (string) - choose a metric in the weather data: TMAX, TMIN, or TAVG
        ylim_low (integer) - the lowest range on the y-axis plot
        ylim_high (integer) - the higher range on the y-axis plot

    Returns:
        p (figure) - plot of the temperature comparison for a year
    """

    assert df.TMAX.min() > ylim_low
    assert df.TMAX.max() < ylim_high

    p = plt.figure(figsize=(15, 5))
    p = sns.boxenplot(data=df, x="month", y="TMAX", linewidth=1.5)
    p = plt.title("\nDaily %s Temperatures\n" % metric, fontsize=20)
    p = plt.xlabel(" ", fontsize=15)
    p = plt.xticks(
        ticks=np.arange(0, 12),
        fontsize=15,
        labels=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
    )
    p = plt.ylabel("\n%s Temperature (°F)\n" % metric, fontsize=15)
    p = plt.ylim(ylim_low, ylim_high)
    p = plt.show()
    return p


def ideal_tmax(
    df: pd.DataFrame, ideal_min_limit: int, ideal_max_limit: int
) -> pd.DataFrame:
    """
    If we defined ideal weather as days where the high temperature is between X and Y degrees,
        then how many days per year of this ideal high temperature happen per location?

    Displays the number of days per year where the maximum temperature is between ideal_min and ideal_max.

    Args:
        df (DataFrame): DataFrame containing temperature data with columns 'TMAX_PDX' and 'TMAX_CLATSKANIE'.
        ideal_min_limit (int): Minimum temperature for ideal weather.
        ideal_max_limit (int): Maximum temperature for ideal weather.
    Returns:
        DataFrame: A DataFrame with the number of ideal weather days per year for both locations
        and the difference in counts.
    """
    ideal_weather1 = df[
        (df["TMAX"] >= ideal_min_limit) & (df["TMAX"] <= ideal_max_limit)
    ]
    ideal_weather2 = ideal_weather1.groupby(["NAME", "year"], as_index=False).agg(
        {"DATE": "count"}
    )
    ideal_weather2 = ideal_weather2.rename(columns={"DATE": "ideal_days"})

    # Prepare data for seaborn barplot
    p = plt.figure(figsize=(10, 6))
    p = sns.barplot(data=ideal_weather2, x="year", y="ideal_days", hue="NAME")
    p = plt.xlabel("Year")
    p = plt.ylabel(
        "Number of Days per Year (%i°F to %i°F)" % (ideal_min_limit, ideal_max_limit)
    )
    p = plt.title(
        "\nNumber of Great Weather Days (Max Temp from %i°F to %i°F) \n"
        % (ideal_min_limit, ideal_max_limit)
    )
    p = plt.legend(loc="lower left")
    p = plt.tight_layout()
    p = plt.show()
    return p


def tmin_plot(df: pd.DataFrame) -> pd.DataFrame:
    """
    A USDA plant hardiness zone is defined by the minimum annual temperature at a station, averaged over the last 30 years.  For example, by this metric:
        * USDA Zone 8a falls within 10°F and 15°F
        * USDA Zone 8b falls within 15°F and 20°F
        * USDA Zone 9a falls within 20°F and 25°F

    Args:
        df (DataFrame): DataFrame containing TMIN temperature data
    Returns:
        p (plot): plot of TMIN for each station, over time
        tmin (DataFrame): data to use dor the USDA plant hardiness zones plot
    """
    # Pivot df to see the minimum temperature by year for each station
    tmin = df.pivot_table(
        index="year", columns="NAME", values="TMIN", aggfunc="min"
    ).reset_index()

    # Calculate the USDA hardiness zone for each station and year for all columns except the first (year)
    for col in tmin.columns[1:]:
        zone_col = f"{col.replace('TMIN_', '').replace('_', ' ')} Hardiness Zone"
        tmin[zone_col] = tmin[col].rolling(window=30, min_periods=30).mean()

    # Store the number of stations
    n = len(df["STATION"].unique())
    # Create a list of the column names for all_locations
    all_locations = list(tmin.columns[1 : n + 1])

    # Make the wide format long, for the seaborn lineplot
    tmin_long = tmin.reset_index().melt(
        id_vars="year", value_vars=all_locations, var_name="station", value_name="tmin"
    )

    # Create the plot
    sns.set_theme(style="whitegrid")
    # sns.set_theme(style="darkgrid")
    # plt.style.use('dark_background')
    p = plt.figure(figsize=(15, 5))
    p = sns.lineplot(
        data=tmin_long,
        x="year",
        y="tmin",
        hue="station",
        #  palette=['green', 'orange', 'blue'],
        marker="o",
        markersize=5,
        linewidth=2,
        style="station",
        dashes=False,
        #  legend='full',
    )
    p = plt.title("\nMinimum Temperature by Year and Station\n")
    p = plt.ylim(-30, 60)
    p = plt.xlabel("\nYear", fontsize=12, rotation=0)
    p = plt.ylabel("\nMinimum Temperature per Year (°F)\n", fontsize=12, rotation=90)
    p = plt.legend(loc="center left", bbox_to_anchor=(0, 0.9))
    # Suppress printouts
    p = plt.show()

    return p, tmin


def usda_plant_hardiness_zone(df: pd.DataFrame, legend_location: str) -> pd.DataFrame:
    """
    A USDA plant hardiness zone is defined by the minimum annual temperature at a station, averaged over the last 30 years.  For example, by this metric:
        * USDA Zone 8a falls within 10°F and 15°F
        * USDA Zone 8b falls within 15°F and 20°F
        * USDA Zone 9a falls within 20°F and 25°F

    Args:
        df (DataFrame): DataFrame containing TMIN temperature data
        legend_location (string): Allows input fto change where the legend is located
    Returns:
        p (plot): plot of USDA plant hardiness zones for each station, over time
    """
    # Count the number of stations
    n = int((len(df.columns) - 1) / 2)

    # Make the wide format long, for the seaborn lineplot
    usdahz = (
        df.reset_index()
        .melt(
            id_vars="year",
            value_vars=list(df.columns[n + 1 :]),
            var_name="station",
            value_name="USDA Hardiness Zone",
        )
        .dropna()
    )
    sns.set_theme(style="whitegrid")

    p = plt.figure(figsize=(15, 5))
    p = sns.lineplot(
        data=usdahz,
        x="year",
        y="USDA Hardiness Zone",
        hue="station",
        #  palette=['green', 'blue', 'orange'],
        marker="o",
        markersize=5,
        linewidth=2,
        style="station",
        dashes=False,
    )

    # Superimpose colored bands for USDA zones
    # https://colorbrewer2.org/#type=sequential&scheme=YlOrBr&n=3
    p.axhspan(-20, -15, color="purple", alpha=0.15, label="Zone 5a (-20 to -15°F)")
    p.axhspan(-15, -10, color="blue", alpha=0.15, label="Zone 5b (-15 to -10°F)")
    p.axhspan(-10, -5, color="#006400", alpha=0.15, label="Zone 6a (-10 to -5°F)")
    p.axhspan(-5, 0, color="green", alpha=0.15, label="Zone 6b (-5 to 0°F)")
    p.axhspan(0, 5, color="#8bc34a", alpha=0.15, label="Zone 7a (0 to 5°F)")
    p.axhspan(5, 10, color="#b7efb2", alpha=0.15, label="Zone 7b (5 to 10°F)")
    p.axhspan(10, 15, color="#fff7bc", alpha=0.15, label="Zone 8a (10 to 15°F)")
    p.axhspan(15, 20, color="#fec44f", alpha=0.15, label="Zone 8b (15 to 20°F)")
    p.axhspan(20, 25, color="#d95f0e", alpha=0.15, label="Zone 9a (20 to 25°F)")
    p.axhspan(25, 30, color="#d95f0e", alpha=0.15, label="Zone 9b (25 to 30°F)")
    p.axhspan(30, 35, color="orange", alpha=0.15, label="Zone 10a (30 to 35°F)")

    # Add zone labels
    year_label = 2024
    p.text(x=year_label, y=-17, s="5a", color="black", fontsize=14, va="center")
    p.text(x=year_label, y=-12, s="5b", color="black", fontsize=14, va="center")
    p.text(x=year_label, y=-7, s="6a", color="black", fontsize=14, va="center")
    p.text(x=year_label, y=-2, s="6b", color="black", fontsize=14, va="center")
    p.text(x=year_label, y=3, s="7a", color="black", fontsize=14, va="center")
    p.text(x=year_label, y=8, s="7b", color="black", fontsize=14, va="center")
    p.text(x=year_label, y=13, s="8a", color="black", fontsize=14, va="center")
    p.text(year_label, 18, "8b", color="black", fontsize=14, va="center")
    p.text(year_label, 23, "9a", color="black", fontsize=14, va="center")
    p.text(year_label, 28, "9b", color="black", fontsize=14, va="center")
    p.text(year_label, 33, "10a", color="black", fontsize=14, va="center")

    plt.title("\nUSDA Hardiness Zone by Year\n")
    plt.ylim(-20, 35)
    p.set_yticks(np.arange(-20, 36, 5))
    p.set_yticklabels(
        [
            "-20°F",
            "-15°F",
            "-10°F",
            "5°F",
            "0°F",
            "5°F",
            "10°F",
            "15°F",
            "20°F",
            "25°F",
            "30°F",
            "35°F",
        ]
    )
    p.set_xlabel("\nYear", fontsize=12, rotation=0)
    p.set_ylabel(
        "\n30-year-Average-Minimum Temperature (°F)\n", fontsize=12, rotation=90
    )
    plt.legend(list(df.columns[-n:]), loc=legend_location)
    return plt.show()
