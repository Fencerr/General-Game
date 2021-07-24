import numpy

"""
This file is responsible for simulating and updating the population.
"""


StartingPopulation = 10000000  # The starting population at the start of the game.
CurrentPopulation = StartingPopulation  # The current population.
FoodPerAnimal = 5  # The units of food used by each alive animal every update.
StartingAnnualFoodSupply = StartingPopulation * 8  # Starting supply of food.
CurrentAnnualFoodSupply = StartingAnnualFoodSupply  # Current annual food supply.

NaturalGrowthRate = 1.10  # The rate at which the population will grow every update.
FoodChangeRate = 1  # The rate at which the food supply will change every update.
PercentCO2 = 0  # Percent of the atmosphere that is CO2.
CO2ChangePerYear = 0  # The change in PercentCO2 per year.

KilledThisYear = 0  # Number of elephants killed in an update cycle.


# Returns the current population.
def getCurrentPopulation():
    return CurrentPopulation


# Returns the current annual food supple.
def getAnnualFoodSupply():
    return CurrentAnnualFoodSupply


# Adds a CO2 emitter that will add the given amount of CO2 a year.
def addCO2Emitter(PercentPerYear):
    global CO2ChangePerYear
    CO2ChangePerYear += PercentPerYear


# Kills the given amount of animals.
def kill(Amount):
    global KilledThisYear
    KilledThisYear += Amount


# Updates the population and CO2 level.
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
