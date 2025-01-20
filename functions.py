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
        combined.to_csv(existing, index=False)

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
