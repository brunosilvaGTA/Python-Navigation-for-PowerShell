import subprocess, os
from function import PowerShellCommands

def run(cmd, current_dir):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, cwd=current_dir)
    if completed.returncode != 0:
        print(f"\n An error occurred: {completed.stderr.strip()}")
    else:
        print(f"\n{completed.stdout.strip()}")
    return completed

if __name__ == '__main__':
    exe = PowerShellCommands()
    directory = os.getcwd()
    while True:
        try:
            choice = int(input("Select your action. \n 1. Listar elementos na pasta. \n 2. Ver configurações de IP. \n 3. Ver políticas de execução.\n 4. Ver diretório atual.\n 5. Voltar uma pasta\n 6. Sair\n"))
            match choice:
                case 1:
                    run(exe.listar(), directory)
                case 2: 
                    run(exe.ipconfig(), directory)
                case 3:
                    run(exe.executionpolicy(), directory)
                case 4:
                    print(f"Current dir: {directory}")
                case 5:
                    run(exe.previous_dir(), directory)
                    print(f"Current Altered dir: {directory}")
                case 6:
                    break
            print("----------------------------------")
        except Exception as err:
            print("Something went wrong", err)