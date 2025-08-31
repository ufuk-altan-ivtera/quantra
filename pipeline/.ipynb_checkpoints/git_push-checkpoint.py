import sys
from subprocess import run

commit_message = sys.argv[1]

commands_list = [
                # Remove Folders
                'rm -r build commerciante.egg-info dist/ && ', 
                
                # Recreate folders
                'python setup.py sdist bdist_wheel && ',
                
                # Add into commit
                'git add . && ', 
                
                # Commit
                f'git commit -m"{commit_message}" && ',
                
                # Push Changes
                'git push && ',
                
                # Uninstall Library
                'pip uninstall commerciante -y && ',
                
                # Reinstall Library
                "pip install 'git+https://UfukAltanUA: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@github.com/UfukAltanUA/commerciante.git' && "
                
                ]



string = ""
for command in commands_list:
    
    command_string = command
    string += command_string

string = string[:-4]
run(string , shell=True)
                                                                                                                        