class Process:
    def __init__(self, name, arrival_time, execution_time, status="Pending"):
        self.name = name
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.remaining_time = execution_time
        self.status = status

    def __str__(self):
        return f"Process '{self.name}' | Arrival Time: {self.arrival_time} | Execution Time: {self.execution_time} | Status: {self.status}"

def round_robin(processes, quantum, run_for):
    first_execution_times = {}
    completion_times = {}
    current_time = 0
    queue = []
    while current_time < run_for: # had to remove  or queue or processes
        # Move processes from the original list to the queue as their arrival times are reached
        for process in processes:
            if process.arrival_time == current_time:
                print(f"Time {current_time}: {process.name} Arrived")
                queue.append(process)
                processes.remove(process)

        if queue:
            current_process = queue.pop(0)
            if current_process.name not in first_execution_times:
                first_execution_times[current_process.name] = current_time
            print(f"Time {current_time}: {current_process.name} Selected (Burst {min(quantum, current_process.remaining_time)})")
            current_process.status = "Running"
            burst_time = min(quantum, current_process.remaining_time)
            current_process.remaining_time -= burst_time
            for _ in range(burst_time):
                current_time += 1
                # Move processes from the original list to the queue as their arrival times are reached
                for process in processes:
                    if process.arrival_time == current_time:
                        print(f"Time {current_time}: {process.name} Arrived")
                        queue.append(process)
                        processes.remove(process)
            if current_process.remaining_time == 0:
                print(f"Time {current_time}: {current_process.name} Finished")
                current_process.status = "Finished"
                completion_times[current_process.name] = current_time
            elif queue: # Human changed from else to elif queue:
                print(f"Time {current_time}: {current_process.name} Waiting")
                current_process.status = "Waiting"
                queue.append(current_process)
            else: # Human added this entire else statement
                queue.append(current_process)
        else:
            print(f"Time {current_time}: Idle")
            current_time += 1

    return first_execution_times, completion_times

def calculate_metrics(processes, completion_times, first_execution_times):
    output = ""
    
    for process in processes:
        completion_time = completion_times[process.name]
        first_execution_time = first_execution_times[process.name]
        wait_time = completion_time - process.arrival_time - process.execution_time
        turnaround_time = completion_time - process.arrival_time
        response_time = first_execution_time - process.arrival_time
        
        output += f"{process.name} wait ({wait_time}) turnaround ({turnaround_time}) response ({response_time})\n"

    return output

# Example usage:
if __name__ == "__main__":
    processes = [Process("A", 0, 7), Process("B", 1, 4), Process("C", 2, 3)]
    quantum = 1
    run_for = 20

    print("Example Output:")
    first_execution_times, completion_times = round_robin(processes.copy(), quantum, run_for)
    print(calculate_metrics(processes, completion_times, first_execution_times))