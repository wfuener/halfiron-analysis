import json
import os
import csv
import sys
import pandas as pd
from ydata_profiling import ProfileReport

BASE_DIR = os.path.join(os.path.dirname(__file__))
INPUT_FILE = f"{BASE_DIR}/../other_datasets/half_ironman_results.csv"


def main():
    df = pd.read_csv(INPUT_FILE)
    df = remove_finishers(df)
    df = derived_columns(df)
    df = subdivide(df)
    df = drop_cols(df)
    profile(df)


def remove_finishers(df: pd.DataFrame):
    df = df.loc[df['Gender'] == 'F']
    return df


def derived_columns(df):
    df['Position'] = df.groupby(['EventLocation', 'EventYear'])['FinishTime'].rank()
    df['PositionPercentage'] = df.groupby(['EventLocation', 'EventYear'])['FinishTime'].rank(pct=True)
    df['PositionBinned'] = pd.cut(df['PositionPercentage'], [0, .01, .05, .10, .25, .50, 1.0],
                                  labels=["top_1", "top_5", "top_10", "10_25", "25_50", "bottom_50"])

    df['SwimPositionPercentage'] = df.groupby(['EventLocation', 'EventYear'])['SwimTime'].rank(pct=True)
    df['BikePositionPercentage'] = df.groupby(['EventLocation', 'EventYear'])['BikeTime'].rank(pct=True)
    df['RunPositionPercentage'] = df.groupby(['EventLocation', 'EventYear'])['RunTime'].rank(pct=True)

    return df


def subdivide(df: pd.DataFrame):
    # df = df.loc[df['AgeGroup'] == '30-34']
    df = df.loc[df['PositionBinned'] == '10_25']
    # df = df.loc[df['SwimTime'] <= 1800] # 30 minute swim or faster
    return df


# Gender,AgeGroup,AgeBand,Country,CountryISO2,EventYear,EventLocation,SwimTime,Transition1Time,BikeTime,Transition2Time,RunTime,FinishTime
def drop_cols(df: pd.DataFrame):
    df = df.drop(columns=['AgeGroup', 'AgeBand', 'Country', 'CountryISO2', 'EventYear', 'EventLocation'])
    return df


def profile(df: pd.DataFrame):
    profile = ProfileReport(df, title="Profiling Report")
    profile.to_file("halfiron_artifacts/profile.html")


if __name__ == '__main__':
    main()
