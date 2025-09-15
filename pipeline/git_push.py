import sys
import subprocess

commit_message = sys.argv[1]

commands = [
    # Clean old build artifacts
    "rm -rf build quantra.egg-info dist/",
    
    # Rebuild package
    "python setup.py sdist bdist_wheel",
    
    # Git add/commit/push
    "git add .",
    f'git commit -m "{commit_message}"',
    "git push",
    
    # Reinstall library from GitHub (SSH instead of HTTPS)
    "pip uninstall -y quantra",
    "pip install 'git+ssh://git@github.com/ufuk-altan-ivtera/quantra.git'"
]

for cmd in commands:
    print(f"→ Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"✗ Command failed: {cmd}")
        sys.exit(result.returncode)
