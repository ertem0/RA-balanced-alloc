import pickle
import matplotlib.pyplot as plt
from main import Data
import sys
# Load from the file
name = sys.argv[1] 
with open(name + '.pkl', 'rb') as file:
    data = pickle.load(file)

print(data)
m = data.m
n_values = data.n_values
mean_values = data.mean_values
variances =  data.variances
std_devs = data.std_devs

plt.figure(figsize=(10, 6))

plt.plot(n_values, mean_values, label='Mean Value', marker='o', color='blue', linestyle='-', markersize=6)
plt.plot(n_values, variances, label='Variance', marker='s', color='green', linestyle='-', markersize=6)
plt.plot(n_values, std_devs, label='Standard Deviation', marker='^', color='red', linestyle='-', markersize=6)

highlight_n = [m, m**2]
highlight_color = 'orange'

highlight_mean_values = [mean_values[i] for i in range(len(n_values)) if n_values[i] in highlight_n]
highlight_variances = [variances[i] for i in range(len(n_values)) if n_values[i] in highlight_n]
highlight_std_devs = [std_devs[i] for i in range(len(n_values)) if n_values[i] in highlight_n]
highlight_n_values = [n_values[i] for i in range(len(n_values)) if n_values[i] in highlight_n]
print(highlight_mean_values, highlight_n_values)

plt.scatter(highlight_n_values, highlight_mean_values, marker='o', color=highlight_color, s=100, edgecolors='black', zorder=5)
plt.scatter(highlight_n_values, highlight_variances,  marker='s',color=highlight_color, s=100, edgecolors='black', zorder=5)
plt.scatter(highlight_n_values, highlight_std_devs,  marker='^',color=highlight_color, s=100, edgecolors='black', zorder=5)

# Labels and title
plt.xlabel("n")
plt.ylabel("Values")
plt.title("Mean, Variance, and Standard Deviation vs. n")
plt.legend()
plt.grid(True)
plt.savefig("./plots/"+name+'.png', dpi=300)

print(name, "complete")