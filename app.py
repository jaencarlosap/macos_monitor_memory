import subprocess
import time

def get_memory_usage():
    # Command to get the process information
    command = "ps aux | awk '{print $11, $4, $6/1024}' | grep -v COMMAND"
    # Execute the command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    # Check for errors
    if process.returncode != 0:
        print(f"Error executing command: {stderr}")
        return {}, {}

    mem = {}
    mem_mb = {}

    # Process the output
    for line in stdout.strip().split('\n'):
        parts = line.split()
        if len(parts) < 3:
            continue
        app_name = parts[0]
        memory_usage_percent = float(parts[1])
        memory_usage_mb = float(parts[2])

        if app_name not in mem:
            mem[app_name] = 0
            mem_mb[app_name] = 0
        mem[app_name] += memory_usage_percent
        mem_mb[app_name] += memory_usage_mb

    return mem, mem_mb

def print_table(mem, mem_mb, max_name_length=50):
    # Create a list of tuples for easy sorting and formatting
    data = [(name, mem[name], mem_mb[name]) for name in mem]
    data.sort(key=lambda x: x[1], reverse=True)  # Sort by Memory Usage (%)

    # Clear previous output and print the table header
    print("\033c", end="")  # ANSI escape sequence to clear the console
    print(f"{'Application Name':<{max_name_length}} {'Memory Usage (%)':<20} {'Memory Usage (MB)':<20}")
    print("=" * (max_name_length + 60))  # Adjust the line length according to the headers

    # Print each row of data
    for app_name, mem_usage, mem_usage_mb in data:
        # Truncate app_name if it's too long
        truncated_name = app_name[:max_name_length - 2] + '...' if len(app_name) > max_name_length else app_name
        print(f"{truncated_name:<{max_name_length}} {mem_usage:<20.2f} {mem_usage_mb:<20.2f}")

def main():
    try:
        while True:
            mem, mem_mb = get_memory_usage()
            print_table(mem, mem_mb)
            time.sleep(2)  # Update every 2 seconds
    except KeyboardInterrupt:
        print("\nMemory monitoring stopped.")

if __name__ == "__main__":
    main()
