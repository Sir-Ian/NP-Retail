import pandas as pd

REQUIRED_COLUMNS = ['latitude', 'longitude']


def validate_columns(df, required=None):
    """Ensure required columns are present."""
    required = required or REQUIRED_COLUMNS
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}")


def drop_invalid_coordinates(df, lat_col='latitude', lon_col='longitude'):
    """Remove rows with non-numeric or missing coordinates."""
    df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
    df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')
    return df.dropna(subset=[lat_col, lon_col])
