#!/usr/bin/env python3

import subprocess
import sys

required_packages = [
    'numpy', 're', 'math', 'textstat'
]

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    print("Checking and installing required packages for PRUFIA...")
    for pkg in required_packages:
        try:
            __import__(pkg)
            print(f"✅ {pkg} already installed.")
        except ImportError:
            print(f"📦 Installing {pkg}...")
            install(pkg)
    print("\n✅ All dependencies are installed. You can now run PRUFIA extractor, batch runner, and echo matching modules.")

if __name__ == "__main__":
    main()
