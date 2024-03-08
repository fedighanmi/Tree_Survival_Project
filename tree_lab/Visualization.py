import pandas as pd
import matplotlib.pyplot as plot
import warnings
import polars.selectors as cs
import seaborn as sns
import polars as pl
from tree_lab import importing as imp

# Ignore all warnings
warnings.filterwarnings("ignore")

data = imp.import_data()


# visualisation
def summarize(df, col, kind="Frequency and Relative frequency", dec=2):
    """
    Summarizes the columns selected from the dataframe by showing the
    frequency and/or relative frequency of the categories

    Parameter:
        - df: a pandas dataframe
        - col: the columns of the dataframe that the user wants to summarize
        - kind: a string specifying if the frequency and/or the relative
          frequencies should be displayed. The default is "Frequency and
          Relative frequency", but it is also possible to choose "Frequency", or
          "Relative frequency"

    Returns the frequency tables for the selected columns
    """

    # Create frequency tables for each specified column
    frequency_tables = {}
    for column_name in col:

        value_counts = df[column_name].value_counts()
        percentages = ((value_counts / len(df)) * 100).round(dec)

        if kind == "Frequency":
            frequency_table_df = pd.DataFrame({'Frequency': value_counts})
            frequency_table_df.reset_index(inplace=True)
            frequency_table_df.columns = [column_name, 'Frequency']
        elif kind == "Relative frequency":
            frequency_table_df = pd.DataFrame(
                {'Relative frequency': percentages})
            frequency_table_df.reset_index(inplace=True)
            frequency_table_df.columns = [column_name, 'Relative frequency']
        elif kind == "Frequency and Relative frequency":
            frequency_table_df = pd.DataFrame(
                {'Frequency': value_counts, 'Relative frequency': percentages})
            frequency_table_df.reset_index(inplace=True)
            frequency_table_df.columns = [column_name, 'Frequency',
                                          'Relative frequency']
        else:
            frequency_table_df = None
            print("Something went wrong!")

        frequency_tables[column_name] = frequency_table_df

    # Display the frequency tables
    for column_name, frequency_table_df in frequency_tables.items():
        print(f"\nSummary for {column_name}:\n")
        print(frequency_table_df)


def compute_stats(dataframe, selected_columns):
    """
    Computes mean, standard deviation, minimum, maximum and median for the
    specified columns

    Parameters:
        - dataframe: the dataframe
        - selected_columns: list containing the columns for which we wish
          to have the statistics

    Returns:
         a dataframe containing the statistics of the columns specified in input
    """
    valid_columns = ['Light_ISF', 'AMF', 'EMF', 'Phenolics', 'Lignin', 'NSC']

    for column in selected_columns:
        if column not in valid_columns:
            print(f"Error: '{column}' is not one of the specified columns.")
            return

    results = pd.DataFrame({
        'Mean': dataframe[selected_columns].mean(),
        'Standard Deviation': dataframe[selected_columns].std(),
        'Minimum': dataframe[selected_columns].min(),
        'Maximum': dataframe[selected_columns].max(),
        'Median': dataframe[selected_columns].median()
    })

    return results


