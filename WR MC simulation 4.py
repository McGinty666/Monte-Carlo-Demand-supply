import random
import pandas as pd

filepath = "E:\\Work\\Supply_demand_v1.xlsx"
# Load data from Excel sheets
sheet1_df = pd.read_excel(filepath, sheet_name="Sheet 1", header=0)
sheet2_df = pd.read_excel(filepath, sheet_name="Sheet 2", header=0)
sheet3_df = pd.read_excel(filepath, sheet_name="Sheet 3", header=0)
sheet4_df = pd.read_excel(filepath, sheet_name="Sheet 4", header=0)

# Define a function to calculate overall benefit and cost
def calculate_overall_benefit_and_cost(strategies, supply_options):
    # Randomly select values from Sheet1 for each strategy
    strategy_values = [random.choice(sheet1_df[strategy]) for strategy in strategies]

    
    # Calculate the sum of strategy values
    strategy_sum = sum(strategy_values)
    
    # Randomly select supply options and calculate their sum
    supply_sum = sheet3_df.loc[sheet3_df['Option'].isin(supply_options), 'Total expenditure in each year the option is in use (£m)'].sum()
    
    # Calculate balance from Sheet4
    balance = sheet4_df.loc[0, 'Supply-Demand Balance (Ml/d)']
    
    # Calculate overall benefit
    overall_benefit = strategy_sum + supply_sum + balance
    
    # Calculate cost based on selected strategy from Sheet1
    cost = sheet2_df.loc[0, strategies].sum()
    
    return overall_benefit, cost

# Perform Monte Carlo simulation
num_iterations = 100
min_cost = float('inf')
best_combination = None

for _ in range(num_iterations):
    # Randomly select strategies and supply options
    strategies = random.sample(list(sheet1_df.columns[1:]), random.randint(1, 5))
    supply_options = random.sample(sheet3_df['Option'].tolist(), random.randint(1, len(sheet3_df)))
    
    # Calculate overall benefit and cost
    overall_benefit, cost = calculate_overall_benefit_and_cost(strategies, supply_options)
    
    # Discard combinations with overall benefit less than 20
    if overall_benefit < 20:
        continue
    
    # Update minimum cost and best combination
    if cost < min_cost:
        min_cost = cost
        best_combination = (strategies, supply_options)

# Print the combination with the lowest cost
print("Combination with the lowest cost:", best_combination)