
import os
import subprocess
import time

PROJECTS_DIR = os.path.join(os.path.dirname(__file__), "..", "projects")

def create_project(project_name):
    """Creates a new project directory."""
    try:
        path = os.path.join(PROJECTS_DIR, project_name)
        if os.path.exists(path):
            return f"Project '{project_name}' already exists."
        
        os.makedirs(path, exist_ok=True)
        # Create a basic README
        with open(os.path.join(path, "README.md"), "w") as f:
            f.write(f"# {project_name}\nCreated by Sara Assistant.")
            
        return f"Created project folder '{project_name}'."
    except Exception as e:
        return f"Failed to create project: {e}"

def write_file(project_name, filename, content, overwrite=False):
    """Writes a file into a project directory."""
    try:
        project_path = os.path.join(PROJECTS_DIR, project_name)
        if not os.path.exists(project_path):
            os.makedirs(project_path, exist_ok=True)
            
        file_path = os.path.join(project_path, filename)
        
        if os.path.exists(file_path) and not overwrite:
            return f"FILE_EXISTS_ERROR: {filename} already exists in {project_name}. Specific confirmation needed to overwrite."
            
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f"Successfully wrote {filename} to {project_name}."
    except Exception as e:
        return f"Failed to write file: {e}"

def execute_code(project_name, filename):
    """Executes a script and returns the output."""
    try:
        project_path = os.path.join(PROJECTS_DIR, project_name)
        file_path = os.path.join(project_path, filename)
        
        if not os.path.exists(file_path):
            return f"Error: {filename} not found."
            
        # Basic Safety Check: Check for dangerous commands in the content (optional, or just rely on user confirm)
        # For now, we execute in a subprocess and capture output
        print(f"🚀 Running {filename} in {project_name}...")
        
        # Determine command based on extension
        cmd = ["python", filename] if filename.endswith(".py") else ["node", filename] if filename.endswith(".js") else None
        
        if not cmd:
            return "Unsupported file type for execution."
            
        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=30 # 30s timeout safety
        )
        
        output = result.stdout.strip()
        error = result.stderr.strip()
        
        if result.returncode == 0:
            return f"Execution successful. Output: {output if output else 'No output'}"
        else:
            return f"Execution failed with error: {error}"
            
    except subprocess.TimeoutExpired:
        return "Execution timed out after 30 seconds."
    except Exception as e:
        return f"Execution error: {e}"

def open_vscode(project_name):
    """Opens the project in VS Code."""
    try:
        project_path = os.path.join(PROJECTS_DIR, project_name)
        if not os.path.exists(project_path):
            return "Project directory not found."
            
        # Use shell=True for 'code' command on Windows
        subprocess.Popen(["code", "."], cwd=project_path, shell=True)
        return f"Opening '{project_name}' in VS Code."
    except Exception as e:
        return f"Failed to launch VS Code: {e}"
