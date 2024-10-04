import sys
from subprocess import run

commands_list = [
                # Create Conda Environment
                'conda create -n "qnt" python=3.10.8 -y && ', 
                
                # Activate Environment
                'conda activate qnt && ',

                # Install commerciante
                "pip install 'git+https://ufuk-altan-ivtera@bitbucket.org/library-ivtera/quantra.git' && "
                
                # Install Requirements
                'pip install -r requirements.txt && ',
                
                # Add Environment into Jupyter Kernel
                'python -m ipykernel install --user --name=QNT && ',
                
                
                ]



string = ""
for command in commands_list:
    
    command_string = command
    string += command_string

string = string[:-4]
run(string , shell=True)
                                                                                                                        