def bar_plot(df, kind):
    """
    Generate different types of bar charts based on the specified kind parameter.

    Parameters:
    - df (pandas DataFrame): Input DataFrame containing relevant data.
    - kind (str): Type of bar chart to generate. Options: "Species_vs_Status",
    "Species_vs_field", "Light level vs status".

    Returns:
        The plots are displayed using the 'plot.show()' method.

    Notes:
    - For "Species_vs_Status", the function generates a bar plot showing
    the count of alive and dead instances for each species.
    - For "Species_vs_field", the function creates a stacked bar chart
    representing the count of each species in different fields.
    - For "Light level vs status", a bar plot is generated to display
    the count of alive and dead instances for each light level category.

    The function utilizes seaborn and matplotlib for visualization
    """

    if kind == "Species_vs_Status":

        df_subset = df[['Species', 'Alive', 'Dead']]
        by_species_df = df_subset.groupby('Species').sum()

        # Create and add a new column containing the species names
        new_column_data = ["Acer saccharum", "Prunus serotina", "Quercus alba",
                           "Quercus rubra"]
        by_species_df.insert(0, 'Species', new_column_data)

        species_df = pl.DataFrame(by_species_df)

        data_counts = species_df.melt(id_vars="Species",
                                      value_vars=cs.numeric(),
                                      variable_name="Status",
                                      value_name="Count")

        sns.set_theme(style="whitegrid")

        data_counts2 = pd.DataFrame(data_counts,
                                    columns=["Species", "Status", "Count"])
        # Plotting the bar chart
        g = sns.catplot(
            data=data_counts2, kind="bar",
            x="Species", y="Count", hue="Status",
            errorbar="sd", palette="dark", alpha=.6, height=6
        )
        g.despine(left=True)
        g.set_axis_labels("Species", "Count")
        plot.subplots_adjust(top=0.9)  # leave space for the title
        g.fig.suptitle("Bar Chart: Species vs Status")

        for p in g.ax.patches:
            g.ax.annotate(f'{p.get_height():.0f}',
                          (p.get_x() + p.get_width() / 2., p.get_height()),
                          ha='center', va='center', xytext=(0, 10),
                          textcoords='offset points')
        plot.show()

    elif kind == "Species_vs_field":

        df_subset = df[['Species', 'Plot']]
        contingency_table = pd.crosstab(df_subset['Plot'], df_subset['Species'])

        df_final = pd.DataFrame(contingency_table)

        # Plotting the bar chart
        ax = df_final.plot(kind='bar', stacked=True, figsize=(10, 6))
        ax.set_xlabel('Field')
        ax.set_ylabel('Count')
        ax.set_title('Count of Species for Each Field')
        plot.legend(title='Species', bbox_to_anchor=(1.05, 1), loc='upper left')
        plot.tight_layout()  # Adjust layout to make space for the legend
        plot.show()

    elif kind == "Light level vs status":

        df_sublight = df[['Light_Cat', 'Alive', 'Dead']]
        by_light_df = df_sublight.groupby('Light_Cat').sum()

        light_cat = ["High", "Low", "Med"]
        by_light_df.insert(0, 'Light_Cat', light_cat)

        light_df = pl.DataFrame(by_light_df)

        data_light_counts = light_df.melt(id_vars="Light_Cat",
                                          value_vars=cs.numeric(),
                                          variable_name="Status",
                                          value_name="Count")

        # plot
        sns.set_theme(style="whitegrid")

        data_light_counts2 = pd.DataFrame(data_light_counts,
                                          columns=["Light_Cat", "Status",
                                                   "Count"])
        g = sns.catplot(
            data=data_light_counts2, kind="bar",
            x="Light_Cat", y="Count", hue="Status",
            errorbar="sd", palette="pink", alpha=.6, height=6
        )
        g.despine(left=True)
        g.set_axis_labels("Light level", "Count")
        plot.subplots_adjust(top=0.9)  # leave space for the title
        g.fig.suptitle("Bar Chart: light level vs status")

        for p in g.ax.patches:
            g.ax.annotate(f'{p.get_height():.0f}',
                          (p.get_x() + p.get_width() / 2., p.get_height()),
                          ha='center', va='center', xytext=(0, 10),
                          textcoords='offset points')

        plot.show()


def scatter_plot(df, column_x, column_y, hue_column, title):
    """
    This function creates a scatter plot for the specified columns in the DataFrame

    Parameters:
        - df: a dataframe
        - column_x: a string specifying the name of a numerical variable of df
        - column_y: a string specifying the name of a numerical variable of df
        - hue_column: allows to assign a categorical variable to the data points
          and represent it using different colours
        - title: a string specifying the title of the plot


    Returns:
        The plots are displayed using the 'plot.show()' method.
        """


    sns.set_theme(style="whitegrid")

    # Input validation
    if not pd.api.types.is_numeric_dtype(df[column_x]):
        raise ValueError(f"The column '{column_x}' must contain numerical data.")

    if not pd.api.types.is_numeric_dtype(df[column_y]):
        raise ValueError(f"The column '{column_y}' must contain numerical data.")

    # Create the scatter plot with hue and style based on the specified column
    plot.figure(figsize=(10, 6))
    sns.scatterplot(x=column_x, y=column_y, hue=hue_column, style=hue_column,
                    data=df, palette="viridis", markers=True)

    # Set labels and title
    plot.xlabel(column_x)
    plot.ylabel(column_y)
    plot.title(title)

    # Add legend
    plot.legend(title=hue_column, bbox_to_anchor=(1.05, 1), loc='upper left')

    # Adjust layout to make space for the legend
    plot.tight_layout()

    # Show the plot
    plot.show()

