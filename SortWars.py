import random
import time
import tracemalloc as tm
import matplotlib.pyplot as plt


MILLISECONDS_PER_SECOND = 1000 #convert from milliseconds to seconds
DATASET_LABEL = 1000 #used for dataset labels to be in thousands
BYTE_TO_KILOBYTE = 1024 # bytes to kilobytes conversion
FIG_WIDTH = 12 # width of the figure
FIG_HEIGHT = 6 #height of the figure

#parameters
numSize = [10000, 100000] # list for dataset sizes
range_Start = 100000 # starting number range of dataset generation
range_End= 1000000 # ending number range of dataset generation

#function to generate datasets
def generateData (numSize, range_Start, range_End):
    # initializes an empty list to store datasets
    dataSets = []
    # loop through each dataset size
    for i in numSize:
        # generate a random datasets with unique numbers without duplications
        randomD = random.sample(range(range_Start, range_End),i)
        # generate Reversed dataset
        reversedD = sorted(randomD, reverse=True)

        #Write random dataset to a text file
        random_file_name ="random_" + str(i) + ".txt"
        #open a file to write random datasets
        with open(random_file_name, mode='w') as randomDataset:
            for num in randomD:
                randomDataset.write(str(num) + "\n")

        #Write Reversed dataset to file
        reversed_file_name ="reversed_" + str(i) + ".txt"
        #open a file to write reversed datasets
        with open(reversed_file_name, mode='w') as reversedDataset:
            for num in reversedD:
                reversedDataset.write(str(num) + "\n")

        #cofirmation message that the file is saved
        print("Saved:", random_file_name)
        print("Reversed:", reversed_file_name)

        #append the dataset information to the list
        dataSets.append(["random",randomD])
        dataSets.append(["reversed",reversedD])

    return dataSets

