import subprocess, os, ctypes, sys
from function import PowerShellCommands

def run(cmd, current_dir):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True,encoding="utf-8", errors="replace", cwd=current_dir)
    if completed.returncode != 0:
        print(f"\n An error occurred: {completed.stderr.strip()}")
    else:
        print(f"\n{completed.stdout.strip()}")
    return completed

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def request_admin_privilegies():
    try: 
        result = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None,1
        )
        return result > 32
    except Exception as err:
        print(f"Error: {err}")
        return False
if not is_admin():
    sucess = request_admin_privilegies()
    if sucess:
        print("Request admin privilegies. Relaunching...")
    else:
        print("Admin privilegie request was denied.")
        sys.exit()
else:
    print("Running without privilegies...")
    subprocess.run("net session", shell=True)

if __name__ == '__main__':
    exe = PowerShellCommands()
    directory = os.getcwd()
    while True:
        try:
            print("Select your action:")
            #print("1. Listar elementos na pasta.")
            #print("2. Ver configurações de IP.")
            #print("3. Ver políticas de execução.")
            #print("4. Ver diretório atual.")
            #print("5. Voltar uma pasta")
            print("1. Ver listas de módulos disponíveis.")
            print("2. Importar módulo ActiveDirectory.")
            print("3. Encontrar um caminho específico.(path)")
            print("4. Listar florestas do AD")
            print("5. Retornar usuários com campos vazios.(precisa de path)")
            print("6. Verificar status de caixa de correio.(precisa de path)")
            print("7. Ver usuários fantasmas.(precisa de path)")
            print("8. Ver objetos em uma pasta.(precisa de path)")
            print("9. Ver membros de um grupo")
            print("10. Sair")
            choice = int(input(" "))
            match choice:
                case 1:
                    run(exe.get_module(), directory)
                case 2:
                    run(exe.import_module(), directory)
                case 3:
                    run(exe.find_path(), directory)
                case 4:
                    run(exe.get_forest(), directory)
                case 5:                    
                    run(exe.verify_empty_fields(), directory)
                case 6:                    
                    run(exe.mailbox_status(), directory)
                case 7:
                    run(exe.mailbox_empty(), directory)  
                case 8:
                    run(exe.return_objetcs(), directory)
                case 9: 
                    run(exe.return_members(), directory)
                case 10:
                    break
            print("----------------------------------")
        except Exception as err:
            print("Something went wrong", err)