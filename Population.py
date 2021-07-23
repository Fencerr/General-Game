import numpy

StartingPopulation = 10000000
CurrentPopulation = StartingPopulation
FoodPerAnimal = 5
StartingAnnualFoodSupply = StartingPopulation * 8
CurrentAnnualFoodSupply = StartingAnnualFoodSupply

NaturalGrowthRate = 1.10
FoodChangeRate = 1
PercentCO2 = 0
CO2ChangePerYear = 0

KilledThisYear = 0


def getCurrentPopulation():
    return CurrentPopulation


def getAnnualFoodSupply():
    return CurrentAnnualFoodSupply


def addCO2Emitter(PercentPerYear):
    global CO2ChangePerYear
    CO2ChangePerYear += PercentPerYear


def kill(Amount):
    global KilledThisYear
    KilledThisYear += Amount


def update():
    global CurrentPopulation
    global CurrentAnnualFoodSupply
    global PercentCO2
    global KilledThisYear

    if CurrentPopulation <= 0:
        return

    # Killed From this year
    CurrentPopulation -= KilledThisYear
    KilledThisYear = 0

    # CO2 Levels
    PercentCO2 = PercentCO2 + (CO2ChangePerYear/100)

    # Food supply change

    CurrentAnnualFoodSupply *= numpy.clip((FoodChangeRate - PercentCO2), 0, 1)

    # Food Supply Effect Population
    NumberCanLive = CurrentAnnualFoodSupply / FoodPerAnimal

    CurrentPopulation = round(numpy.clip(NumberCanLive, 0, CurrentPopulation))


    # Reproduction
    CurrentPopulation = round(CurrentPopulation * NaturalGrowthRate)

    return max(CurrentPopulation, 0)


i = 0
for i in range(1, 100):
    i += 1
    addCO2Emitter(.5)
    kill(i*100)
    print(update())
