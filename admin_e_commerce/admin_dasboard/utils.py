# admin_dasboard/utils.py
import pandas as pd
from bson import ObjectId

def convert_objectid_to_str(df):
    df = df.copy()
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].apply(lambda x: str(x) if isinstance(x, ObjectId) else x)
    return df
