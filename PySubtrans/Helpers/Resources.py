import os
import sys
import appdirs # type: ignore
from importlib import resources

old_config_dir : str = appdirs.user_config_dir("GPTSubtrans", "MachineWrapped", roaming=True)
config_dir : str = appdirs.user_config_dir("LLMSubtrans", "MachineWrapped", roaming=True)

def GetResourcePath(relative_path : str, *parts : str) -> str:
    """
    Locate a resource file or folder in the application directory or the PyInstaller bundle.
    """
    if hasattr(sys, "_MEIPASS"):
        # Running in a PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path, *parts) # type: ignore

    # Try to use importlib.resources to find package resources (needed for uvx/pip installs)
    try:
        # Get the PySubtrans package root directory
        py_subtrans_root = resources.files("PySubtrans")
        
        # Try to find resource in PySubtrans package (e.g., PySubtrans/instructions/...)
        path_parts = (relative_path,) + parts
        resource_path = py_subtrans_root.joinpath(*path_parts)
        
        try:
            if resource_path.is_file() or resource_path.is_dir():
                return str(resource_path)
        except AttributeError:
            pass
        
        # Fallback: try parent directory (for backwards compatibility)
        package_root = py_subtrans_root.parent
        resource_path = package_root.joinpath(*path_parts)
        
        try:
            if resource_path.is_file() or resource_path.is_dir():
                return str(resource_path)
        except AttributeError:
            pass
    except (ImportError, ModuleNotFoundError, FileNotFoundError):
        pass

    # Fallback to current working directory (for development mode)
    return os.path.join(os.path.abspath("."), relative_path or "", *parts)
