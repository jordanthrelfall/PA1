import sys

# Class to store process data
class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.response_time = 0
        self.turnaround_time = 0

# Read in filename from command line
inputFileCMD = sys.argv[1]

# Generating the name of the output file
outputFilename = inputFileCMD.replace(".in", ".out")

# open the file for reading
inputFile = open(inputFileCMD, 'r')

# Creating the .out file with the output file name
outputFile = open(outputFilename, 'x')

fileList = inputFile.readlines()

lineNum = 0
line = ''
lineSplit = ''

processCount = 0
runFor = 0
scheduler = ''

processList = []
processNum = 0

with open(inputFileCMD) as file:
    while True:
        lineNum += 1
        line = file.readline()
        if line == 'end':
            break
        lineStrip = line.strip()
        lineSplit = lineStrip.split(' ')

        if lineSplit[0] == 'processcount':
            # sets global variable to the process count number
            processCount = int(lineSplit[1])
        elif lineSplit[0] == 'runfor':
            # sets global variable to the run for number
            runFor = int(lineSplit[1])
        elif lineSplit[0] == 'use':
            # sets variable for the algorithm to use
            scheduler = lineSplit[1]
        elif (lineSplit[0] == 'process') and (lineSplit[1] == 'name'):
            # adds all of the processes to a list
            processList.append(Process(lineSplit[2], int(lineSplit[4]), int(lineSplit[6])))


def fcfs(processes, run_for):
    current_time = 0
    queue = []
    completed_processes = []

    print(f"{len(processes)} processes")
    print("Using fcfs\n")

    # Sort processes based on arrival time
    processes.sort(key=lambda x: x.arrival)

    while processes or queue:
        for process in processes[:]:
            if process.arrival <= current_time:
                print(f"Time {current_time:3} : {process.name} arrived")
                queue.append(process)
                processes.remove(process)

        if queue:
            current_process = queue.pop(0)
            print(f"Time {current_time:3} : {current_process.name} selected (burst {current_process.burst})")

            current_process.response_time = max(0, current_time - current_process.arrival)

            while current_process.burst > 0:
                current_time += 1
                current_process.burst -= 1

                # Check for arrivals during the execution of the process
                for process in processes[:]:
                    if process.arrival == current_time:
                        print(f"Time {current_time:3} : {process.name} arrived")
                        queue.append(process)
                        processes.remove(process)

            print(f"Time {current_time:3} : {current_process.name} finished")

            current_process.turnaround_time = current_time - current_process.arrival
            completed_processes.append(current_process)
        else:
            print(f"Time {current_time:3} : Idle")
            current_time += 1

    print(f"Finished at time {current_time}")

    print("\nResults:")
    for process in completed_processes:
        print(f"{process.name} wait {process.response_time} turnaround {process.turnaround_time} response {process.response_time}")



# Call the fcfs simulator with the process list and run time
simulate_fcfs(processList, runFor)
