import pandas as pd
import matplotlib.pyplot as plt
import sys

def create_pie_chart_from_csv(csv_file, category_column, value_column, 
                            title='Pie Chart', colors=None, 
                            output_file=None, dpi=300):
    """
    Creates a pie chart from data in a CSV file with custom colors and high-quality PDF output.
    
    Parameters:
    - csv_file: Path to the CSV file
    - category_column: Name of the column containing category labels
    - value_column: Name of the column containing numerical values
    - title: Chart title (default: 'Pie Chart')
    - colors: Optional list of colors for pie slices (hex, name, or RGB tuples)
    - output_file: Optional filename to save the chart (PDF recommended for quality)
    - dpi: Resolution in dots per inch (default: 300 for high quality)
    """
    
    # Read the CSV file
    try:
        data = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # Check if required columns exist
    if category_column not in data.columns or value_column not in data.columns:
        print(f"Error: Columns '{category_column}' or '{value_column}' not found in the CSV file.")
        print(f"Available columns: {list(data.columns)}")
        return
    
    def absolute_value(val):
        # Calculate absolute value from percentage
        a = round(val/100.*sum(data[value_column]))
        return f"{a}"

    # Create the pie chart with enhanced styling
    plt.figure(figsize=(20, 20))
    wedges, texts, autotexts = plt.pie(
        data[value_column], 
        labels=data[category_column], 
        autopct=absolute_value, # '%1.1f%%', 
        startangle=70,
        colors=data["Color"], #colors,
        textprops={'fontsize': 12},
        pctdistance=0.85,
        radius=1,
        counterclock=False,
        wedgeprops = {'linewidth': 0.5, 'linestyle': '-', 'edgecolor': 'white'}
    )
    
    # Improve label appearance
    plt.setp(autotexts, size=20, weight="bold")
    plt.setp(texts, size=12)
    
    # Add white circle in center to make it a donut chart (optional)
    #centre_circle = plt.Circle((0,0), 0.70, fc='white')
    #fig = plt.gcf()
    #fig.gca().add_artist(centre_circle)
    
    plt.title(title, fontsize=16, pad=25)
    plt.axis('equal')  # Ensure pie is drawn as a circle
    
    # Save or display the chart
    if output_file:
        if output_file.lower().endswith('.pdf'):
            plt.savefig(output_file, format='pdf', dpi=dpi, bbox_inches='tight')
            print(f"High-quality PDF saved to {output_file}")
        else:
            plt.savefig(output_file, dpi=dpi, bbox_inches='tight')
            print(f"Chart saved to {output_file} with {dpi} DPI")
    plt.show()

# Example usage with custom colors and PDF output:
if __name__ == "__main__":
    # Sample data path and column names
    csv_path =  sys.argv[1] # 'data.csv'
    category_col = 'Category'
    value_col = 'Value'
    
    # Custom color palette (can use hex codes, color names, or RGB tuples)
    custom_colors = [
        '#FF6B6B',  # Soft red
        '#4ECDC4',  # Teal
        '#45B7D1',  # Light blue
        '#FFA07A',  # Light salmon
        '#98D8C8'   # Mint
    ]
    
    create_pie_chart_from_csv(
        csv_path, 
        category_col, 
        value_col,
        title='Product Sales Distribution',
        colors=custom_colors,
        output_file='high_quality_pie.pdf',
        dpi=300
    )