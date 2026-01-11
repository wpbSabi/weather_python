import folium
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def view_station_date_ranges(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    """
    Returns a data frame that shows the min and max date for each
        station in the data.

    Args:
        df (data frame) - raw weather data
        metric (string) - choose a metric in the weather data: TMAX, TMIN, etc.

    Returns:
        return_df (data frame) - filtered data frame that meets the criteria

    """

    # Filter out stations that do not have non-null data for the metric
    df = df[~df[metric].isnull()]

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


def ideal_temp(
    df: pd.DataFrame, tmin_or_tmax: str, ideal_min_limit: int, ideal_max_limit: int
) -> pd.DataFrame:
    """
    If we defined ideal weather as days where the high temperature is between X and Y degrees,
        then how many days per year of this ideal high temperature happen per location?

    Displays the number of days per year where the maximum temperature is between ideal_min and ideal_max.

    Args:
        df (DataFrame): DataFrame containing temperature data with columns for TMAX or TMIN at different locations.
        ideal_min_limit (int): Minimum temperature for ideal weather.
        ideal_max_limit (int): Maximum temperature for ideal weather.
    Returns:
        DataFrame: A DataFrame with the number of ideal weather days per year for both locations
        and the difference in counts.
    """
    ideal_weather1 = df[
        (df[tmin_or_tmax] >= ideal_min_limit) & (df[tmin_or_tmax] <= ideal_max_limit)
    ]
    ideal_weather2 = ideal_weather1.groupby(["NAME", "year"], as_index=False).agg(
        {"DATE": "count"}
    )
    ideal_weather2 = ideal_weather2.rename(columns={"DATE": "ideal_days"})
    ideal_weather_avg = (
        ideal_weather2.groupby("NAME")
        .agg({"ideal_days": "mean"})
        .sort_values("ideal_days", ascending=False)
    )

    # Prepare data for seaborn barplot
    p = plt.figure(figsize=(10, 6))
    p = sns.barplot(data=ideal_weather2, x="year", y="ideal_days", hue="NAME")
    p = plt.xlabel("Year")
    p = plt.ylabel(
        "Number of Days per Year (%i°F to %i°F)" % (ideal_min_limit, ideal_max_limit)
    )
    p = plt.title(
        "\nNumber of Great Weather Days (%s from %i°F to %i°F) \n"
        % (tmin_or_tmax, ideal_min_limit, ideal_max_limit)
    )
    p = plt.legend(loc="lower left")
    p = plt.tight_layout()
    p = plt.show()
    return p, ideal_weather_avg


def tmin_annual_plot(df: pd.DataFrame) -> pd.DataFrame:
    """
    Plots the minimum TMIN temperature per year per station

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
    p.axhspan(-20, -15, color="#9ecae1", alpha=0.15, label="Zone 5a (-20 to -15°F)")
    p.axhspan(-15, -10, color="#3182bd", alpha=0.15, label="Zone 5b (-15 to -10°F)")
    p.axhspan(-10, -5, color="#c2e699", alpha=0.15, label="Zone 6a (-10 to -5°F)")
    p.axhspan(-5, 0, color="#78c679", alpha=0.15, label="Zone 6b (-5 to 0°F)")
    p.axhspan(0, 5, color="#31a354", alpha=0.15, label="Zone 7a (0 to 5°F)")
    p.axhspan(5, 10, color="#006837", alpha=0.15, label="Zone 7b (5 to 10°F)")
    p.axhspan(10, 15, color="#fef0d9", alpha=0.15, label="Zone 8a (10 to 15°F)")
    p.axhspan(15, 20, color="#fdcc8a", alpha=0.15, label="Zone 8b (15 to 20°F)")
    p.axhspan(20, 25, color="#fc8d59", alpha=0.15, label="Zone 9a (20 to 25°F)")
    p.axhspan(25, 30, color="#e34a33", alpha=0.15, label="Zone 9b (25 to 30°F)")
    p.axhspan(30, 35, color="#b30000", alpha=0.15, label="Zone 10a (30 to 35°F)")

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


def non_ideal_temp_days(df, tmin_threshold, tmax_threshold):
    """
    Calculate the average annual number of non-ideal temperature days for each location.

    Args:
        df (pd.DataFrame): DataFrame with temperature data
        tmin_threshold (float): Maximum temperature threshold for too cold days
        tmax_threshold (float): Minimum temperature threshold for too hot days

    Returns:
        pd.DataFrame: DataFrame with average annual non-ideal temperature days for each location.
    """
    # too_cold
    too_cold = df[(df["TMIN"] <= tmin_threshold)]
    too_cold_yearly = too_cold.groupby(["NAME", "year"], as_index=False).agg(
        {"DATE": "count"}
    )
    too_cold_yearly_avg = too_cold_yearly.groupby(["NAME"], as_index=False).agg(
        {"DATE": "mean"}
    )
    too_cold_yearly_avg = too_cold_yearly_avg.rename(
        columns={"DATE": "avg_days_too_cold"}
    )

    # too_hot
    too_hot = df[df["TMAX"] >= tmax_threshold]
    too_hot_yearly = too_hot.groupby(["NAME", "year"], as_index=False).agg(
        {"DATE": "count"}
    )
    too_hot_yearly_avg = too_hot_yearly.groupby(["NAME"], as_index=False).agg(
        {"DATE": "mean"}
    )
    too_hot_yearly_avg = too_hot_yearly_avg.rename(columns={"DATE": "avg_days_too_hot"})

    too = too_cold_yearly_avg.merge(
        too_hot_yearly_avg,
        on=["NAME"],
        how="inner",
    )
    too["avg_days_too_cold"] = round(too["avg_days_too_cold"], 0).astype(int)
    too["avg_days_too_hot"] = round(too["avg_days_too_hot"], 0).astype(int)
    too["non_ideal_days"] = too["avg_days_too_cold"] + too["avg_days_too_hot"]

    return too.sort_values(by="non_ideal_days")
