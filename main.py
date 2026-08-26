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
            print("┌──────────────────────────────────────────────────────────────┐")
            print("│              PAINEL DE AUDITORIA E GOVERNANÇA                │")
            print("└──────────────────────────────────────────────────────────────┘")
            print(" ⚙️  SISTEMA & INFRAESTRUTURA")
            print("  [01] Listar Módulos PowerShell Disponíveis")
            print("  [02] Importar Módulo Active Directory")
            print("  [03] Mapear Caminhos de Estrutura (Find Path)")
            print("  [04] Exibir Informações da Floresta AD")
            print("---")
            print(" 📧 AUDITORIA EXCHANGE & CAIXAS DE CORREIO")
            print("  [05] Identificar Contas com Campos Vazios    --> [Requer Caminho/OU]")
            print("  [06] Diagnosticar Status de Caixas Exchange  --> [Requer Caminho/OU]")
            print("  [07] Listar Contas sem Caixa Provisionada    --> [Requer Caminho/OU]")
            print("---")
            print(" 👥 GOVERNANÇA DE GRUPOS & IDENTIDADES")
            print("  [08] Listar Objetos de uma Pasta (Contas/OU)--> [Requer Caminho/OU]")
            print("  [08.2] Listar somente nomes dos Objetos de uma Pasta (Contas/OU)--> [Requer Caminho/OU]")
            print("  [09] Consultar Membros de um Grupo Específico--> [Requer Nome do Grupo]")
            print("  [10] Exportar Todos os Membros de Todos os Grupos -> [Requer Caminho/OU]")
            print("  [11] Detectar Grupos Órfãos (Sem Membros)")
            print("  [12] Localizar Usuários Avulsos (Sem Grupo)")
            print("  [13] Identificar Contas Desabilitadas em Grupos")
            print("  [14] Ver grupos de um usuário")
            print("  [15] Ver locação de usuários (Por Arquivo de Texto)")
            print("---")
            print(" 🛡️  SEGURANÇA E CONFORMIDADE")
            print("  [16] Auditar Contas Ativas sem Logon (+90 dias) -> [Requer Caminho/OU]")
            print("  [17] Encontrar endereço Mac -> [Requer Caminho/OU]")
            print("---")
            print(" ❌ [18] Sair do Sistema")
            print("────────────────────────────────────────────────────────────────")
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
                case 82:
                    run(exe.return_objetcs2(), directory)
                case 9: 
                    run(exe.return_members(), directory)
                case 10:
                    run(exe.get_all_members_of_all_groups(), directory)
                case 11:
                    run(exe.get_empty_groups(), directory)
                case 12:
                    run(exe.return_users_without_groups(), directory)
                case 13:
                    run(exe.return_groups_with_disabled_users(), directory)
                case 14: 
                    run(exe.return_user_groups(), directory)
                case 15:
                    run(exe.get_users_office_location(), directory)
                case 16:
                    run(exe.return_inactive_active_users(), directory)
                case 17:
                    run(exe.get_mac_from_file(), directory)
                case 18:
                    break
            print("----------------------------------")
        except Exception as err:
            print("Something went wrong", err)