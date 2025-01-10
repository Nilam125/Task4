import pulp
import pandas as pd

# Problem Statement: A company produces two products, Product A and Product B. 
# Each unit of Product A requires 3 hours of machine time and 1 hour of labor.
# Each unit of Product B requires 2 hours of machine time and 2 hours of labor.
# The company has 240 hours of machine time and 100 hours of labor available each week.
# Each unit of Product A yields a profit of $50, and each unit of Product B yields a profit of $40.
# Objective: Maximize the company's profit while staying within resource constraints.

# Define the Linear Programming problem



model = pulp.LpProblem(name="Maximize_Profit", sense=pulp.LpMaximize)

# Decision Variables
x1 = pulp.LpVariable(name="Product_A", lowBound=0, cat="Continuous")  # Number of units of Product A
x2 = pulp.LpVariable(name="Product_B", lowBound=0, cat="Continuous")  # Number of units of Product B

# Objective Function
model += 50 * x1 + 40 * x2, "Total_Profit"

# Constraints
model += 3 * x1 + 2 * x2 <= 240, "Machine_Time_Constraint"
model += 1 * x1 + 2 * x2 <= 100, "Labor_Time_Constraint"

# Solve the problem
status = model.solve()

# Extract results
results = {
    "Variable": [v.name for v in model.variables()],
    "Optimal_Value": [v.varValue for v in model.variables()],
}
results_df = pd.DataFrame(results)

# Save results to a text file
with open("result.txt", "w") as file:
    file.write("Optimization Results:\n")
    file.write(results_df.to_string(index=False))
    file.write("\n\nTotal Profit: " + str(pulp.value(model.objective)) + "\n\n")

    # Analysis/Insights
    insights = """
1. The optimal solution suggests producing {Product_A} units of Product A and {Product_B} units of Product B.
2. The maximum achievable profit is ${Profit}.
3. The machine time constraint and labor time constraint are binding at optimal levels, 
   meaning they are fully utilized in the optimal solution.
4. If more resources are available (e.g., additional machine or labor hours), the profit could increase further.
""".format(
        Product_A=results_df.loc[results_df['Variable'] == 'Product_A', 'Optimal_Value'].values[0],
        Product_B=results_df.loc[results_df['Variable'] == 'Product_B', 'Optimal_Value'].values[0],
        Profit=pulp.value(model.objective),
    )
    file.write(insights)

# Display insights
print("\nOptimization Results:")
print(results_df)
print("\nTotal Profit:", pulp.value(model.objective))
print(insights)
