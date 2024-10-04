import sys
from subprocess import run

commit_message = sys.argv[1]

commands_list = [
                # Remove Folders
                'rm -r build quantra.egg-info dist/ && ', 
                
                # Recreate folders
                'python setup.py sdist bdist_wheel && ',
                
                # Add into commit
                'git add . && ', 
                
                # Commit
                f'git commit -m"{commit_message}" && ',
                
                # Push Changes
                'git push && ',
                
                # Uninstall Library
                'pip uninstall quantra -y && ',
                
                # Reinstall Library
                "pip install 'git+https://ufuk.altan.ivtera@gitlab.com/library3921439/quantra.git' && "
                
                ]



string = ""
for command in commands_list:
    
    command_string = command
    string += command_string

string = string[:-4]
run(string , shell=True)
                                                                                                                        