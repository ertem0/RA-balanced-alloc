import pickle
import matplotlib.pyplot as plt
from main import Data
import sys


#data for the plot
files = ["1k0.25beta",
         "1k0.5beta",
         "1k0.75beta",
         "1k2choice",
         "2k0.25beta",
         "2k0.5beta",
         "2k0.75beta",
         "2k2choice"]



datas = []
for name in files:
    with open(name + '.pkl', 'rb') as file:
        datas.append(pickle.load(file))

plt.figure(figsize=(10, 6))
for i in range(len(datas)):
    data = datas[i]
    m = data.m
    n_values = data.n_values
    mean_values = data.mean_values
    variances =  data.variances
    std_devs = data.std_devs

    plt.plot(n_values, mean_values, label=files[i], linestyle='-', markersize=6)
plt.xlabel("n")
plt.ylabel("Values")
plt.title("Mean vs. n")
plt.legend()
plt.grid()
plt.show()


plt.figure(figsize=(10, 6))
for i in range(len(datas)):
    data = datas[i]
    m = data.m
    n_values = data.n_values
    mean_values = data.mean_values
    variances =  data.variances
    std_devs = data.std_devs

    plt.plot(n_values, variances, label=files[i], linestyle='-', markersize=6)
plt.xlabel("n")
plt.ylabel("Values")
plt.title("Variance vs. n")
plt.legend()
plt.grid()
plt.show()


plt.figure(figsize=(10, 6))
for i in range(len(datas)):
    data = datas[i]
    m = data.m
    n_values = data.n_values
    mean_values = data.mean_values
    variances =  data.variances
    std_devs = data.std_devs

    plt.plot(n_values, std_devs, label=files[i], linestyle='-', markersize=6)
plt.xlabel("n")
plt.ylabel("Values")
plt.title("Standard Deviation vs. n")
plt.legend()
plt.grid()
plt.show()
