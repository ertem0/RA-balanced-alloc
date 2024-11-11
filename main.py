import random
import math
import time
import pickle
import subprocess

def calculate_median(arr):
    n = len(arr)
    if n % 2 == 1:
        return arr[n // 2]
    else:
        return (arr[n // 2 - 1] + arr[n // 2]) / 2

class Data:
    def __init__(self):
        self.m = 0
        self.n_values = []
        self.mean_values = []
        self.variances = []
        self.std_devs = []

    def import_from_testcases(self, data):
        self.m = data[0].m
        self.n_values = [obj.n for obj in data]
        self.mean_values = [obj.mean_value for obj in data]
        self.variances = [obj.variance for obj in data]
        self.std_devs = [obj.std for obj in data]
        return self

    def import_from_arrays(self, m, n_values, mean_values, variances, std_devs):
        self.m = m
        self.n_values = n_values
        self.mean_values =  mean_values
        self.variances = variances
        self.std_devs = std_devs
        return self
class Bucket:
    def __init__(self):
        self.value = 0

    def __str__(self):
        return str(self.value)

class ChoosingFunctions:
    def __init__(self, d=None, beta=None, k=None):
        self.d = d
        self.beta = beta
        self.k = k

    def d_choice(self, buckets):
        if(self.d == 1):
            return random.choice(buckets)
        sample = random.sample(buckets, self.d)
        min_value = min(sample, key=lambda bucket: bucket.value).value
        min_buckets = filter(lambda x: x.value == min_value, sample)
        return random.choice(list(min_buckets))

    def beta_choice(self,buckets):
        r = random.uniform(0, 1)
        if(r < self.beta):
            self.d = 1
        else:
            self.d = 2
        return self.d_choice(buckets)

    def k_beta_choice(self, buckets):
        r = random.uniform(0, 1)
        if(r < self.beta):
            return random.choice(buckets)
        else:
            self.d = 2
        return self.k_choice(buckets)

    def k_choice(self, buckets):
        values = [bucket.value for bucket in buckets]
        values.sort()
        median = calculate_median(values)
        sample = random.sample(buckets, 2)
        bucket_selected = []
        if sample[0].value < median:
            bucket_selected.append(sample[0])
        if sample[1].value < median:
            bucket_selected.append(sample[1])
        if len(bucket_selected) % 2==0:
            if self.k == 1:
                return random.choice(sample)
        else:
            return bucket_selected[0]
        #k==2

        second_selection = []
        if len(bucket_selected) == 0:
            upper_half = values[(len(values) + 1) // 2:]
            Q25 = calculate_median(upper_half)
            if sample[0].value < Q25:
                second_selection.append(sample[0])
            if sample[1].value < Q25:
                second_selection.append(sample[1])
            if len(second_selection) % 2==0:
                return random.choice(sample)
            else:
                return second_selection[0]
        else:
            lower_half = values[:len(values) // 2] 
            Q75 = calculate_median(lower_half)
            if sample[0].value < Q75:
                second_selection.append(sample[0])
            if sample[1].value < Q75:
                second_selection.append(sample[1])
            if len(second_selection) % 2==0:
                return random.choice(sample)
            else:
                return second_selection[0]  
        
    def get_func(self):
        if self.k and self.beta:
            return self.k_beta_choice
        elif self.beta:
            return self.beta_choice
        elif self.d:
            return self.d_choice
        elif self.k:
            return self.k_choice
        

class Instance:
    def __init__(self, n_buckets, choosing_def):
        self.buckets = [Bucket() for x in range(n_buckets)]
        self.n_buckets = n_buckets
        self.choosing_def = choosing_def
        pass

    def drop_balls(self, n, batch):
        for x in range(0,n, batch):
            selected_buckets = []
            for i in range(batch):
                selected_buckets.append(self.choosing_def(self.buckets))
            for bucket in selected_buckets:
                bucket.value += 1

        #calculating gap
        return max([bucket.value - n/self.n_buckets for bucket in self.buckets])
        
    def drop_balls_gap_each(self, n):
        results = []
        for x in range(0,n):
            bucket = self.choosing_def(self.buckets)
            bucket.value += 1
            results.append(max([bucket.value - x/self.n_buckets for bucket in self.buckets]))
        return results

    def __str__(self):
        return str(self.gap)

class TestCase:
    def __init__(self, sample, m, n, choosing_def, batch = 1):
        self.m = m
        self.results = []
        self.sample = sample
        self.choosing_def = choosing_def
        self.n = n
        self.batch = batch

    def results_balls(self):
        for x in range(self.sample):
            self.results.append(Instance(self.m, self.choosing_def).drop_balls(self.n, self.batch))

        self.mean_value = sum(self.results) / len(self.results)
        self.variance = sum((x - self.mean_value) ** 2 for x in self.results) / len(self.results)
        self.std = math.sqrt(self.variance)

        return self

    def results_balls_each(self):

        n = self.n
        mean = [0] * n
        variance = [0] * n
        std_deviation = [0] * n

        for x in range(self.sample):
            self.results.append(Instance(self.m, self.choosing_def).drop_balls_gap_each(self.n))
        
        for i in range(n):
            mean[i] = sum(array[i] for array in self.results) / self.sample

        for i in range(n):
            variance[i] = sum((array[i] - mean[i]) ** 2 for array in self.results) / self.sample

        for i in range(n):
            std_deviation[i] = variance[i] ** 0.5

        self.mean_value = mean
        #print(self.mean_value)
        self.variance = variance
        self.std_deviation = std_deviation
        return self


def k_test(m, k, t, name, beta=None):
    data = TestCase(t, m, m**2, ChoosingFunctions(k=k, beta=beta).get_func()).results_balls_each()
    payload = Data().import_from_arrays(data.m, range(1,data.n +1), data.mean_value, data.variance, data.std_deviation)
    with open(name+'.pkl', 'wb') as file:
        pickle.dump(payload, file)

def d_test(m,d,t,name):
    data = []
    for n in range(0, m+1, 1):
        data.append(TestCase(t, m, n**2, ChoosingFunctions(d=d).get_func()).results_balls())
    payload = Data().import_from_testcases(data)
    with open(name+'.pkl', 'wb') as file:
        pickle.dump(payload, file)

def beta_test(m,beta,t,name):
    data = []
    for n in range(0, m+1, 1):
        data.append(TestCase(t, m, n**2, ChoosingFunctions(beta=beta).get_func()).results_balls())
    payload = Data().import_from_testcases(data)
    with open(name+'.pkl', 'wb') as file:
        pickle.dump(payload, file)

def d_batched_test(m,d,batch,t,name):
    data = []
    for n in range(1, ((m**2)//batch)+1):
        data.append(TestCase(t, m, n*batch, ChoosingFunctions(d = d).get_func(), batch).results_balls())
    payload = Data().import_from_testcases(data)
    with open(name+'.pkl', 'wb') as file:
        pickle.dump(payload, file)

def beta_batched_test(m,beta,batch,t,name):
    data = []
    for n in range(1, ((m**2)//batch)+1):
        data.append(TestCase(t, m, n*batch, ChoosingFunctions(beta = beta).get_func(), batch).results_balls())
    payload = Data().import_from_testcases(data)
    with open(name+'.pkl', 'wb') as file:
        pickle.dump(payload, file)

if __name__ == "__main__":
    #m has to be greater than batch
    m = 400
    t= 20
    betas = [0.25,0.5,0.75]
    batches = [1,2,10, 50, 80]
    start = time.time()

    for way in [1,2]:
        #simple test
        d_test(m,way,t,f'{way}choice')
        #batched test
        for batch in batches:
            d_batched_test(m,way,batch*m,t,f'{way}choice{batch}batched')
    for beta in betas:
        #simple test
        beta_test(m,beta,t,f'{beta}beta')
        #batched test
        for batch in batches: 
            beta_batched_test(m,beta,batch*m,t,f'{beta}beta{batch}batched')
    # k tests
    for k in [1,2]:
        k_test(m,k,t,f'{k}k2choice')
        for beta in betas:
            k_test(m,k,t,f'{k}k{beta}beta', beta=beta)

    print(time.time()-start)
    