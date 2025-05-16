import importlib
import subprocess
import sys

def ensure_pip():
    try:
        import pip
        print("pip is already installed.")
        return True
    except ImportError:
        print("pip not found. Trying to bootstrap pip...")
        try:
            import ensurepip
            ensurepip.bootstrap()
            print("pip installed successfully.")
            return True
        except ImportError:
            print("Failed to install pip automatically. Please install pip manually.")
            return False

def install_package(package_name):
    print(f"Installing '{package_name}'...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"Installed '{package_name}' successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install '{package_name}'. Error: {e}")
        sys.exit(1)

def install_if_missing(package_name):
    try:
        importlib.import_module(package_name)
        print(f"'{package_name}' is already installed.")
    except ImportError:
        install_package(package_name)

if __name__ == "__main__":
    if ensure_pip():
        for pkg in ["numpy", "gudhi", "pygame"]:
            install_if_missing(pkg)
    else:
        sys.exit(1)
    from interactive import *
    from filtrations import *
    run_window()

