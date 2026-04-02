import os
import subprocess
import time
from difflib import SequenceMatcher

# Directories to search
SEARCH_DIRS = [
    os.path.join(os.path.expanduser("~"), "Desktop"),
    os.path.join(os.path.expanduser("~"), "Documents"),
    os.path.join(os.path.dirname(__file__), "..", "projects")
]

def smart_search(query, memory=None):
    """Searches for a file or folder matching the query across key directories."""
    query = query.lower()
    candidates = []
    
    for root_dir in SEARCH_DIRS:
        if not os.path.exists(root_dir): continue
        
        # Limit depth to 3 for performance
        base_depth = root_dir.count(os.sep)
        for root, dirs, files in os.walk(root_dir):
            if root.count(os.sep) - base_depth > 3:
                continue
                
            for item in dirs + files:
                full_path = os.path.join(root, item)
                name = item.lower()
                
                # Scoring
                score = SequenceMatcher(None, query, name).ratio()
                
                # Context Boost: Check if this file was recently mentioned in memory
                if memory and query in name:
                    score += 0.2
                    
                if score > 0.6: # Threshold
                    candidates.append({"path": full_path, "name": item, "score": score})
                    
    # Sort by score descending
    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[:5] # Return top 5

def open_file_safe(path):
    """Opens a file with the default system application."""
    try:
        os.startfile(path)
        return f"Opening {os.path.basename(path)}."
    except Exception as e:
        return f"Failed to open file: {e}"

def delete_to_recycle_bin(path):
    """Moves a file or folder to the Recycle Bin via Windows PowerShell."""
    try:
        # Resolve absolute path for PowerShell
        abs_path = os.path.abspath(path).replace("'", "''") # Escape single quotes
        
        # Use Microsoft.VisualBasic.FileIO.FileSystem for a native Recycle Bin move
        cmd = f'powershell -Command "Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile(\'{abs_path}\', \'OnlyErrorDialogs\', \'SendToRecycleBin\')"'
        
        # If it's a directory
        if os.path.isdir(path):
            cmd = f'powershell -Command "Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory(\'{abs_path}\', \'OnlyErrorDialogs\', \'SendToRecycleBin\')"'
            
        subprocess.run(cmd, shell=True, check=True)
        return f"Successfully moved {os.path.basename(path)} to the Recycle Bin."
    except Exception as e:
        return f"Failed to delete file safely: {e}"

def rename_file(old_path, new_name):
    """Renames a file or folder."""
    try:
        directory = os.path.dirname(old_path)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
        return f"Renamed to {new_name}."
    except Exception as e:
        return f"Rename failed: {e}"

def create_directory(name, parent_dir=None):
    """Creates a new folder."""
    try:
        if not parent_dir:
            parent_dir = SEARCH_DIRS[0] # Default to Desktop
            
        path = os.path.join(parent_dir, name)
        os.makedirs(path, exist_ok=True)
        return f"Created folder '{name}' at {parent_dir}."
    except Exception as e:
        return f"Folder creation failed: {e}"