#function to perform merge sort and count swaps
def mergeSort(arr):
    # initializing the swap/compariosn counter
    mergeCounter = 0
    # goes ahead only if the array has more than one element
    if len(arr)>1:
        #splitting the array into two halves
        left_arr=arr[:len(arr)//2]
        right_arr=arr[len(arr)//2:]#integer division //

        #call mergesort recursively and sort both halves
        left_arr, leftcounter = mergeSort(left_arr)
        right_arr, rightCounter = mergeSort(right_arr)
        #update the counter
        mergeCounter += leftcounter + rightCounter

        #merging the two arrays
        a = 0 # left_arr index 
        b = 0 # right_arr index
        h = 0 # merged array index
        #merge the two halves
        while a < len(left_arr) and b < len(right_arr):
            # increment the swap/comparison counter
            mergeCounter += 1
            #compare the elements from both halves
            if left_arr[a] < right_arr[b]:
                arr[h] = left_arr[a] # placing the smaller element in the merged array
                a += 1 # move the index for the right half
                h += 1 #move the index for the left half
            else:
                arr[h] = right_arr[b] #place the smaller element in merged array
                b += 1 #move the index for the right half
                h += 1 #move the merged array index
        #add any remaining elements from left array
        while a < len(left_arr):
            arr[h] = left_arr[a]
            a += 1
            h += 1
        # add any remaining elements from right array
        while b < len(right_arr):
            arr[h] = right_arr[b]
            b += 1
            h += 1

    return arr, mergeCounter #returns the sorted array and swap/comparison count

#function to perfrom quick sort and count swpas/comparions
def quicksort(arr, left, right):
    # initializing swaps/compariosns counter
    quickCounter = 0
    # base case
    if left < right:
        #partitioning the array
        partition_pos, partitionCounter = partition(arr, left, right)
        #updating the counter
        quickCounter += partitionCounter

        #recursively sort the left and right subarrays
        sorted_left, leftcounter = quicksort(arr, left, partition_pos - 1)
        quickCounter += leftcounter
        sorted_right, rightCounter = quicksort(arr, partition_pos + 1, right )
        quickCounter += rightCounter
    return arr, quickCounter

#function to partition the array for quicksort
def partition(arr, left, right):
  # initialize the swaps/comparsions counter
  partitionCounter = 0
  # find the middle index
  mid = (left + right) // 2
  # swap the middle element with the rightmost
  arr[mid], arr[right] = arr[right], arr[mid]

  #select the pivot
  pivot = arr[right]
  # initialize the partition index
  i = left - 1
  #iterate through the array
  for j in range(left, right):
      #increment the swaps counter
      partitionCounter += 1
      # compare elements with pivot
      if arr[j] <= pivot:
          i += 1
          # swapping the elements
          arr[i], arr[j] = arr[j], arr[i]
  # places the pivot in the correct position
  arr[i + 1], arr[right] = arr[right], arr[i + 1]
  #returns the partition index and counter
  return i + 1, partitionCounter

def DatasetCopy(dataSets):
    mergeCopy = [] # stores copies of merge sort
    quickCopy = [] # stores copies of quick sort
    datasetInfo =[] #stores dataset information

    for dataSet in dataSets:
        datasetType = dataSet[0] #random and reversed
        numbers = dataSet[1] #the actual list of numbers
        size = len(numbers) #get size of the numbers

        #make copies of the data
        merge_copy = numbers.copy()
        quick_copy = numbers.copy()

        #append the copies and of the relevant lists
        mergeCopy.append(merge_copy)
        quickCopy.append(quick_copy)
        datasetInfo.append([datasetType, size])

    return mergeCopy, quickCopy, datasetInfo

mergeResults = [] # lists to store the sorted results of merge sort
quickResults = [] # lists to store the sorted results of quick sort

def SaveSorted_data(dataSets):
    print("\n--MERGE SORT PERFORMANCE ANALYSIS--")
    #loop to iterate over each dataset
    for dataSet in dataSets:
        #get the dataset type
        datasetType = dataSet[0]
        #get the original data
        originalData = dataSet[1]
        #get the size of the dataset
        size = len(originalData)

        #measure time and memory
        mergeData = originalData.copy() #make a temporary copy of the datasets
        tm.start() #start memory tracking
        start_time = time.time()
        sortedData, mergeCounter = mergeSort(mergeData) #perfrom merge sort
        end_time = time.time()
        current_memory, peak_memory = tm.get_traced_memory() # get memory usage
        tm.stop() #stop memory tracking

        #create dataset label
        datasetLabel = f"{datasetType}_{size // DATASET_LABEL}k"

        merge_Time = (end_time - start_time) * MILLISECONDS_PER_SECOND #calculate execution time

        #print the performance metrics
        print(f"Analyzing Merge Sort on {datasetType} with {size} elements")
        print(f"Execution Time: {merge_Time:.2f} ms")
        print(f"Memory usage:{peak_memory /BYTE_TO_KILOBYTE :.2f} KB") # display current memory usage
        print(f"Number of Comparisons(Swaps):{mergeCounter}\n")

        # save the sorted data to files
        mergefile = f"merge_Sorted_{datasetType}_{size}.txt"
        with open(mergefile, mode='w') as f:
            for num in mergeData:
                f.write(f"{num}\n")
        #print("Saved:", mergefile)
        mergeResults.append([datasetLabel, merge_Time, peak_memory / 1024, mergeCounter]) #append the results

    print("\n--QUICK SORT PERFORMANCE ANALYSIS--")
    for dataSet in dataSets:
        #get the data information
        datasetType = dataSet[0]
        originalData = dataSet[1]
        size = len(originalData)

        datasetLabel = f"{datasetType}_{size // DATASET_LABEL}k"

        #measure time
        quickData = originalData.copy() # make a temporary copy of the datasets
        tm.start() #start memory tracking
        start_time = time.time()
        sortedData, quickCounter = quicksort(quickData, 0, len(quickData) - 1) #perfrom quick sort
        end_time = time.time()
        current_memory , peak_memory = tm.get_traced_memory() # get memory usage
        tm.stop()

        quick_Time = (end_time - start_time) * MILLISECONDS_PER_SECOND # calculate execution time

        #print the perfromace metrics
        print(f"Analyzing Quick Sort on {datasetType} with {size} elements")
        print(f"Execution Time: {quick_Time:.2f} ms")
        print(f"Memory usage:{peak_memory / BYTE_TO_KILOBYTE:.2f} KB")
        print(f"Number of Comparisons(Swaps):{quickCounter}\n")

        #save sorted data into files
        qucikfile = f"quick_Sorted_{datasetType}_{size}.txt"
        with open(qucikfile, mode='w') as f:
            for num in quickData:
                f.write(f"{num}\n")
        #print("Saved:", qucikfile)
        quickResults.append([datasetLabel, quick_Time, peak_memory / 1024, quickCounter])

    return mergeResults, quickResults

#function to generate the graphs for merge sort performance
def generate_MergeGraphs(mergeResults):
    #getting the dataset labels , time , memory , counts
    datasets =[dataset[0] for dataset in mergeResults]
    time = [dataset[1] for dataset in mergeResults]
    memory = [dataset[2] for dataset in mergeResults]
    swaps = [dataset[3] for dataset in mergeResults]

    #define colors for bars
    barColors = {
        "random_10k": 'blue',
        "reversed_10k": 'red',
        "random_100k": 'green',
        "reversed_100k": 'yellow',
    }

    memory_colors = [barColors[dataset] for dataset in datasets]
    time_colors = [barColors[dataset] for dataset in datasets]
    swap_colors = [barColors[dataset] for dataset in datasets]

    #memory graph
    plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
    plt.bar(datasets, memory, color=memory_colors)
    plt.title("Merge Sort - Memory Usage")
    plt.ylabel("Memory(KB)")
    plt.xlabel("Datasets")
    plt.savefig("Merge_memory.png")
    plt.show()

    # Time graph
    plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT)) #set the fig size
    plt.bar(datasets, time, color=time_colors)
    plt.title("Merge Sort - Execution Time")
    plt.ylabel("Time(ms)")# y-axis label
    plt.xlabel("Datasets")# x-axis label
    plt.savefig("Merge_time.png") #saving the memory graph
    plt.show()#display the graph

    # Swaps graph
    plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
    plt.bar(datasets, swaps, color=swap_colors)
    plt.title("Merge Sort - Number of Comparisons")
    plt.ylabel("Swaps/Comparisons")
    plt.xlabel("Datasets")
    plt.savefig("Merge_swaps.png")
    plt.show()

