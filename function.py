import os

class PowerShellCommands:
    def __init__(self, dir=None):
        self.dir = dir if dir else os.getcwd()
    def listar(self):
        return "Get-ChildItem"
    def ipconfig(self):
        return "ipconfig"
    def executionpolicy(self):
        return "Get-ExecutionPolicy"
    def previous_dir(self):
        return "cd.."
    def get_module(self):
        return "Get-Module -ListAvailable"
    def import_module(self):
        return "Import-Module ActiveDirectory"
    def disabled_users(self):
        return "Search-ADAccount -AccountDisabled | select name"
    def find_path(self, name_like=None):
        if name_like is None:
            name_like = input("Enter the name of the file or folder you want to find: ")
        # O Out-String -Width 500 garante uma linha única gigante para cada resultado
        return f'Get-ADOrganizationalUnit -Filter \'Name -like "*{name_like}*"\' | Select-Object Name, DistinguishedName | Out-String -Width 500'
    def verify_empty_fields(self, path=None):
        if path is None:
            path = input("Enter the path of the folder you want to check: ")
        # Corrigido: Adicionado ';' após a variável e removida a aspa dupla extra no final.
        # Adicionado: '| Format-List' no final para o caminho/e-mails não virem cortados.
        return f'$CaminhoDaPasta = "{path}"; Get-ADUser -Filter "mailNickname -notlike \'*\'" -SearchBase $CaminhoDaPasta -Properties mail, mailNickname, proxyAddresses, ObjectGUID | Select-Object Name, UserPrincipalName, mail, mailNickname, @{{Name="ObjectGUID";Expression={{$_.ObjectGUID.ToString()}}}}, @{{Name="ProxyAddresses";Expression={{$_.proxyAddresses -join \'; \'}}}} | Format-List'
    def get_forest(self):
        return "Get-ADForest"
        
    