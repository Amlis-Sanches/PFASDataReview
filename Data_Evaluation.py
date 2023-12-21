# -------------------------------------imported packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import statsmodels.api as sm

# -------------------------------Import data and clean data
PFASdata = pd.read_excel(
    r"C:\Users\natha\Documents\Coding\PFASDataReview\PFAS Project Lab Known Contamination Site Tracker - May 2023 for sharing with lat_long.xlsx",
    sheet_name="USA Contamination Sites",
    engine="openpyxl",
)
PFAS = pd.DataFrame(PFASdata)
# print(PFAS.head())
print(PFAS.columns)
states_list = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
]


# Check if there are any nan
print(PFAS["PFAS Level (ppt)"].isnull().sum())
# Remove rows without PFAS data in PFAS levels
PFAS = PFAS.dropna(subset=["PFAS Level (ppt)"])

# -----------------------------Determine for each states  the total number of tests------#
# Here we find the top states with the most samples. This will allow us to determine     #
# similarities between the top measured states and with a stronger corolation. Even      #
# though some states have higher concentrations, the amount of samples that are taken    #
# are extreamly low. Comparing these states might not be valuble unless more infromation #
# is found.                                                                              #
# ---------------------------------------------------------------------------------------#

# Count the Total Number of Test for each state
number_of_Sites = PFAS["State"].value_counts()

# Compute the min and max concentrations for each state
concentration_range = PFAS.groupby("State")["PFAS Level (ppt)"].agg(["min", "max"])
concentration_range["range"] = concentration_range["max"] - concentration_range["min"]

# Combine the data
State_Summary = pd.DataFrame(
    {
        "State": number_of_Sites.index,
        "Total Number of Test": number_of_Sites.values,
        "Min Concentration (ppt)": concentration_range["min"].values,
        "Max Concentration (ppt)": concentration_range["max"].values,
        "Concentration Range (ppt)": concentration_range["range"].values,
    }
)
State_Summary.set_index("State", inplace=True)

# Calculate the average
State_Summary["Average Concentration"] = PFAS.groupby("State")[
    "PFAS Level (ppt)"
].mean()
State_Summary["Standard Deviation"] = PFAS.groupby("State")["PFAS Level (ppt)"].std()

# Determine the states that are the best for comparrison are:
# New Hampshire, Mishigan, California, Minnisota, Maine, Flordia, Vermont, Alaska, New York, North Carolina
# Although i want to confirm this with analysis to determine states that have the highest & lowest concentrations and highest count for measurment.


# -------------------------------------------------------------#
# Remove all other locaitons besides States                    #
# -------------------------------------------------------------#
State_Summary = State_Summary[State_Summary.index.isin(states_list)]

# Find missing states
missing_states = [
    state for state in states_list if state not in State_Summary.index.tolist()
]

# For each missing state, append a new row to the State_Summary dataframe
for state in missing_states:
    new_row = {
        "state": state,
        "Total Number of Test": 0,
        "Concentration Range": 0,
    }  # You can adjust the 'Concentration Range' value as necessary
    State_Summary = State_Summary.append(new_row, ignore_index=True)

# --------------------------------------------------#
# Reviewing the concentrations of nearby states to  #
# identify if there is a trend compaired to the     #
# the highest recorded state, new hampshire         #
# --------------------------------------------------#
# only use selected states
states_list = ["New Hampshire", "Maine", "Vermont", "Massachusetts"]
df_NH = State_Summary[State_Summary.index.isin(states_list)]
print(df_NH)


# --------------------------------------------------#
#           Graphing Section                       #
# --------------------------------------------------#
# Graping Functions:
def overlapped_bar(
    df, show=False, width=0.9, alpha=0.5, title="", xlabel="", ylabel="", **plot_kwargs
):
    xlabel = xlabel or df.index.name
    N = len(df)
    M = len(df.columns)
    indices = np.arange(N)
    colors = ["steelblue", "firebrick", "goldenrod", "gray"] * int(M / 5.0 + 1)
    for i, label, color in zip(range(M), df.columns, colors):
        kwargs = plot_kwargs
        kwargs.update({"color": color, "label": label})
        plt.bar(indices, df[label], width=width, alpha=alpha if i else 1, **kwargs)
        plt.xticks(indices + 0.5 * width, ["{}".format(idx) for idx in df.index.values])
    plt.legend()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.xticks(rotation=90)
    plt.ylabel(ylabel)
    if show:
        plt.show()
    return plt.gcf()


def graph_bar(X_Tick, Data, title="", xlabel="", ylabel=""):
    plt.figure(figsize=(12, 8))  # This is to set the size of the chart
    plt.bar(X_Tick, Data)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=90)  # This is to rotate the x-labels for better visibility
    plt.tight_layout()  # This is to ensure all labels fit well in the plot
    plt.show()


# graphing tested Sites
con = "Concentration (ppt)"
graph_bar(
    State_Summary.index,
    State_Summary["Total Number of Test"],
    "Number of Test Locations",
    "States",
    "Total Number of Test",
)

