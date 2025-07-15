import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

# Load data from CSV
data = pd.read_csv(sys.argv[1])  # Replace with your CSV file path

# Set Seaborn style (optional, improves aesthetics)
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.2)  # Good for publications

# Create scatter plot with log scale
plt.figure(figsize=(8, 6))  # Adjust figure size if needed
scatter = sns.scatterplot(
    data=data,
    x="freq", #"x_column",  # Replace with your x-axis column name
    y="abundance", # "y_column",  # Replace with your y-axis column name
    alpha=0.7,     # Transparency for better visibility of overlapping points
    edgecolor="none",  # Removes point borders
    s=15,          # Adjust point size
)

# Set logarithmic scale on both axes
plt.xscale("log")
plt.yscale("log")

# Add labels and title (customize as needed)
plt.xlabel("X-axis label (log scale)", fontsize=12)
plt.ylabel("Y-axis label (log scale)", fontsize=12)
plt.title("Scatter Plot (Log-Log Scale)", fontsize=14)

# Improve tick labels for log scale
plt.minorticks_off()  # Optional: Cleans up minor ticks if too cluttered

# Save as high-quality PDF (vector format for publications)
plt.savefig("scatter_plot_log_log.pdf", dpi=300, bbox_inches="tight")

# Show the plot
plt.show()