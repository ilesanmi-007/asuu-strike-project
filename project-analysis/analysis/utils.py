# utils.py

# This file exists to store all necessary functions that will be used across the project.
# Create and test your function in the relevant notebook
# Copy and paste the function here for future use.
# Import utils in any notebook to use these functions

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway, kruskal, ttest_ind, anderson
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd


# Data cleaning and preprocessing functions
def remove_duplicates(df):
    """Remove duplicate rows from a DataFrame."""
    return df.drop_duplicates()


def fill_missing_values(df, value):
    """Fill missing values in a DataFrame with a given value."""
    return df.fillna(value)


def convert_to_numeric(df, columns):
    """Convert specified columns in a DataFrame to numeric data type."""
    df[columns] = df[columns].apply(pd.to_numeric, errors="coerce")
    return df


def convert_to_categorical(df, columns):
    """Convert specified columns in a DataFrame to categorical data type."""
    df[columns] = df[columns].astype("category")
    return df


# Data visualization functions
def plot_histogram(data, title, xlabel, ylabel):
    """Plot a histogram for the given data."""
    plt.hist(data, bins=10, alpha=0.7, color="skyblue", edgecolor="black")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()


def plot_scatter(data, x, y, title, xlabel, ylabel):
    """Plot a scatter plot for the given data."""
    plt.scatter(data[x], data[y], alpha=0.5, color="orange")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()


def plot_heatmap(data, x_var, y_var, count_var, colour_map):
    """
    Plots a heatmap for two categorical variables, specifically using the count.
    x_var : x-axis variable
    y_var : y-axis variable
    count_var : any other column to perform a count on

    """

    # prepare the data for use
    df = data[[x_var, y_var, count_var]]

    # performing a groupby on the data
    data_count = df.groupby([x_var, y_var]).count()

    # Pivot the data
    data_pivot = data_count.pivot_table(values=count_var, index=y_var, columns=x_var)

    # fill any null value with zero
    data_pivot = data_pivot.fillna(value=0)

    # plot heatmap
    sns.heatmap(data_pivot, cmap=colour_map, annot=True)


# Other utility functions
def save_plot(fig, filename):
    """Save a matplotlib figure to a file."""
    fig.savefig(filename, bbox_inches="tight")

def display_dataframe(df, max_rows=10):
    """Display the first few rows of a DataFrame."""
    display(df.head(max_rows))


def plot_heatmap_new(data, x_var, y_var, target_feature, colour_map = 'magma_r',title = ''):
    '''
    Update to plot_heatmap

    Plots a heatmap for two categorical variables, specifically using the count and mean of a target column. 
    This helps check how to variables relate with respect to a third (numerical variable).

    data: Dataframe containing the data
    x_var : x-axis variable
    y_var : y-axis variable
    target_feature : any other column to perform a count and get the mean.
    
    '''

    #prepare the data for use
    df = data[[x_var, y_var, target_feature]]
    
    # performing a groupby on the data to get the number of occurrences and the average of the target feature by the other features
    data_count = df.groupby([x_var, y_var]).count()
    data_avg = df.groupby([x_var, y_var]).mean()

    #Pivot the count data and fill any null value with zero
    count_pivot = data_count.pivot_table(values = target_feature , index = y_var, columns = x_var)
    count_pivot = count_pivot.fillna(value = 0)

    #Pivot the average data and fill any null value with zero
    avg_pivot = data_avg.pivot_table(values = target_feature , index = y_var, columns = x_var)
    avg_pivot = avg_pivot.fillna(value = 0)

    # Define a custom order for the x and y axes
    x_order = ['Poorly', 'Moderately', 'Very']
    y_order = ['Very', 'Moderately','Poorly' ]

    # Rearrange the pivot tables based on the custom order of columns and index labels
    count_pivot = count_pivot.reindex(columns=x_order, index=y_order)    
    avg_pivot = avg_pivot.reindex(columns=x_order, index=y_order)

     #create axes to plot
    fig, axes = plt.subplots(1, 2, figsize = (15, 5))


    #plot count data and avg data heatmaps
    sns.heatmap(count_pivot,cmap = colour_map, annot = True, ax = axes[0])
    axes[0].set_title('Occurrences')
    sns.heatmap(avg_pivot,cmap = colour_map, annot = True, ax = axes[1])
    axes[1].set_title(f'Average {target_feature}')
    
    #Setting a major title for both plots
    fig.suptitle(f'Overview prep_before vs prep_after {title}', fontsize=16)
    plt.subplots_adjust(wspace=0.8)


def count_and_average(group, avg_col, dataframe):
    '''
    Plots a count and average plot n the same ax
    group: The column to count, group by and get a reference average for.
    avg_col: The column to get the mean for
    ///
    Example: ...
    '''
    
    #getting the average
    avg_course = dataframe.groupby(group).mean().reset_index()

    #Plotting the count and average plots
    plt.figure(figsize = (25, 12))
    ax = sns.countplot(data = dataframe, x=group, label = f'Count of {group} by {group}', color = 'blue')
    ax2 = ax.twinx()
    sns.lineplot(x=group, y= avg_col,data = avg_course, ax=ax2, color='r', label = f'Average {avg_col} by {group}')
    ax2.set_ylabel(f'average {avg_col}')
    ax2.set_ylim(0, max(avg_course[avg_col]))

    #setting the labels
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper right')


