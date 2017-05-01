import numpy as np
import scipy.stats
import math

def calculateMean(N):
    coins = np.array(range(1,N+1))
    i = 1
    mean = 0.0
    prev_mean = 1.0  # dummy mean - to enter the while loop for the first time
    err = 0.000001
    total_all_payments = 0.0
    while abs(mean - prev_mean) >= err:     # for convergence
        total_payment = 0
        prev = 0
        choices = np.random.choice(coins, size=N, replace=False)
        #print(i, choices)
        for e in choices:
            total_payment += abs(prev - e)
            prev = e
        total_all_payments += total_payment
        prev_mean = mean
        mean = total_all_payments / i
        i += 1
    return mean

def calculateStandardDeviation(N, mean):
    coins = np.array(range(1, N + 1))
    i = 1
    stand_dev = 0.0
    prev_stand_dev = 1.0  # dummy mean - to enter the while loop for the first time
    err = 0.000001
    total_diff = 0.0
    while abs(stand_dev - prev_stand_dev) >= err:  # for convergence
        total_payment = 0
        prev = 0
        choices = np.random.choice(coins, size=N, replace=False)
        # print(i, choices)
        for e in choices:
            total_payment += abs(prev - e)
            prev = e
        total_diff += pow(total_payment - mean, 2)
        prev_stand_dev = stand_dev
        stand_dev = math.sqrt(total_diff / i)
        i += 1
    return stand_dev

mean_N10 = calculateMean(10)
sd_N10 = calculateStandardDeviation(10, mean_N10)
prob_payment_gteq_45 = 1.0 - scipy.stats.norm(mean_N10, sd_N10).cdf(45)
print("Mean of total payment for N=10 is : " + str(mean_N10))
print("Standard deviation for N=10 is : " + str(sd_N10))
print("Probability that total payment is greater than or equal to 45 for N=10 is : " + str(prob_payment_gteq_45))

mean_N20 = calculateMean(20)
sd_N20 = calculateStandardDeviation(20, mean_N20)
prob_payment_gteq_160 = 1.0 - scipy.stats.norm(mean_N20, sd_N20).cdf(160)
print("Mean of total payment for N=20 is : " + str(mean_N20))
print("Standard deviation for N=20 is : " + str(sd_N20))
print("Probability that total payment is greater than or equal to 160 for N=20 is : " + str(prob_payment_gteq_160))

#Mean of total payment for N=10 is : 38.4952103063
#Standard deviation for N=10 is : 6.37599454618
#Probability that total payment is greater than or equal to 45 for N=10 is : 0.153816806676
#Mean of total payment for N=20 is : 143.998689384
#Standard deviation for N=20 is : 18.0001500371
#Probability that total payment is greater than or equal to 160 for N=20 is : 0.187013822878

#Mean of total payment for N=10 is : 38.507943346
#Standard deviation for N=10 is : 6.36945023553
#Probability that total payment is greater than or equal to 45 for N=10 is : 0.15404235223
#Mean of total payment for N=20 is : 143.531698359
#Standard deviation for N=20 is : 18.4624164054
#Probability that total payment is greater than or equal to 160 for N=20 is : 0.186198988971