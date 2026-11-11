import os
import pandas as pd

# Directory where CSVs are located
csv_dir = './'
# List of CSV file names as you described
csv_files = [
    'bt_randon_o=100_cp=10_ap=10_MAE=0_time=20240506 115257.csv',
    'bt_randon_o=100_cp=10_ap=10_MAE=5_time=20240506 172702.csv',
    'bt_randon_o=100_cp=10_ap=50_MAE=0_time=20240506 115600.csv',
    'bt_randon_o=100_cp=30_ap=10_MAE=5_time=20240508 222143.csv',
    'bt_randon_o=100_cp=50_ap=10_MAE=5_time=20240508 222622.csv',
    'bt_randon_o=100_cp=50_ap=30_MAE=5_time=20240508 223352.csv',
    'bt_randon_o=100_cp=50_ap=50_MAE=5_time=20240508 224801.csv',
    'bt_randon_o=300_cp=50_ap=50_MAE=5_time=20240508 232751.csv',
    'bt_randon_o=500_cp=50_ap=50_MAE=0_time=20240506 124308.csv',
    'bt_randon_o=500_cp=50_ap=50_MAE=5_time=20240120 020115.csv'
]


# Prepare a list to accumulate the results
results = []
# Loop through all CSV files
for file in csv_files:
    # Extract the scenario details from the file name
    parts = file.split('_')
    scenario = {
        'Objects': int(parts[2].split('=')[1]),
        'Pc': int(parts[3].split('=')[1]),
        'Pa': int(parts[4].split('=')[1]),
        'MAE': int(parts[5].split('=')[1]),
        'Time': parts[6].split('=')[1] + '_' + parts[6].split('.')[0]
    }

    # Load CSV into DataFrame
    df = pd.read_csv(os.path.join(csv_dir, file))

    # Extract results for each algorithm
    obtea = df.iloc[0]
    baseline = df.iloc[1]

    # Collect relevant data in a single row
    result = {
        'Objects': scenario['Objects'],
        'Pc': scenario['Pc'],
        'Pa': scenario['Pa'],
        'MAE': scenario['MAE'],
        'Literals': round(obtea['literals_obj_count'], 1),
        'States Avg': round(obtea['state_avg'], 1),
        'Actions Avg': round(obtea['act_avg'], 1),
        'Baseline Cost Avg': round(baseline['cost_avg'], 1),
        'OBTEA Cost Avg': round(obtea['cost_avg'], 1),
        'Baseline Cond Tick Avg': round(baseline['cond_tick_avg'], 1),
        'OBTEA Cond Tick Avg': round(obtea['cond_tick_avg'], 1),
        'OBTEA WM Cond Tick Avg': round(obtea['wm_cond_tick_avg'], 1)
    }
    # Add this result to the list
    results.append(result)

# Convert the list of results into a DataFrame
final_results = pd.DataFrame(results)

# Sort the DataFrame
final_results.sort_values(by=['MAE', 'Objects', 'Pc', 'Pa'], inplace=True)

# Display the final results
# Output the entire DataFrame
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(final_results)
# 输出的表格，每行的内容是 Objects、Pc、Pa、MAE，csv中的 literals_obj_count、state_avg、act_avg，
# Baseline的cost_avg，OBTEA的cost_avg，Baseline的cond_tick_avg，OBTEA的cond_tick_avg，OBTEA的wm_cond_tick_avg