# Add more functions as needed for your specific project

# Example usage of utility functions
if __name__ == "__main__":
    # Example usage of functions
    data = pd.DataFrame({"A": [1, 2, 3, np.nan, 5], "B": [10, 20, np.nan, 40, 50]})
    print("Original DataFrame:")
    print(data)

    cleaned_data = remove_duplicates(data)
    print("\nDataFrame after removing duplicates:")
    print(cleaned_data)

    filled_data = fill_missing_values(data, value=0)
    print("\nDataFrame after filling missing values:")
    print(filled_data)


def anova_assumptions_test(feature, target, df):
    '''
    This function tests the assumptions required for the ANOVA statistical test.

    feature: The feature being tested for ANOVA assumptions.
    target: The column to aggregate for ANOVA.
    df: The dataframe containing the data.

    Returns one of four strings:
    1. The given data passes both tests of homoscedasticity and normality.
    2. The given data passes the test of homoscedasticity but fails the test of normality.
    3. The given data passes the test of normality but fails the test of homoscedasticity.
    4. The given data fails both tests of homoscedasticity and normality.
    '''
    # Homoscedasticity
    feature_std = df.groupby(feature)[target].std()
    max_std = feature_std.max()
    min_std = feature_std.min()

    # Normality
    normality = anderson_darling(df=df, feature=feature, target=target)

    if min_std * 2 >= max_std and normality:
        return 'The given data passes both tests of homoscedasticity and normality.'
    elif min_std * 2 >= max_std and not normality:
        return 'The given data passes the test of homoscedasticity but fails the test of normality.'
    elif min_std * 2 < max_std and normality:
        return 'The given data passes the test of normality but fails the test of homoscedasticity.'
    else:
        return 'The given data fails both tests of homoscedasticity and normality.'


def anderson_darling(df,feature,alpha,target):
  '''
  This function tests for normality in the df.
  
  df: The dataframe that contains the df you want to test.
  feature: The feature being tested for normality.
  target: The column to aggregate.
  alpha: The significance level for the statistical test. Default 0.05 or 5%.                                                   
  alpha should be inserted as a percentage in integer form, eg, 5% should be inserted as 5.
  
  Returns: True or False
  True means that the data follows a normal distribution.
  False means that the data doesn't follows a normal distribution.
  '''
  unique = df[feature].unique().to_list()
  counter = []

  for unique_value in unique:
    test_data = df[df[feature]==unique_value][target]
    
    if len(test_data) < 5:
        pass
    
    else:
        result = anderson(test_data)
        test_statistic = result.statistic
        critical_values = list(result.critical_values)
        significance_level = list(result.significance_level)
        index_sig_level = significance_level.index(alpha)

        if test_statistic <= critical_values[index_sig_level]:
            # It follows a normal distribution.
            counter.append(True)
        
        else:
            # It does not follow a normal distribution
            pass
    
  if False in counter:
      return False
  else:
      return True
  

def perform_one_way_anova(df, feature, target):
    '''
    Perform a one-way ANOVA test to assess the equality of means among multiple groups.
    
    Parameters:
        df (DataFrame): The DataFrame containing the data.
        feature (str): The column name for the categorical levels.
        target (str): The column name for the continuous variable (CGPA change).

    Returns:
        result (F_onewayResult): The result of the one-way ANOVA test.
    '''
    unique_levels = df[feature].unique()
    levels_data = {level: df[df[feature] == level][target] for level in unique_levels}
    
    result = f_oneway(*levels_data.values())
    
    return (f'ANOVA F-statistic:", {result.statistic}, "ANOVA p-value:", {result.pvalue}')


def perform_pairwise_tukeyhsd(df, feature, target):
    '''
    Perform pairwise Tukey's Honestly Significant Difference (HSD) test to compare group means.

    Parameters:
        df (DataFrame): The DataFrame containing the data.
        feature (str): The column name for the categorical groups.
        target (str): The column name for the data to be compared.

    Returns:
        tukey_result (MultiComparison): The result of the pairwise Tukey's HSD test.
    '''
    tukey_result = pairwise_tukeyhsd(
        endog=df[target],
        groups=df[feature]
    )
    print(tukey_result)
    
    
def perform_kruskal_willis_test(df, feature, target, min_count=5):
    '''
    Perform the Kruskal-Wallis test after filtering out groups with low counts.

    Parameters:
        df (DataFrame): The DataFrame containing the data.
        feature (str): The column name for the categorical groups.
        target (str): The column name for the data to be compared.
        min_count (int): Minimum count required for each group. Groups with counts below this are dropped.

    Returns:
        kruskal_result (KruskalResult): The result of the Kruskal-Wallis test.
    '''
    group_counts = df[feature].value_counts()
    low_count_groups = group_counts.index[group_counts < min_count]
    filtered_df = df[~df[feature].isin(low_count_groups)]

    groups_data = {group: filtered_df[filtered_df[feature] == group][target] for group in filtered_df[feature].unique()}

    kruskal_result = kruskal(*groups_data.values())
    return (f"Kruskal-Wallis Test statistic:, {kruskal_result.statistic}, Kruskal-Wallis Test p-value:, {kruskal_result.pvalue}")

