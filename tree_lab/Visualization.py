import pandas as pd
import matplotlib.pyplot as plot
import warnings
import polars.selectors as cs
import seaborn as sns
import polars as pl

# Ignore all warnings
warnings.filterwarnings("ignore")

data = pd.read_csv('../example/Tree_Data.csv')


# visualisation
def summarize(df, col, kind="Frequency and Relative frequency", dec=2):
    """
    Generates bar plots based on the specified kind.

    Parameters:
    - df (pd.DataFrame): The input dataframe.
    - kind (str): Specifies the type of bar plot to generate.
      It can take values "Species_vs_Status", "Species_vs_field", or "Light level vs status".

    Returns:
    None

    Raises:
    ValueError: If the provided 'kind' is not one of the specified options.

    Notes:
    - For "Species_vs_Status", the function generates a bar plot showing the count of alive and dead
    instances for each species.
    - For "Species_vs_field", the function creates a stacked bar chart representing the count of each
    species in different fields.
    - For "Light level vs status", a bar plot is generated to display the count of alive and dead
    instances for each light level category.

    The function utilizes seaborn and matplotlib for visualization, and the plots are displayed using
    the 'plot.show()' method.
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


def bar_plot(df, kind):
    """
    Generate different types of bar charts based on the specified kind parameter.

    Parameters:
    - df (pandas DataFrame): Input DataFrame containing relevant data.
    - kind (str): Type of bar chart to generate. Options: "Species_vs_Status", "Species_vs_field",
    "Light level vs status".

    Returns:
    The plots are displayed using the 'plot.show()' method.
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
    """ This function creates a scatter plot for the specified columns in the DataFrame """

    sns.set_theme(style="whitegrid")

    # Input validation
    if not pd.api.types.is_numeric_dtype(df[column_x]):
        raise ValueError(f"The column '{column_x}' must contain numerical data.")

    if not pd.api.types.is_numeric_dtype(df[column_y]):
        raise ValueError(f"The column '{column_y}' must contain numerical data.")

    # Create the scatter plot with hue and style based on the specified column
    plot.figure(figsize=(10, 6))
    sns.scatterplot(x=column_x, y=column_y, hue=hue_column, style=hue_column, data=df, palette="viridis", markers=True)

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

    def process_light_level_data(self):

        # Ensure 'Alive' column is present in the light_df DataFrame
        if 'Alive' not in light_df.columns:
            light_df['Alive'] = 0

        if 'Dead' not in light_df.columns:
            light_df['Dead'] = 1

        # Convert Polars DataFrame to Pandas DataFrame
        light_pandas_df = light_df.to_pandas()

        data_light_counts = light_pandas_df.melt(id_vars="Light_Cat",
                                                 value_vars=["Alive"],
                                                 var_name="Status",
                                                 value_name="Count")

        # Display the processed dataset
        display(data_light_counts)

        return data_light_counts

        # Display the processed dataset
        display(data_light_counts)

        return data_light_counts