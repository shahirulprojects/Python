# guide to python virtual environments
"""
virtual environments in python are isolated environments that allow you to:
- install packages without affecting other projects
- maintain different versions of the same package
- keep your global python installation clean
- share project dependencies easily
"""

# here's how to work with virtual environments:

"""
1. creating a virtual environment:
   
   # using venv (built into python)
   python -m venv myenv
   
   # using virtualenv (needs to be installed)
   pip install virtualenv
   virtualenv myenv

2. activating the virtual environment:
   
   # windows
   myenv\Scripts\activate
   
   # unix/macos
   source myenv/bin/activate
   
   # deactivating
   deactivate

3. managing packages:
   
   # installing packages
   pip install package_name
   
   # installing from requirements.txt
   pip install -r requirements.txt
   
   # listing installed packages
   pip list
   
   # generating requirements.txt
   pip freeze > requirements.txt

4. project structure with virtual environment:
   
   myproject/
   ├── myenv/              # virtual environment
   ├── src/                # source code
   ├── tests/              # test files
   ├── requirements.txt    # project dependencies
   └── README.md          # project documentation
"""

# example script to demonstrate virtual environment usage
import sys
import pkg_resources

def get_python_info():
    """get information about the python environment."""
    return {
        "python_version": sys.version,
        "python_path": sys.executable,
        "virtual_env": sys.prefix != sys.base_prefix
    }

def list_installed_packages():
    """list all installed packages and their versions."""
    return [
        f"{pkg.key} {pkg.version}"
        for pkg in pkg_resources.working_set
    ]

def main():
    """main function to display environment information."""
    # get python information
    info = get_python_info()
    
    print("python environment information:")
    print("-" * 30)
    print(f"python version: {info['python_version'].split()[0]}")
    print(f"python path: {info['python_path']}")
    print(f"using virtual environment: {info['virtual_env']}")
    
    # list installed packages
    print("\ninstalled packages:")
    print("-" * 30)
    for package in list_installed_packages():
        print(package)

# best practices for virtual environments:
"""
1. always create a virtual environment for each project
2. never commit virtual environment to version control
3. always include requirements.txt in your project
4. document any specific setup steps in README.md
5. use .gitignore to exclude virtual environment:

   # .gitignore
   myenv/
   venv/
   .env/
   *.pyc
   __pycache__/
"""

# common virtual environment tools:
"""
1. venv: built-in python module for creating virtual environments
2. virtualenv: more features than venv, supports older python versions
3. pipenv: combines pip and virtualenv, provides dependency resolution
4. conda: package and environment management, popular in data science
5. poetry: modern dependency management and packaging
"""

# troubleshooting virtual environments:
"""
1. activation not working:
   - check if virtual environment is created correctly
   - verify activation script path
   - try creating a new environment

2. package installation fails:
   - check internet connection
   - verify package name and version
   - update pip: pip install --upgrade pip
   - check for conflicts: pip check

3. multiple python versions:
   - specify python version when creating environment:
     python3.8 -m venv myenv
   - use pyenv for managing multiple python versions

4. path issues:
   - check system PATH variable
   - verify virtual environment bin/scripts directory
   - ensure correct python interpreter is being used
"""

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a script that:
#    - creates a virtual environment
#    - installs required packages
#    - runs a test script
#    - generates requirements.txt

# 2. create a project that:
#    - uses multiple python versions
#    - manages dependencies with poetry
#    - includes development dependencies
#    - provides setup documentation

# 3. create a deployment script that:
#    - sets up virtual environment
#    - installs production dependencies
#    - runs tests
#    - prepares for deployment

# example solution for #1:
"""
import os
import subprocess
import sys
from pathlib import Path

def setup_project():
    # create project directory
    project_dir = Path("myproject")
    project_dir.mkdir(exist_ok=True)
    os.chdir(project_dir)
    
    # create virtual environment
    subprocess.run([sys.executable, "-m", "venv", "venv"])
    
    # activate virtual environment
    if sys.platform == "win32":
        activate_script = "venv\\Scripts\\activate"
    else:
        activate_script = "venv/bin/activate"
    
    # create requirements.txt
    with open("requirements.txt", "w") as f:
        f.write("requests>=2.26.0\\n")
        f.write("pytest>=6.2.5\\n")
    
    # create test script
    with open("test_script.py", "w") as f:
        f.write("import requests\\n")
        f.write("def test_request():\\n")
        f.write("    response = requests.get('https://python.org')\\n")
        f.write("    assert response.status_code == 200\\n")
    
    print("project setup complete!")
    print(f"to activate: source {activate_script}")
    print("then run: pip install -r requirements.txt")

if __name__ == "__main__":
    setup_project()
""" 