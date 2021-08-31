"""
Khoa Tran
CSE 163 AB

This program implements the functions from geopandas,
pandas, and matplotlib to create a dataset that is a
combination of two files and create the geometry of
every census tract in Washington and ouputs information
for food access for Washington's censys tracts. Plots the
census tracts in multiple ways especially with colorings to
display various information
"""
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt


def load_in_data(file1, file2):
    """
    From the given two file inputs,
    returns GeoDataFrame that merges
    both datasets of the file, keeping
    all census tracts in datset with geometry,
    and disregarding the rest.
    """
    df1 = gpd.read_file(file1)
    df2 = pd.read_csv(file2)
    result = df1.merge(df2, left_on='CTIDFP00',
                       right_on='CensusTract', how='left')
    return result


def percentage_food_data(data):
    """
    From the given dataset, returns the
    percentage of census tracts that
    corresponds with the food access data.
    """
    df = data['CensusTract']
    total = df.notnull().sum()
    length = len(df)
    temp = total/length
    percent = temp * 100
    return percent


def plot_map(data):
    """
    From given dataset, outputs a plot
    of Washington with all census tracts.
    Save output in washington_map.png.
    """
    data.plot()
    plt.savefig('washington_map.png')


def plot_population_map(data):
    """
    From given dataset, outputs a map of
    Washington with censys tracts that is colored
    by population.
    Save plot output to washington_population_map.png.
    """
    df = data.dropna()
    df.plot(legend=True, column='POP2010')
    plt.savefig('washington_population_map.png')


def plot_population_county_map(data):
    """
    From given dataset, outputs a map of
    Washington with each county having a color to
    indicate their population.
    Save plot output to washington_county_population_map.png.
    """
    df = data.dropna()
    df = df[['POP2010', 'County', 'geometry']]
    df = df.dissolve(by='County', aggfunc='sum')
    df.plot(column='POP2010', legend=True)
    plt.savefig('washington_county_population_map.png')


def plot_food_access_by_county(data):
    """
    From given dataset, creates four different plots
    that each map Washington state and the counties it has,
    coloring the counties by various different values of
    food access chance as well as combining
    with different income levels.
    Save plot output to washington_county_food_access.png.
    """
    df = data.dropna()
    df = df[['County', 'geometry', 'POP2010', 'lapophalf',
             'lapop10', 'lalowihalf', 'lalowi10']]
    df = df.dissolve(by='County', aggfunc='sum')
    df['lapophalf_ratio'] = df['lapophalf'] / df['POP2010']
    df['lalowihalf_ratio'] = df['lalowihalf'] / df['POP2010']
    df['lapop10_ratio'] = df['lapop10'] / df['POP2010']
    df['lalowi10_ratio'] = df['lalowi10'] / df['POP2010']
    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, figsize=(20, 10), ncols=2)
    df.plot(ax=ax1, legend=True, vmin=0, vmax=1, column='lapophalf_ratio')
    df.plot(ax=ax2, legend=True, vmin=0, vmax=1, column='lalowihalf_ratio')
    df.plot(ax=ax3, legend=True, vmin=0, vmax=1, column='lapop10_ratio')
    df.plot(ax=ax4, legend=True, vmin=0, vmax=1, column='lalowi10_ratio')
    ax1.set_title('Low Access: Half')
    ax2.set_title('Low Access + Low Income: Half')
    ax3.set_title('Low Access: 10')
    ax4.set_title('Low Access + Low Income: 10')
    fig.savefig('washington_county_food_access.png')


def plot_low_access_tracts(data):
    """
    From given dataset, creates a plot with multiple layers
    that indicate food and census data. The combination of the
    layers maps the state of Washington, coloring census tracts
    to indicate the low access to food supplies.
    Save plot output to washington_low_access.png.
    """
    fig, ax1 = plt.subplots(1)
    data.plot(color='#EEEEEE', ax=ax1)
    df = data.dropna()
    df.plot(color='#AAAAAA', ax=ax1)
    data['lapop10_ratio'] = data['lapop10'] / data['POP2010']
    data['lapophalf_ratio'] = data['lapophalf'] / data['POP2010']
    data['Low_Access_Urban'] = ((data['Urban'] == 1) &
                                ((data['lapophalf_ratio'] >= 0.33)
                                | (data['lapophalf'] >= 500)))
    data['Low_Access_Rural'] = ((data['Rural'] == 1) &
                                ((data['lapop10_ratio'] >= 0.33)
                                | (data['lapop10'] >= 500)))
    data = data[(data['Low_Access_Urban'])
                | (data['Low_Access_Rural'])]
    data.plot(ax=ax1)
    fig.savefig('washington_low_access.png')


def main():
    """
    Load data and runs all functions with the data
    """
    data = load_in_data('/course/food-access/tl_2010_53_tract00/\
tl_2010_53_tract00.shp', '/course/food-access/food-access.csv')
    percentage_food_data(data)
    plot_map(data)
    plot_population_map(data)
    plot_population_county_map(data)
    plot_food_access_by_county(data)
    plot_low_access_tracts(data)


if __name__ == '__main__':
    main()
