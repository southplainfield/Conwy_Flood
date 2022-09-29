##to tidyup planning data
import pandas as pd
from get_coordinates import get_coordinates
from get_reversed_address import reverse_address
import clean
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def main():
    # load in planning_data
    planning_data = pd.read_csv('<<FILE>>v')

    # clean
    #clean.drop_columns(planning_data, "View")

    # reversed postcode address
    #reversed_address = planning_data['Site Address'].apply(
    #    lambda x: pd.Series(reverse_address(x), index=['Reversed_address']))

    #planning_data = pd.concat([planning_data[:], reversed_address[:]], axis="columns")

    # get long and lat
    coordinates = planning_data['Site Address'].apply(lambda x: pd.Series(get_coordinates(x), index=['Latitude', 'Longitude']))
    planning_data = pd.concat([planning_data[:], coordinates[:]], axis="columns")

    # return to csv
    planning_data.to_csv(r"conwy_planning_data.csv", encoding="utf-8", header="true", index=False)

if __name__ == "__main__":
    main()
