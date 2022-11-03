import math

# Identify the Big-O time complexity of the following functions,
# relative to the size of the input

TimeComplexity = {
  'FIX_ME': 'wrong answer',
  'CONSTANT': 'constant',
  'LOGARITHMIC': 'logarithmic',
  'LINEAR': 'linear',
  'QUADRATIC': 'quadratic',
  'EXPONENTIAL': 'exponential',
}

# TODO: Update this constant ex. sortedIndexOfTimeComplexity = TimeComplexity.EXPONENTIAL
sortedIndexOfTimeComplexity = TimeComplexity['EXPONENTIAL']

def sortedIndexOf(list, targetElement):
  minIndex = 0
  maxIndex = len(list) - 1
  currentIndex = 0
  currentElement = 0

  while (minIndex <= maxIndex):
    currentIndex = math.floor((minIndex + maxIndex) / 2)
    currentElement = list[currentIndex]

    if (currentElement < targetElement):
      minIndex = currentIndex + 1
    elif (currentElement > targetElement):
      maxIndex = currentIndex - 1
    else:
      return currentIndex

  return -1;


# TODO: Update this constant
findDuplicatesTimeComplexity = TimeComplexity['LINEAR']

def findDuplicates(string):
  tracker = {}
  result = []

  for letter in string:
    tracker[letter] = tracker[letter] or 0;

    if (tracker[letter] == 1):
      result.push(letter)


    tracker[letter] += 1

  return result;

# TODO: Update this constant
hasDuplicatesTimeComplexity = TimeComplexity['LINEAR']

def hasDuplicates(list):
  for index, item in enumerate(list):
    try:
      if (list.index(item, index) != -1):
        return True
    except ValueError:
      print(f"Value {item} not found in string!")

  return False



# TODO: Update this constant
removeLastThreeElementsTimeComplexity = TimeComplexity['LINEAR']

def removeLastThreeElements(list):
  numberOfElementsToRemove = 3

  while (numberOfElementsToRemove > 0):
    list.pop()
    numberOfElementsToRemove -= 1


# TODO: Update this constant
increasingStepTimeComplexity = TimeComplexity['LINEAR']

def increasingStep(number):
  counter = 1

  while counter < number:
    print(counter)
    counter *= 2


# TODO: Update this constant
printRangeTimeComplexity = TimeComplexity['LINEAR']

def printRange(list):
  for item in list:
    for number in range(10):
      print(f"{item} {number + 1}")
