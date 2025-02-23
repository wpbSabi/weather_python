import folium
import pandas as pd


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


def map_stations(df: pd.DataFrame) -> folium.map:
    """
    Maps the stations on a folium map

    Args:
        df (data frame) - geospatial data by station, such as latitude

    Returns:
        m (folium.Map) - displays the results_df on a folium map
    """
    # Create the folium map and center on the default location
    m = folium.Map(
        [46.082, -123.187],
        zoom_start=11,
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
        year (integer) - filter on a year, for the

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
    return plt