#function to generate the graphs for quick sort performance
def generate_QuickGraphs(quickResults):
    datasets = [dataset[0] for dataset in quickResults]
    time = [dataset[1] for dataset in quickResults]
    memory = [dataset[2] for dataset in quickResults]
    swaps = [dataset[3] for dataset in quickResults]

    #colors for the bar charts
    barColors = {
        "random_10k": 'blue',
        "reversed_10k": 'red',
        "random_100k": 'green',
        "reversed_100k": 'yellow',
    }

    memory_colors = [barColors[dataset] for dataset in datasets]
    time_colors = [barColors[dataset] for dataset in datasets]
    swap_colors = [barColors[dataset] for dataset in datasets]

    #memory graph
    plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT)) #set figure size
    plt.bar(datasets, memory, color=memory_colors)
    plt.title("Quick Sort - Memory Usage")
    plt.ylabel("Memory(KB)")
    plt.xlabel("Datasets")
    plt.savefig("Quick_memory.png")
    plt.show()#display the graph

    # Time graph
    plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
    plt.bar(datasets, time, color=time_colors)
    plt.title("Quick Sort - Execution Time")
    plt.ylabel("Time(ms)")
    plt.xlabel("Datasets")
    plt.savefig("Quick_time.png")
    plt.show()

    # Swaps graph
    plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
    plt.bar(datasets, swaps, color=swap_colors)
    plt.title("Quick Sort - Number of Comparisons")
    plt.ylabel("Swaps/Comparisons")
    plt.xlabel("Datasets")
    plt.savefig("Quick_swaps.png")
    plt.show()

#generate the datasets
dataSets = generateData(numSize, range_Start, range_End)

#make copies of the datasets
mergeCopy, quickCopy, datasetInfo = DatasetCopy(dataSets)

#Sort and save the datasets to a textfile
SaveSorted_data(dataSets)

#generate the graphs for merge sort and quick sort
generate_MergeGraphs(mergeResults)
generate_QuickGraphs(quickResults)

#references used
#https://youtu.be/cVZMah9kEjI?si=UZA7axQOQTi-6nW1
#https://youtu.be/9KBwdDEwal8?si=Fl5Atb4pSRTujNmB
#https://www.geeksforgeeks.org/bar-plot-in-matplotlib/
#https://www.w3schools.com/python/python_lists.asp
#https://www.w3schools.com/python/matplotlib_bars.asp