# Graph Lowest Concentration
graph_bar(
    State_Summary.index,
    State_Summary["Min Concentration (ppt)"],
    "Lowest Recorded Concentration of PFAS",
    "States",
    con,
)

# Removig Idiho to get a review of smaller concentrations
# ----------------------------------------------------------------------#
# df = df[df['Grad Intention'] != 'Undecided']                          #
# or                                                                    #
# df.drop(df[df['Grad Intention'] == 'Undecided'].index, inplace = True)#
# ----------------------------------------------------------------------#
df_min = State_Summary[State_Summary.index != "Idaho"]
graph_bar(
    df_min.index,
    df_min["Min Concentration (ppt)"],
    "Lowest Recorded Concentration of PFAS",
    "States",
    con,
)

# Graph Highest Concentration
graph_bar(
    State_Summary.index,
    State_Summary["Max Concentration (ppt)"],
    "Highest Recorded Concentration of PFAS",
    "States",
    con,
)

# Graph the average concentration
graph_bar(
    State_Summary.index,
    State_Summary["Average Concentration"],
    "Average Concentration of Each State",
    "State",
    con,
)

# Graph Concentration Comparison
overlapped_bar(
    State_Summary[["Min Concentration (ppt)", "Max Concentration (ppt)"]],
    show=True,
    title="Concentration of PFAS per State",
    xlabel="States",
    ylabel=con,
)

plt.figure(figsize=(12, 8))
plt.scatter(
    State_Summary["Total Number of Test"], State_Summary["Average Concentration"]
)
plt.xlabel("Total Number of Test")
plt.ylabel("Average Concentration(ppt)")
plt.title(
    "Graphic Visual for Comparison between Total Number of Test and Concentration"
)
plt.show()

# ------------------------------------------Statistics---------------------------------------------------#
# Performing an analysis to see if there is a corrolation between Total Number of Test and Average concentration
# using a Corelation because it's reviewing the states total number of samples and the PFAS concentration.


# --------------------------------------------------------------------------------------------------------#
# A correlation coefficient of -0.0964 suggests a very weak negative relationship between the number of
# samples taken in a state and the average PFAS level for each state. In this context, a negative
# correlation means that as one variable (number of samples) increases, the other variable (average PFAS
# level) tends to decrease slightly, and vice versa.

# However, the relationship is very weak, as the value is close to 0. In practical terms, there might be
# little to no real relationship between the two variables, or other factors might be influencing the
# relationship.

# If you were expecting a stronger relationship or a different direction (positive or negative), it's
# worthwhile to consider other variables or factors that could be influencing the PFAS levels, or it
# might be that the number of samples simply isn't strongly related to the average PFAS level in a state.

# Remember that correlation doesn't imply causation. Even if there was a stronger correlation, it wouldn't
# necessarily mean that the number of samples causes a change in PFAS levels.
# --------------------------------------------------------------------------------------------------------#

Corr_NOS_AC = State_Summary["Total Number of Test"].corr(
    State_Summary["Average Concentration"]
)
print("your corrolation coefficent is", Corr_NOS_AC)

X = State_Summary["Total Number of Test"]
y = State_Summary["Average Concentration"]
X = sm.add_constant(X)  # Adds a constant term to the predictor

model = sm.OLS(y, X)
results = model.fit()
print(results.summary())
# --------------------------------------------------------------------------------------------------------#
# R-squared: This value is 0.009, indicating that only 0.9% of the variability in the average PFAS
# concentration is explained by the Total Number of Test. An R2 this low suggests that the model does not fit
# your data well.
#
# Adjusted R-squared: This value is even slightly negative (-0.011). While R2 will always increase when a
# new predictor is added, the adjusted #R2 takes into account the number of predictors in the model and
# can decrease if a predictor doesn't improve the model's fit. A negative adjusted #R2 suggests that the
# model fits the data worse than a horizontal line.
#
# F-statistic and Prob (F-statistic): The F-statistic is 0.4505, and the associated p-value is 0.505. This
# means the model isn't significantly better at predicting the average PFAS concentration than a model
# with no predictors (just a mean). Generally, a p-value below 0.05 is considered statistically
# significant. In your case, it's well above that threshold.
#
# Coefficient for Number of Sights: The coefficient is -1874.3524, suggesting a negative relationship.
# However, the p-value for this coefficient is 0.505, which means it is not statistically significant.
# The 95% confidence interval for this coefficient spans from -7489.044 to 3740.339, which includes zero.
# This further emphasizes that there isn't strong evidence of a significant relationship.
#
# Omnibus, Skew, and Kurtosis: The Omnibus test p-value is 0.000, suggesting the residuals are not
# normally distributed. The high Skew and Kurtosis values further indicate that the model's assumptions
# are not being met.
# --------------------------------------------------------------------------------------------------------#

# -------------------------------------------Exporting data
State_Summary.to_csv("State_Summary.csv", index=True)
State_Summary.to_excel("State_Summary.xlsx", index=True)
