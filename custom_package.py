import subprocess
import sys

def install_playwright_and_upgrade_packages():
    # Install Playwright
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    
    # Install Playwright's required browsers
    subprocess.check_call([sys.executable, "-m", "playwright", "install"])
    
    # Upgrade pandas
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pandas"])
    
    # Upgrade numpy
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "numpy"])

# Example usage
install_playwright_and_upgrade_packages()
