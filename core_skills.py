import random

rand_list = [random.randint(1,20) for _ in range(20)]
print(rand_list)

list_comprehension_below_10 = [no for no in rand_list if no < 10]
print(list_comprehension_below_10)

filter_list_comprehension_below_10 = list(filter(lambda no: no < 10, rand_list))
print(list_comprehension_below_10)


from datetime import datetime, timedelta

print(datetime.now() + timedelta(days=14))