from sympy import false


# ok so what shoudl I take into account for this
# total population
# currently infected
# spread rate
# number of people who will actually get the vaccine
# vaccine stopping rate
# days for vaccine to kick in
# vaccine mortality rate

# how many people will be saved from this thing (calculate this fetcher)




def utility_calculation(total_population, currently_infected, spread_rate, number_of_people_who_will_actually_get_vaccine, vaccine_stopping_rate, days_for_vaccine_to_kick_in, vaccine_mortality_rate):
    pass
    if (currently_infected == 0):
        return False
    # so the main goal is to figure out how many people will actually die. if the number of currently effected * the spread rate * days_to_stop is greater than current population, than it does no good
    if (currently_infected * (spread_rate ** days_for_vaccine_to_kick_in) > total_population):
        return False # not worth forcing vaccine.
    # I will do the rest tomorrow. Maybe.

























if __name__ == "__main__":

    print("this is the output of the fetcher ", utility_calculation())