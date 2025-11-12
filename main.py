import math

result = 50 #starting utility

happinessUtil = [1,2,4,4]
happinessProb = [0.5,0.5,0.3,0.2]

enjoymentUtil = [1,2,4,4]
enjoymentProb = [0.5,0.5,0.3,0.3]

enjoymentUtil = [1,2,4,4]
enjoymentProb = [0.5,0.5,0.3,0.3]

enjoymentUtil = [1,2,4,4]
enjoymentProb = [0.5,0.5,0.3,0.3]

enjoymentUtil = [1,-2,4,-1]
enjoymentProb = [0.5,0.5,0.3,0.2]


def calculateOutcomes(utils, probs):
    output = []
    for i in range (0,len(utils)):
        util = utils[i]*probs[i]
        output.append(util)
    return output

#def calculateExpectedUtility():
# tar inn outcomes 
# spits out expected utilities for each category

#display
# show assessment, value from 0 to 100
# colour coded
# ascii art

print(f"Enjoyment:{calculation(enjoymentUtil,enjoymentProb)}")
print(f"Happiness:{calculation(happinessUtil,happinessProb)}")
#rekn ut 1
# enjoyment
# +10
# -50
#  +5
#   0
#vekt=2
#ut1=result*vekt

#rekn ut 2
# lifespan
# +20
# -30
# +10
# -10
#vekt 1.5
#ut2=result*vekt

#maks mulig util
#ut1=10*2
#ut2=20*1.5
#tot=50

#maks mulig util=result+tot



#begynn på 0
# 0-50+20=-30

#begynn på 50
# 50-50+20=20