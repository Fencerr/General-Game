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

def getCurrentPopulation():
    return CurrentPopulation


def getAnnualFoodSupply():
    return CurrentAnnualFoodSupply


def addCO2Emitter(PercentPerYear):
    global CO2ChangePerYear
    CO2ChangePerYear += PercentPerYear


def update():
    global CurrentPopulation
    global CurrentAnnualFoodSupply
    global PercentCO2

    # CO2 Levels
    PercentCO2 += CO2ChangePerYear

    # Food supply change
    CurrentAnnualFoodSupply = CurrentAnnualFoodSupply * numpy.clip((FoodChangeRate - PercentCO2), 0, 1)

    # Food Supply Effect Population
    NumberCanLive = CurrentAnnualFoodSupply / FoodPerAnimal
    CurrentPopulation = round(numpy.clip(NumberCanLive, 0, CurrentPopulation))

    # Reproduction
    CurrentPopulation = round(CurrentPopulation * NaturalGrowthRate)

    return CurrentPopulation
