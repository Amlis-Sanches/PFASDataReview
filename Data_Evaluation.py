import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

PFASdata = pd.read_excel(r'C:\Users\natha\Documents\Coding\PFASDataReview\PFAS Project Lab Known Contamination Site Tracker - May 2023 for sharing with lat_long.xlsx', sheet_name='USA Contamination Sites', engine='openpyxl')
PFAS = pd.DataFrame(PFASdata)
#print(PFAS.head())
print(PFAS.columns)
states_list = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", 
               "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois",
               "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
               "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
               "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
               "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
               "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
               "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]


#Check if there are any nan
print(PFAS['PFAS Level (ppt)'].isnull().sum())
#Remove rows without PFAS data
PFAS = PFAS.dropna(subset=['PFAS Level (ppt)'])


# Count the number of Sights for each state
number_of_Sights = PFAS['State'].value_counts()

# Compute the min and max concentrations for each state
concentration_range = PFAS.groupby('State')['PFAS Level (ppt)'].agg(['min', 'max'])
concentration_range['range'] = concentration_range['max'] - concentration_range['min']

# Combine the data
State_Summary = pd.DataFrame({
    'State': number_of_Sights.index,
    'Number of Sights': number_of_Sights.values,
    'Min Concentration (ppt)': concentration_range['min'].values,
    'Max Concentration (ppt)': concentration_range['max'].values,
    'Concentration Range (ppt)': concentration_range['range'].values
})
State_Summary.set_index('State', inplace=True)

#Calculate the average
State_Summary['Average Concentration'] = PFAS.groupby('State')['PFAS Level (ppt)'].mean()
State_Summary['Standard Deviation'] = PFAS.groupby('State')['PFAS Level (ppt)'].std()

#-------------------------------------------------------------#
#Remove all other locaitons besides States                    #
#-------------------------------------------------------------#
State_Summary = State_Summary[State_Summary.index.isin(states_list)]

# Find missing states
missing_states = [state for state in states_list if state not in State_Summary.index.tolist()]

# For each missing state, append a new row to the State_Summary dataframe
for state in missing_states:
    new_row = {'state': state, 'Number of Sights': 0, 'Concentration Range': 0}  # You can adjust the 'Concentration Range' value as necessary
    State_Summary = State_Summary.append(new_row, ignore_index=True)

#--------------------------------------------------#
#Reviewing the concentrations of nearby states to  #
#identify if there is a trend compaired to the     #
#the highest recorded state, new hampshire         #
#--------------------------------------------------#
#only use selected states
states_list = ['New Hampshire', 'Maine', 'Vermont', 'Massachusetts']
df_NH = State_Summary[State_Summary.index.isin(states_list)]
print(df_NH)

#--------------------------------------------------#
#           Graphing Section                       #
#--------------------------------------------------#
#Graping Functions: 
def overlapped_bar(df, show=False, width=0.9, alpha=.5,title='', xlabel='', ylabel='', **plot_kwargs):
    xlabel = xlabel or df.index.name
    N = len(df)
    M = len(df.columns)
    indices = np.arange(N)
    colors = ['steelblue', 'firebrick', 'goldenrod', 'gray'] * int(M / 5. + 1)
    for i, label, color in zip(range(M), df.columns, colors):
        kwargs = plot_kwargs
        kwargs.update({'color': color, 'label': label})
        plt.bar(indices, df[label], width=width, alpha=alpha if i else 1, **kwargs)
        plt.xticks(indices + .5 * width,['{}'.format(idx) for idx in df.index.values])
    plt.legend()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.xticks(rotation=90)
    plt.ylabel(ylabel)
    if show:
        plt.show()
    return plt.gcf()

def graph_bar(X_Tick, Data, title='', xlabel ='', ylabel =''):
    plt.figure(figsize=(12,8))  # This is to set the size of the chart
    plt.bar(X_Tick, Data)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=90)  # This is to rotate the x-labels for better visibility
    plt.tight_layout()  # This is to ensure all labels fit well in the plot
    plt.show()

# graphing tested sights
con = 'Concentration (ppt)'
graph_bar(State_Summary.index, State_Summary['Number of Sights'], 'Number of Test Locations', 'States', 'Number of Sights')

#Graph Lowest Concentration
graph_bar(State_Summary.index, State_Summary['Min Concentration (ppt)'], 'Lowest Recorded Concentration of PFAS', 'States', con)

#Removig Idiho to get a review of smaller concentrations
#----------------------------------------------------------------------#
#df = df[df['Grad Intention'] != 'Undecided']                          #
#or                                                                    #
#df.drop(df[df['Grad Intention'] == 'Undecided'].index, inplace = True)#
#----------------------------------------------------------------------#
df_min = State_Summary[State_Summary.index != 'Idaho']
graph_bar(df_min.index, df_min['Min Concentration (ppt)'], 'Lowest Recorded Concentration of PFAS', 'States', con)

#Graph Highest Concentration
graph_bar(State_Summary.index, State_Summary['Max Concentration (ppt)'], 'Highest Recorded Concentration of PFAS', 'States', con)

#Graph the average concentration
graph_bar(State_Summary.index, State_Summary['Average Concentration'], 'Average Concentration of Each State', 'State', con)

#Graph Concentration Comparison
overlapped_bar(State_Summary[['Min Concentration (ppt)','Max Concentration (ppt)']], show=True,title='Concentration of PFAS per State', xlabel='States', ylabel=con)

