import subprocess

# Path to your executables
exe1 = "actuator.exe"
# exe2 = "./actuator2.exe"

# Run the executables in parallel
process1 = subprocess.run(exe1)
# process2 = subprocess.Popen([exe2])