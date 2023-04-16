import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# define dataframe
df = pd.read_csv('C:/Users/Keegan/OneDrive/Desktop/sample_data_sets/books_adj.csv',header=0)

# create plot variables
groupby_yr = df.groupby('year')['num_pages'].mean()
x = groupby_yr.index
y = groupby_yr.values

# create data point marker for subplot max
x0 = [1987.99]
y0 = [330]

# create data point marker for subplot min
x1 = [2014]
y1 = [209]

# create plot
fig = plt.figure(facecolor="#e1ddbf")
ax = fig.add_subplot(111)
ax.set_ylim(min(y) - 5, max(y)+ 21.1)
ax.set_xlim(min(x)+2, max(x))


plt.annotate('329 Pages', xy=(1987, 335), xytext=(1988.5, 330) )
plt.annotate('209 Pages', xy=(2009, 220), xytext=(2009, 208) )
plt.plot(x,y, color= '#009dc4', linewidth= 2 )
plt.yticks([200, 250, 300, 350])

# Plot data label points
plt.plot( x0, y0, marker= 'o', markerfacecolor= '#454545', markeredgecolor= 'black', markersize= 6 ) 
plt.plot( x1, y1, marker= 'o', markerfacecolor= '#454545', markeredgecolor= 'black', markersize= 6 )

# Plot avg constant 
plt.axhline( y=np.nanmean(y), color= '#5A5A5A', linestyle='--', linewidth= 1, label= "Avg")


# Plot labels
plt.xlabel('Year of Publication')
plt.title('Average Page Counts of Books', fontsize= 14, pad= 20)

plt.savefig("Page Counts over Time.png")

