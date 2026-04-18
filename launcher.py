import os
import sys

# Launcher to run the assistant
if __name__ == "__main__":
    print("🚀 Launching SARA Assistant...")
    # Defaulting to terminal mode, but can be changed to UI
    os.system("python main.py " + " ".join(sys.argv[1:]))
