
import pandas as pd
import matplotlib.pyplot as plot

df = pd.read_csv('../example/Tree_Data.csv')

# visualisation
def bar_plot(df, type):
    """ This function gives barplots in output. The kind of barplot is choosen
      by the use through the input parameter type """

    if type == 1:
        df.dropna(subset=['Event'], inplace=True)
        df = df.fillna(0)

        df['Alive'] = df['Alive'].replace('X', 1)
        df['Harvest'] = df['Harvest'].replace('X', 1)

        df_subset = df[['Species', 'Harvest', 'Alive', 'Event']]

        by_species_df = df_subset.groupby('Species').sum()

        fig = plot.figure(figsize=(7, 7))
        plot.bar(by_species_df.index, by_species_df['Event'], label='Died',
                 width=0.5, color='#826')
        plot.bar(by_species_df.index, by_species_df['Alive'],
                 bottom=by_species_df['Event'], label='Alive', width=0.5,
                 color='#182')

        plot.xlabel('Tree species', labelpad=5, size=10)
        plot.ylabel('Count', labelpad=5, size=10)
        plot.title('Bar Chart died/alive of Species')
        plot.legend(fontsize=13)
        plot.xticks(size=7)
        plot.show()

    elif type == 2:

        # for now it just works with this kind of data in input, I will fix it
        data = {
            'Species': ['Acer saccharum', 'Prunus serotina', 'Quercus alba',
                        'Quercus rubra'],
            '1': [41, 42, 38, 37],
            '2': [42, 42, 35, 26],
            '3': [42, 42, 41, 32],
            '4': [42, 42, 36, 30],
            '5': [42, 42, 37, 31],
            '6': [42, 41, 37, 36],
            '7': [42, 41, 39, 37],
            '8': [42, 42, 30, 29],
            '9': [42, 42, 38, 25],
            '10': [41, 41, 36, 42],
            '11': [42, 41, 42, 42],
            '12': [42, 40, 36, 41],
            '13': [41, 42, 36, 24],
            '14': [41, 42, 39, 33],
            '15': [42, 42, 37, 38],
            '16': [42, 42, 38, 29],
            '17': [42, 41, 36, 37],
            '18': [41, 42, 41, 41]
        }
        df = pd.DataFrame(data)
        df.set_index('Species', inplace=True)
        transposed_df = df.transpose()

        # Plotting the bar chart
        ax = transposed_df.plot(kind='bar', stacked=True, figsize=(10, 6))
        ax.set_xlabel('Field')
        ax.set_ylabel('Count')
        ax.set_title('Count of Species for Each Field')
        plot.legend(title='Species', bbox_to_anchor=(1.05, 1), loc='upper left')
        plot.show()