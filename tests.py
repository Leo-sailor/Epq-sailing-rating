def calculateTotalSum(sum, *arguments):
    if arguments == ():
        print(True)
    totalSum = 0
    totalSum += sum
    for number in arguments:
        totalSum += number
    print(totalSum)


# function call
calculateTotalSum(4)
