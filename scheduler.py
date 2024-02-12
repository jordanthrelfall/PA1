import sys

def fcfs(processes):
    pass

def sjf(processes):
    pass

def rr(processes, quantum):
    pass

def parse_input(input_file):
    data = {}
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip().split()
            if line[0] == 'process':
                name = line[2]
                arrival = int(line[4])
                burst = int(line[6])
                data[name] = {'arrival': arrival, 'burst': burst}
            elif line[0] == 'processcount':
                data['process_count'] = int(line[1])
            elif line[0] == 'runfor':
                data['run_for'] = int(line[1])
            elif line[0] == 'use':
                data['scheduling_algorithm'] = line[1]
                if line[1] == 'rr':
                    data['quantum'] = int(file.readline().strip().split()[1])
    return data

def write_output(output_file, data):
    with open(output_file, 'w') as file:
        file.write(f"Process Count: {data['process_count']}\n")
        file.write(f"Run For: {data['run_for']} time units\n")
        file.write(f"Using Scheduling Algorithm: {data['scheduling_algorithm']}\n")
        if data['scheduling_algorithm'] == 'rr':
            file.write(f"Quantum: {data['quantum']}\n")
        file.write("\nProcesses:\n")
        for process, info in data.items():
            if isinstance(info, dict) and 'arrival' in info and 'burst' in info:
                file.write(f"Name: {process[6:]}, Arrival Time: {info['arrival']}, Burst Time: {info['burst']}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file_name")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = input_file.replace('.in', '.out')

    data = parse_input(input_file)
    scheduling_algorithm = data['scheduling_algorithm']
    processes = list(data.values())[3:-2]  # Extracting processes from data

    if scheduling_algorithm == 'fcfs':
        fcfs(processes)
    elif scheduling_algorithm == 'sjf':
        sjf(processes)
    elif scheduling_algorithm == 'rr':
        quantum = data['quantum']
        rr(processes, quantum)

    write_output(output_file, data)
