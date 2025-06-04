import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
iceland_df = pd.read_csv('/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Volcano/volcano_Iceland.csv')
hawaii_df = pd.read_csv('/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Volcano/volcano_Hawaii.csv')
indonesia_df = pd.read_csv('/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Volcano/volcano_Indonesia.csv')
italy_df = pd.read_csv('/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Volcano/volcano_Italy.csv')


# Dictionary to hold dataframes and their country names
volcano_data = {
    'Iceland': iceland_df,
    'Hawaii': hawaii_df,
    'Indonesia': indonesia_df,
    'Italy': italy_df
}

# Create and save individual pie charts
for country, df in volcano_data.items():
    type_counts = df['Type'].dropna().value_counts()

    plt.figure(figsize=(7, 7))
    plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title(f'Volcano Type Distribution in {country}', fontsize=16, fontweight='bold', pad=20)
    plt.axis('equal')

    # Save the figure as a PNG file
    filename = f'volcano_types_{country.lower()}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    
    plt.show()
