import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# file_name = 'result_merge'  # result_merge, 
file_name = 'merged_result_Hard_stats_16_states=1318_acts=1269_20240118 000116' 

df = pd.read_csv(file_name+'.csv')
epoch_num = 15
y_fontsize = 18 #14
fontsize = 28 #18
fig, ax = plt.subplots(figsize=(15,10))
x = range(epoch_num)
y = np.arange(0, 500, 100)
label = ['Hard','Medium','Easy']
marker = ['o','s','^','+', 'x', ]
color = ['blue','orange','green']  # green,red orange
plot_y_index = [5,5,5]
for i in range(len(df.columns)):
    plt.plot(x, df.iloc[:epoch_num,i], label=label[i],
             marker=marker[i],markersize=10,color=color[i], linewidth=2.8)
    for j,(m, n) in enumerate(zip(x[:plot_y_index[i]], df.iloc[:plot_y_index[i],i])):
        if i==0 and j==0:
            ax.annotate(f'{n:.1f}', xy=(m+0.7, n-10), textcoords="offset points", xytext=(0, 10), ha='center',
                        fontsize=y_fontsize)
        elif i==0 and j==1:
            ax.annotate(f'{n:.1f}', xy=(m+0.6, n), textcoords="offset points", xytext=(0, 10), ha='center',
                        fontsize=y_fontsize)
        elif i==0 and j==2:
            ax.annotate(f'{n:.1f}', xy=(m+0.05, n), textcoords="offset points", xytext=(0, 10), ha='center',
                        fontsize=y_fontsize)
        elif i==0 and j==2:
            ax.annotate(f'{n:.1f}', xy=(m+0.3, n), textcoords="offset points", xytext=(0, 10), ha='center',
                        fontsize=y_fontsize)
        else:
            ax.annotate(f'{n:.1f}', xy=(m, n), textcoords="offset points", xytext=(0,10), ha='center',
                        fontsize=y_fontsize)

ax.tick_params(axis='both', which='major', labelsize=fontsize)
plt.xlabel('Maximum Recursion Depth during Compaction',fontsize=fontsize, labelpad=15)
plt.ylabel('Condition Node Ticks',fontsize=fontsize, labelpad=15)
plt.legend(loc=(0.7, 0.7),fontsize=fontsize)
plt.grid()
plt.savefig('Merge Result.png', bbox_inches='tight',dpi=300)
    
