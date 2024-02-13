import sys

class Process:
    def __init__(self, name, arrival_time, execution_time, status="Pending"):
        self.name = name
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.remaining_time = execution_time
        self.status = status

    def __str__(self):
        return f"Process '{self.name}' | Arrival Time: {self.arrival_time} | Execution Time: {self.execution_time} | Status: {self.status}"

def fcfs(processes, run_for, output_file):
    pass

def sjf(processes, run_for, output_file):
    pass

def round_robin(processes, quantum, run_for, output_file):
    first_execution_times = {}
    completion_times = {}
    current_time = 0
    queue = []
    processCopy = processes.copy()
    with open(output_file, "w") as file:

        file.write(f"{len(processes)} processes\n") #added from other prompt to get correct formatting
        file.write("Using Round-Robin\n") #added from other prompt to get correct formatting
        file.write(f"Quantum   {quantum}\n\n") #added from other prompt to get correct formatting

        while current_time < run_for: # had to remove  or queue or processes
            # Move processes from the original list to the queue as their arrival times are reached
            for process in processes:
                if process.arrival_time == current_time:
                    file.write(f"Time {current_time}: {process.name} Arrived\n")
                    queue.append(process)
                    processes.remove(process)

            if queue:
                current_process = queue.pop(0)
                if current_process.name not in first_execution_times:
                    first_execution_times[current_process.name] = current_time
                file.write(f"Time {current_time}: {current_process.name} Selected (burst {current_process.remaining_time})\n") # Changed from Burst{min(quantum, current_process.remaining_time)} by human
                current_process.status = "Running"
                burst_time = min(quantum, current_process.remaining_time)
                current_process.remaining_time -= burst_time
                for _ in range(burst_time):
                    current_time += 1
                    # Move processes from the original list to the queue as their arrival times are reached
                    for process in processes:
                        if process.arrival_time == current_time:
                            file.write(f"Time {current_time}: {process.name} Arrived\n")
                            queue.append(process)
                            processes.remove(process)
                if current_process.remaining_time == 0:
                    file.write(f"Time {current_time}: {current_process.name} Finished\n")
                    current_process.status = "Finished"
                    completion_times[current_process.name] = current_time
                elif queue: # Human changed from else to elif queue:
                    #file.write(f"Time {current_time}: {current_process.name} Waiting\n") Commented out by Human
                    current_process.status = "Waiting"
                    queue.append(current_process)
                else: # Human added this entire else statement
                    queue.append(current_process)
            else:
                file.write(f"Time {current_time}: Idle\n")
                current_time += 1
        file.write(f"Finished at time  {current_time}\n\n") #added from other prompt to get correct formatting
    
    calculate_metrics(processCopy, completion_times, first_execution_times, output_file)



def rr(processes, quantum, run_for, output_file):
    round_robin(processes, quantum, run_for, output_file)

def calculate_metrics(processes, completion_times, first_execution_times, output_file):
    with open(output_file, 'a') as file:
    
        for process in processes:
            completion_time = completion_times[process.name]
            first_execution_time = first_execution_times[process.name]
            wait_time = completion_time - process.arrival_time - process.execution_time
            turnaround_time = completion_time - process.arrival_time
            response_time = first_execution_time - process.arrival_time
        
            file.write(f"{process.name} wait\t {wait_time} turnaround\t {turnaround_time} response\t {response_time}\n")

    #return output


def parse_input(input_file):
    processes = []
    data = {}
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip().split()
            if line[0] == 'process':
                name = line[2]
                arrival = int(line[4])
                burst = int(line[6])
                processes.append(Process(name, arrival, burst))
            elif line[0] == 'processcount':
                data['process_count'] = int(line[1])
            elif line[0] == 'runfor':
                data['run_for'] = int(line[1])
            elif line[0] == 'use':
                data['scheduling_algorithm'] = line[1]
                if line[1] == 'rr':
                    data['quantum'] = int(file.readline().strip().split()[1])
    data['processes'] = processes
    return data

def write_output(output_file, data):
    with open(output_file, 'a') as file:
        file.write(f"Process Count: {data['process_count']}\n")
        file.write(f"Run For: {data['run_for']} time units\n")
        file.write(f"Using Scheduling Algorithm: {data['scheduling_algorithm']}\n")
        if data['scheduling_algorithm'] == 'rr':
            file.write(f"Quantum: {data['quantum']}\n")
        file.write("\nProcesses:\n")
        for process in data['processes']:
            file.write(str(process) + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file_name")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = input_file.replace('.in', '.out')

    data = parse_input(input_file)
    scheduling_algorithm = data['scheduling_algorithm']
    run_for = data['run_for']
    processes = data['processes']

    if scheduling_algorithm == 'fcfs':
        fcfs(processes, run_for, output_file)
    elif scheduling_algorithm == 'sjf':
        sjf(processes, run_for, output_file)
    elif scheduling_algorithm == 'rr':
        quantum = data['quantum']
        rr(processes, quantum, run_for, output_file)
    
