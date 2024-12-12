validation_func = lambda x: x in [1,2,3]

validation_func(2)  # True
validation_func(4)  # False

print(validation_func(2))
print(validation_func(4))
