import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

PFASdata = pd.read_excel(r'C:\Users\natha\Documents\Coding\PFASDataReview\PFAS Project Lab Known Contamination Site Tracker - May 2023 for sharing with lat_long.xlsx', sheet_name='USA Contamination Sites', engine='openpyxl')
PFAS = pd.DataFrame(PFASdata)
print(PFAS.head())
print(PFAS.columns)
states_list = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", 
               "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois",
               "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
               "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
               "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
               "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
               "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
               "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]


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
State_Summary = State_Summary[State_Summary['State'].isin(states_list)]
#-------------------------------------------------------------#
#Remove all other locaitons besides States                    #
#-------------------------------------------------------------#
# Find missing states
missing_states = [state for state in states_list if state not in State_Summary['State'].tolist()]

# For each missing state, append a new row to the State_Summary dataframe
for state in missing_states:
    new_row = {'State': state, 'Number of Sights': 0, 'Concentration Range': 0}  # You can adjust the 'Concentration Range' value as necessary
    State_Summary = State_Summary.append(new_row, ignore_index=True)

print(State_Summary)

#--------------------------------------------------#
#           Graphing Section                       #
#--------------------------------------------------#
plt.figure(figsize=(12,8))  # This is to set the size of the chart
plt.bar(State_Summary['State'], State_Summary['Number of Sights'])
plt.xlabel('State')
plt.ylabel('Number of Sights')
plt.title('Number of Sights per State')
plt.xticks(rotation=90)  # This is to rotate the x-labels for better visibility
plt.tight_layout()  # This is to ensure all labels fit well in the plot
plt.show()
