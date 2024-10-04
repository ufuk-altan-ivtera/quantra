import sys
from subprocess import run

commands_list = [
                # Create Conda Environment
                'conda create -n "cmt" python=3.10.8 && ', 
                
                # Activate Environment
                'conda activate cmt && ',

                # Install commerciante
                "pip install 'git+https://UfukAltanUA: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@github.com/UfukAltanUA/commerciante.git' && "
                
                # Install Requirements
                'pip install -r requirements.txt && ',
                
                # Add Environment into Jupyter Kernel
                'python -m ipykernel install --user --name=CMT && ',
                
                
                ]



string = ""
for command in commands_list:
    
    command_string = command
    string += command_string

string = string[:-4]
run(string , shell=True)
                                                                                                                        