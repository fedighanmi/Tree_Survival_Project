
import pandas as pd
import matplotlib.pyplot as plot
import warnings
import polars.selectors as cs
import seaborn as sns
import polars as pl

# Ignore all warnings
warnings.filterwarnings("ignore")

df = pd.read_csv('../example/Tree_Data.csv')

# visualisation
def bar_plot(df, type):
    """ This function gives barplots in output. The kind of barplot is choosen
      by the use through the input parameter type """

    if type == "Species_vs_Status":
        df.dropna(subset=['Event'], inplace=True)
        df = df.fillna(0)

        df['Alive'] = df['Alive'].replace('X', 1)

        df_subset = df[['Species', 'Alive', 'Event']]
        df_subset = df_subset.rename(columns = {'Event': 'Dead'})

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
        plt.subplots_adjust(top=0.9)  #leave space for the title
        g.fig.suptitle("Bar Chart: Species vs Status")

        for p in g.ax.patches:
            g.ax.annotate(f'{p.get_height():.0f}',
                          (p.get_x() + p.get_width() / 2., p.get_height()),
                          ha='center', va='center', xytext=(0, 10),
                          textcoords='offset points')
        plot.show()

    elif type == "Species_vs_field":

        df_subset = df[['Species', 'Plot']]
        contingency_table = pd.crosstab(df_subset['Plot'], df_subset['Species'])

        df_final = pd.DataFrame(contingency_table)

        # Plotting the bar chart
        ax = df_final.plot(kind='bar', stacked=True, figsize=(10, 6))
        ax.set_xlabel('Field')
        ax.set_ylabel('Count')
        ax.set_title('Count of Species for Each Field')
        plot.legend(title='Species', bbox_to_anchor=(1.05, 1), loc='upper left')
        plot.show()

    elif type == "Light level vs status":

        df.dropna(subset=['Event'], inplace=True)
        df = df.fillna(0)

        df['Alive'] = df['Alive'].replace('X', 1)

        df_sublight = df[['Light_Cat', 'Alive', 'Event']]
        df_sublight = df_sublight.rename(columns={'Event': 'Dead'})

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
        plt.subplots_adjust(top=0.9) # leave space for the title
        g.fig.suptitle("Bar Chart: light level vs status")

        for p in g.ax.patches:
            g.ax.annotate(f'{p.get_height():.0f}',
                          (p.get_x() + p.get_width() / 2., p.get_height()),
                          ha='center', va='center', xytext=(0, 10),
                          textcoords='offset points')
        plot.show()