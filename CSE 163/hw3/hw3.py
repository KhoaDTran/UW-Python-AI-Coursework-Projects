import cse163_utils  # noqa: F401
# This is a hacky workaround to an unfortunate bug on macs that causes an
# issue with seaborn, the graphing library we want you to use on this
# assignment.  You can just ignore the above line or delete it if you are
# not using a mac!
"""
Khoa Tran
CSE 163 AB

This program performs data analytics using various libraries
to show dataset comparision of education level compared to
other variables of race and sex. This program filters out
data to get the desired relationship for plotting. Lastly,
the program implements a ML model to train and test its accuracy
with the mean_squared_error.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
sns.set()


def compare_bachelors_1980(df):
    """
    From the given DataFrame, returns a
    new DataFrame that compares the percentage of men
    and women that has a minimum degree of a bachelor's
    degree in 1980
    """
    degree = df['Min degree'] == "bachelor's"
    year = df['Year'] == 1980
    sex = (df['Sex'] == 'M') | (df['Sex'] == 'F')
    new_df = df[degree & year & sex]
    result = new_df.loc[:, ['Sex', 'Total']]
    return result


def top_2_2000s(df):
    """
    From the given DataFrame, returns a Series
    of the two most commonly awarded levels of
    educational attainment given between
    2000 and 2010(inclusive)
    """
    sex = df['Sex'] == 'A'
    year = (df['Year'] >= 2000) & (df['Year'] <= 2010)
    new_df = df[year & sex]
    new_df = new_df.groupby('Min degree')['Total'].mean()
    result = new_df.nlargest(2)
    return result


def percent_change_bachelors_2000s(df, sex='A'):
    """
    From given DataFrame and sex, returns the difference
    in total percentage of bachelor's degree from 2010 to 2000

    Special Case: if not given sex, sex is defaulted as 'A' (all)
    """
    df_2000 = df[(df['Year'] == 2000) &
                 (df['Min degree'] == "bachelor's") &
                 (df['Sex'] == sex)]
    df_2010 = df[(df['Year'] == 2010) &
                 (df['Min degree'] == "bachelor's") &
                 (df['Sex'] == sex)]
    df_2000 = df_2000.loc[:, ['Total']].squeeze()
    df_2010 = df_2010.loc[:, ['Total']].squeeze()
    return df_2010 - df_2000


def line_plot_bachelors(df):
    """
    From the given DataFrame, outputs a line plot of the
    total percentage with a bachelor's degree throughout
    the years of the data. Save plot in a file named
    'line_plot_bachelors.png'
    """
    new_df = df[(df['Min degree'] == "bachelor's") & (df['Sex'] == 'A')]
    sns.relplot(data=new_df, kind='line', x='Year', y='Total')
    plt.ylabel('Percentage')
    plt.title("Percentage Earning Bachelor's over Time")
    plt.savefig('line_plot_bachelors.png', bbox_inches='tight')


def bar_chart_high_school(df):
    """
    From the given DataFrame, outputs a bar chart of the
    percentage of everyone compared with men and female
    that has a minimum degree of high school in 2009.
    Save bar chart in file named 'bar_chart_high_school.png'
    """
    new_df = df[(df['Min degree'] == 'high school') & (df['Year'] == 2009)]
    new_df = new_df.loc[:, ['Sex', 'Total']]
    sns.catplot(x='Sex', y='Total', data=new_df, kind='bar')
    plt.ylabel('Percentage')
    plt.title('Percentage Completed High School by Sex')
    plt.savefig('bar_chart_high_school.png', bbox_inches='tight')


def plot_hispanic_min_degree(df):
    """
    From the given DataFrame, outputs a line plot showing
    the change in percentage of Hispanic with a minimum degree
    of high school compared to bachelor's degree between
    the years of 1990 and 2010(inclusive). Save the line plot
    in a file named 'plot_hispanic_min_degree.png'
    """
    sex = df['Sex'] == 'A'
    degree = (df['Min degree'] == 'high school') |\
             (df['Min degree'] == "bachelor's")
    year = (df['Year'] >= 1990) & (df['Year'] <= 2010)
    new_df = df[sex & degree & year]
    sns.relplot(x='Year', y='Hispanic', data=new_df,
                kind='line', hue='Min degree', style='Min degree')
    plt.ylabel('Percentage of Hispanic')
    plt.title("Percentage of Hispanics with\
 Bachelor's degree vs. High School degrees")
    plt.savefig('plot_hispanic_min_degree.png', bbox_inches='tight')


def fit_and_predict_degrees(df):
    """
    From the given DataFrame, trains a regression
    decision tree in order to predict the percentage of
    individuals of the specified sex to achieve that degree
    type for a specific year. After prediction, returns the
    mean squared error of the test dataset to test the
    accuracy of the prediction
    """
    new_df = df.loc[:, ['Year', 'Min degree', 'Sex', 'Total']]
    new_df = new_df.dropna()
    features = new_df.loc[:, new_df.columns != 'Total']
    features = pd.get_dummies(features)
    labels = new_df['Total']
    features_train, features_test, labels_train, labels_test = \
        train_test_split(features, labels, test_size=0.2)
    model = DecisionTreeRegressor()
    model.fit(features_train, labels_train)
    test_prediction = model.predict(features_test)
    result = mean_squared_error(labels_test, test_prediction)
    return result


def main():
    """
    Implement written functions
    with given file
    """
    data = pd.read_csv('/home/hw3-nces-ed-attainment.csv', na_values='---')
    compare_bachelors_1980(data)
    top_2_2000s(data)
    percent_change_bachelors_2000s(data, 'A')
    line_plot_bachelors(data)
    bar_chart_high_school(data)
    plot_hispanic_min_degree(data)
    fit_and_predict_degrees(data)


if __name__ == '__main__':
    main()
