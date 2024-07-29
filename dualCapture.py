import subprocess
import time
import os

# Define the paths to your scripts
script1_path = "photoCapture.py"
script2_path = "pupilEyetracker.py"

# Define the names of your Anaconda environments
env1_name = "Nao"  # Python 2.7 environment
env2_name = "pupil"   # Latest Python environment

def run_script_in_env(env_name, script_path):
    """
    Run a Python script in a specific Anaconda environment.
    """
    command = f"conda run -n {env_name} python {script_path}"
    process = subprocess.Popen(command, shell=True)
    return process

def main():
    # Start the first script in the Python 2.7 environment
    print(f"Running {script1_path} in environment {env1_name}...")
    process1 = run_script_in_env(env1_name, script1_path)
    
    # Give the first script a moment to start
    # time.sleep(2)
    
    # Start the second script in the latest Python environment
    print(f"Running {script2_path} in environment {env2_name}...")
    process2 = run_script_in_env(env2_name, script2_path)
    
    # Wait for both processes to complete
    process1.wait()
    process2.wait()

if __name__ == "__main__":
    main()
