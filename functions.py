import pandas as pd

def update_data(new_data_path: str, 
                existing_data_path: str,
                overwrite: str='yes') -> pd.DataFrame:
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
    if overwrite=='yes':
        combined.to_csv(existing, index=False)

    return combined