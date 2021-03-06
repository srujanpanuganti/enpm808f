# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 16:17:23 2019

@author: Srujan Panuganti
"""
#%%
import numpy as np
import matplotlib.pyplot as plt
import random
import math

                ###########################################
                ## defining a class for Assiciative cells##
                ###########################################
                
class association:
    def __init__(self,index,weight):
        self.index = 0
        self.weight = []
        #self.response = np.zeros(35,1)

#%%
                ######################
                ##preparing the data##
                ######################

Fs = 100
f = 1
sample = 100

x = np.arange(sample)
y = np.sin(2 * np.pi * f * x / Fs)

plt.plot(x, y, 'r')
plt.show()

func = np.stack((x.T, y.T), axis=0)
data = func.T

np.random.shuffle(data)

train_data = data[:70]
test_data = data[70:]

                ###################
                ## Training data ##
                ###################

X = train_data[:, 0]
Y = train_data[:, 1]

                ###################
                ## Testing data  ##
                ###################

X_test = test_data[:,0]
Y_test = test_data[:,1]

plt.figure(1)
plt.plot(X,Y,'r+',label = 'sensory input data')
plt.legend()
plt.show()

#print(X_test)
#print('\n')
#print(Y_test)

#%%
beta = 5
assoc_num = 35

weights = np.ones((35,1))
rate = 1


def assoc_values(ind, beta):
    weights = []
    b = (beta//2)
    for i in range(ind - b, ind + b + 1):
        weights.append(i)
    return weights

def assoc_index(i,beta,assoc_num,sample):
    i = int(i)
    a_ind = beta//2 + ((assoc_num - 2*(beta//2))*i)/sample
    return math.floor(a_ind)

def meanSqEr(weights, synapse_weight,X,Y):
    meansq =0
    for i in range(0,len(synapse_weight)):
        sum_syn = 0
        for j in synapse_weight[i]:
            sum_syn = sum_syn + weights[j]
        meansq += (sum_syn - Y[i])**2
    return meansq

def test(weights,synapse_weight):
    output = []
    for i in range(0,len(synapse_weight)):
        sum_syn = 0
        for j in synapse_weight[i]:
            sum_syn += weights[j]
        output.append(sum_syn)
    return output


synapse = association([],[])
synapse_test = association([],[])

                #######################################
                ### Creating the Associative cells  ###
                #######################################

for ind in X:
    synapse.index = assoc_index(ind, beta , assoc_num, sample)
    synapse.weight.append(assoc_values(synapse.index, beta))

for ix in X_test:
    synapse_test.index = (assoc_index(ix, beta , assoc_num, sample))
    synapse_test.weight.append(assoc_values(synapse_test.index, beta))
    

#%%

error_list = []
error_plot = []

prevError = 0
currentError = 10
iterations = 0

while iterations < 100 and abs(prevError - currentError) > 0.00001:
    prevError = currentError
    #print(abs(prevError- currentError))
    for i in range(0,len(synapse.weight)):
        sum_syn = 0
        for j in synapse.weight[i]:
            sum_syn += weights[j]
            #print(sum_syn)
        error = sum_syn - Y[i]
        #print(error)
        correction  = error/beta
        #print(correction)
        for j in synapse.weight[i]:
            weights[j] -= rate*correction
            #print(correction)
    currentError = float(meanSqEr(weights,synapse.weight,X,Y))
    #print(currentError)
    error_list.append(currentError)
    iterations += 1
    error_plot.append(iterations)

plt.figure(2)
plt.plot(np.asarray(error_plot), np.asarray(error_list), 'r--',label = 'error convergence')
plt.legend()
plt.show()

#%%
                ####################################
                ### Testing the trained synapses ###
                ####################################

output = test(weights, synapse_test.weight)


plt.figure(3)
plt.plot(X,Y,'g+',label = 'training data')
plt.plot(X_test,Y_test,'r+',label = 'test data')
plt.plot(X_test,np.asarray(output),'bo', label = 'predicted outputs')
plt.legend()
plt.show()
# =============================================================================

#%%
plt.plot(X_test,Y_test,'g+',label = 'test data')
plt.legend()
plt.show()