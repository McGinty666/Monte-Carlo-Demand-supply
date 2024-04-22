Created on Mon Apr 22 09:02:50 2024

Created on Mon Apr 22 09:02:50 2024

@author: RMCGINT
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

# Specify the path to your Excel file
file_path = r"C:\Users\RMCGINT\OneDrive - Wessex Water\Python\InterviewTask_v1.xlsx"

# Read the sheets into dataframes
demand_benefit_df = pd.read_excel(file_path, sheet_name="demand_benefit_sheet")
demand_cost_df = pd.read_excel(file_path, sheet_name="demand_cost_sheet")
supply_option_df = pd.read_excel(file_path, sheet_name="supply_option_sheet")
base_balance_df = pd.read_excel(file_path, sheet_name="base_balance_sheet")


# Define the vectors for base balance
years = base_balance_df["year"]
base_balance_ML = base_balance_df["Supply-Demand Balance (Ml/d)"]


# Define the variables for each demand strategy benefit

demand_op_1_ben = demand_benefit_df["Demand Strategy 1"]
demand_op_2_ben = demand_benefit_df["Demand Strategy 2"]
demand_op_3_ben = demand_benefit_df["Demand Strategy 3"]
demand_op_4_ben = demand_benefit_df["Demand Strategy 4"]
demand_op_5_ben = demand_benefit_df["Demand Strategy 5"]


# Define the vectors for each demand option cost
demand_op_1_cost = demand_cost_df["Demand Strategy 1"]
demand_op_2_cost = demand_cost_df["Demand Strategy 2"]
demand_op_3_cost = demand_cost_df["Demand Strategy 3"]
demand_op_4_cost = demand_cost_df["Demand Strategy 4"]
demand_op_5_cost = demand_cost_df["Demand Strategy 5"]


# Define supply_option
supply_option = supply_option_df['Option']
# Define supply_option_benefit
supply_option_benefit = supply_option_df['Benefit (Ml/d)']
# Define supply_option_lead_time
supply_option_lead_time = supply_option_df['Lead time time (years)']
# Define supply_option_CAPEX
supply_option_CAPEX = supply_option_df['Total expenditure prior to option being in use (£m)']
# Define supply_option_OPEX
supply_option_OPEX = supply_option_df['Total expenditure in each year the option is in use (£m)']


# Create a vector of random integers from 1 to 12 (without replacement)
random_numbers = np.random.choice(range(1, 13), size=len(supply_option), replace=False)

# Select the supply option based on the random number
selected_indices = random_numbers - 1  # Convert to 0-based indices

# Create vectors for selected supply option variables
selected_supply_option = supply_option[selected_indices]
selected_benefit = supply_option_benefit[selected_indices]
selected_supply_lead_time = supply_option_lead_time[selected_indices]
selected_supply_option_CAPEX = supply_option_CAPEX[selected_indices]
selected_supply_option_OPEX = supply_option_OPEX[selected_indices]

'''
# Print the selected values (just for checking etc)
print(f"Selected supply option: {selected_supply_option}")
print(f"Benefit: {selected_benefit}")
print(f"Lead time: {selected_supply_lead_time}" )
print(f"CAPEX: {selected_supply_option_CAPEX}" )
print(f"OPEX: {selected_supply_option_OPEX}" )
'''

supply_benefit_vector = np.zeros(55)
# Randomly select one of the demand options vectors
selected_demand_vector = random.choice([demand_op_1_ben, demand_op_2_ben, demand_op_3_ben, demand_op_4_ben, demand_op_5_ben])


# Determine the selected demand option
if selected_demand_vector is demand_op_1_ben:
    selected_demand_option = "Demand Option 1"
elif selected_demand_vector is demand_op_2_ben:
    selected_demand_option = "Demand Option 2"
elif selected_demand_vector is demand_op_3_ben:
    selected_demand_option = "Demand Option 3"
elif selected_demand_vector is demand_op_4_ben:
    selected_demand_option = "Demand Option 4"
elif selected_demand_vector is demand_op_5_ben:
    selected_demand_option = "Demand Option 5"

print(f"Selected demand option: {selected_demand_option} chosen")

if selected_demand_vector is demand_op_1_ben:
    selected_demand_cost = demand_op_1_cost
elif selected_demand_vector is demand_op_2_ben:
    selected_demand_cost = demand_op_2_cost
elif selected_demand_vector is demand_op_3_ben:
    selected_demand_cost = demand_op_3_cost
elif selected_demand_vector is demand_op_4_ben:
    selected_demand_cost = demand_op_4_cost
elif selected_demand_vector is demand_op_5_ben:
    selected_demand_cost = demand_op_5_cost

# Initialize selected_benefit using the first entry in the vector
selected_benefit_supply_first = supply_option_benefit[0]
selected_benefit_interim_matrix = np.zeros(len(years))

# Add the selected demand vector, supply benefit vector to base_balance_ML to calculate the overall benefit
overall_benefit = base_balance_ML + selected_demand_vector 

original_n = 0
n = original_n #number of supply options to be selected from th vector
max_n = original_n #will get updated

yearly_OPEX = np.zeros(len(years))

for i in range(len(years)):
    # Check if overall_benefit is negative
    while overall_benefit[i] < 0:
        n += 1
        sum_of_first_n_benefit = sum(selected_benefit[:n])
        overall_benefit[i] += sum_of_first_n_benefit
        # Update max_n if necessary
        max_n = max(max_n, n)  # Keep track of the maximum n achieved
        yearly_OPEX[i] = sum(selected_supply_option_OPEX[:n])

    # Revert n to its original value if overall_benefit becomes positive
    if overall_benefit[i] > 0:
        n = original_n

# Print the maximum value of n achieved
print(f"Maximum value of n achieved (number of supply options chosen): {max_n}")

print("Supply Options selected:")
print(selected_supply_option[:max_n])


# Create the plot
plt.figure(figsize=(8, 6))
plt.plot(years, overall_benefit, marker='o', linestyle='-', color='b')
plt.title("Overall Benefit vs. Year")
plt.xlabel("Year")
plt.ylabel("Overall Benefit")
plt.grid(True)
plt.show()  


# Calculate total option cost by adding demand option cost and supply option cost
total_option_cost_by_year = selected_demand_cost + yearly_OPEX

plt.plot(years, total_option_cost_by_year, marker='o', label='Total Option Cost')
plt.xlabel('Years')
plt.ylabel('Total Option Cost')
plt.title('Total Option Cost by Year')
plt.grid(True)
plt.legend()
plt.show()


CAPEX = sum(selected_supply_option_CAPEX[:max_n])
total_option_cost_cum = np.cumsum(total_option_cost_by_year) + CAPEX

print ('total CAPEX='+ str(CAPEX))

# Create a simple line plot
plt.figure(figsize=(10, 6))
plt.plot(years, total_option_cost_cum, marker='o', linestyle='-', color='b')
plt.title("Cumulative Total Option Cost vs. Years")
plt.xlabel("Years")
plt.ylabel("Cumulative Total Option Cost")
plt.grid(True)
plt.show()

