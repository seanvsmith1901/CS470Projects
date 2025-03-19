import math
import random

from sympy import false


# ok so what shoudl I take into account for this
# total population
# currently infected
# spread rate
# number of people who will actually get the vaccine
# vaccine stopping rate
# days for vaccine to kick in

# how many people will be saved from this thing (calculate this fetcher)



# total population as an int, currenltly infected as an int, how manyt people will get infected per infection, as a percent, time ti takes for vaccine to kick in, and how many people the vaccine will kill.
def utility_calculation(total_population, currently_infected, spread_rate, number_of_people_who_will_actually_get_vaccine,
                        vaccine_stopping_rate, days_for_vaccine_to_kick_in, mortality_rate, risk_aversity):
    # just get all of the edge cases out of the way.
    if risk_aversity == "MAX":
        total_population *= 0.5
        currently_infected *= 2
        spread_rate *= 2
        number_of_people_who_will_actually_get_vaccine *= 0.5
        vaccine_stopping_rate *= 2
        days_for_vaccine_to_kick_in *= 0.5
        mortality_rate *= 2


    if risk_aversity == "MIN":
        total_population *= 2
        currently_infected *= 0.5
        spread_rate *= 0.5
        number_of_people_who_will_actually_get_vaccine *= 2
        vaccine_stopping_rate *= 0.5
        days_for_vaccine_to_kick_in *= 2
        mortality_rate *= 0.5



    if (currently_infected == 0): return False
    if total_population == 0: return False
    if spread_rate == 0: return False
    if spread_rate == 1: return True
    if number_of_people_who_will_actually_get_vaccine == 0: return False
    if vaccine_stopping_rate == 0: return False
    if days_for_vaccine_to_kick_in == math.inf: return False
    if mortality_rate == 0: return False
    max_infected_percent = 10 # no more than 10# population infected
    max_dead_percent = 20 # no more than 5% rn.




    # if everyone is going to get infected
    if (currently_infected * (spread_rate ** days_for_vaccine_to_kick_in) > total_population):
        print("1")
        return False # not worth forcing vaccine. Everyone will get infected

    # a quick google search says that society will likely not be feeling well if 5% of the population dies.
    # we can model infections and whatnot but I am most concerned with deaths, even though infections
    # I will also consider more than 10% of the population infected to be another porblem point, as that will likely shut things down as well.
    # so if we exceed either of those 2, shut down.
    if (currently_infected * (spread_rate ** days_for_vaccine_to_kick_in) > total_population/max_infected_percent):
        print("1")
        return True # more than 10 percent are already infectd, we gotta turn this around now.

    if ((currently_infected * (spread_rate ** days_for_vaccine_to_kick_in) * mortality_rate) > total_population / max_dead_percent ):
        print("2")
        return True # more than 5 percent are already dead. turn this around now.

    # so we have modeled our unacceptable cases. what are accedptable cases? when would the government not want to put a mandate?

    if spread_rate < 1 and number_of_people_who_will_actually_get_vaccine < 0.01:
        print("3")
        return False # just not worth trying to enforce, no one is going to do it, will go away on its own.

    if spread_rate > 1: # so more people WILL get infected
        if mortality_rate > 0.1: # more than 10 percent mortality
            if currently_infected / total_population > 0.1:
                if number_of_people_who_will_actually_get_vaccine > 0.5:
                    print("4")
                    return True
                else:
                    print("5")
                    return False
            else:
                print("6")
                return False
        else:
            print("7")
            return False

    print("8")
    if risk_aversity == "MIN":
        return False
    if risk_aversity == "MAX":
        return True
    if risk_aversity == "AVG":
        return random.choice([True, False])
    return True # better safe than sorry.

if __name__ == "__main__":


    print("this is the output of the fetcher ", utility_calculation(330000000, 0, 0.01, 0.9, 0.7, 3, 1, "AVG"))