import math

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
                        vaccine_stopping_rate, days_for_vaccine_to_kick_in, mortality_rate):
    # just get all of the edge cases out of the way.
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
        return False # not worth forcing vaccine. Everyone will get infected

    # a quick google search says that society will likely not be feeling well if 5% of the population dies.
    # we can model infections and whatnot but I am most concerned with deaths, even though infections
    # I will also consider more than 10% of the population infected to be another porblem point, as that will likely shut things down as well.
    # so if we exceed either of those 2, shut down.
    if (currently_infected * (spread_rate ** days_for_vaccine_to_kick_in) > total_population/max_infected_percent):
        return True # more than 10 percent are already infectd, we gotta turn this around now.

    if ((currently_infected * (spread_rate ** days_for_vaccine_to_kick_in) * mortality_rate) > total_population / max_dead_percent ):
        return True # more than 5 percent are already dead. turn this around now.

    # so we have modeled our unacceptable cases. what are accedptable cases? when would the government not want to put a mandate?

    if spread_rate < 1 and number_of_people_who_will_actually_get_vaccine < 1:
        return False # just not worth trying to enforce, no one is going to do it, will go away on its own.

    return True # better safe than sorry.

if __name__ == "__main__":


    print("this is the output of the fetcher ", utility_calculation(330000000, 100000, 1.5, 0.6, 0.8, 3, 0.1))