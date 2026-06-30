from importlib.resources import path
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
        return f'Get-ADOrganizationalUnit -Filter \'Name -like "*{name_like}*"\' | Select-Object Name, DistinguishedName | Out-String -Width 500'
    
    def verify_empty_fields(self, path=None):
        if path is None:
            path = input("Enter the path of the folder you want to check: ")
        return f'$CaminhoDaPasta = "{path}"; Get-ADUser -Filter "mailNickname -notlike \'*\'" -SearchBase $CaminhoDaPasta -Properties mail, mailNickname, proxyAddresses, ObjectGUID | Select-Object Name, UserPrincipalName, mail, mailNickname, @{{Name="ObjectGUID";Expression={{$_.ObjectGUID.ToString()}}}}, @{{Name="ProxyAddresses";Expression={{$_.proxyAddresses -join \'; \'}}}} | Format-List'
    
    def get_forest(self):
        return "Get-ADForest | Out-String -Width 500"
    
    def mailbox_status(self, path=None):
        if path is None:
            path = input("Enter the path of the folder you want to check: ")
        return f'$CaminhoDaPasta = "{path}"; Get-ADUser -Filter * -SearchBase $CaminhoDaPasta -Properties mail, mailNickname, msExchRemoteRecipientType, msExchUserAccountControl | Select-Object Name, mail, mailNickname, @{{Name="RemoteRecipientType";Expression={{$_.msExchRemoteRecipientType}}}}, @{{Name="ExchangeAccountControl";Expression={{$_.msExchUserAccountControl}}}}'
    
    def mailbox_empty(self, path=None):
        if path is None:
            path = input("Enter path: ")
        return f'$CaminhoDaPasta = "{path}"; Get-ADUser -Filter "msExchUserAccountControl -notlike \'*\'" -SearchBase $CaminhoDaPasta -Properties mail, mailNickname, msExchRemoteRecipientType, msExchUserAccountControl | Select-Object Name, UserPrincipalName, mail, mailNickname, @{{Name="RemoteRecipientType";Expression={{$_.msExchRemoteRecipientType}}}}, @{{Name="ExchangeAccountControl";Expression={{$_.msExchUserAccountControl}}}}'
    
    def return_objetcs(self, path=None):
        if path is None:
            path = input("Enter path: ")
        return f'$CaminhoDaPasta = "{path}"; Get-ADObject -Filter "ObjectClass -eq \'user\' -or ObjectClass -eq \'group\' " -SearchBase $CaminhoDaPasta -Properties ObjectClass, Name | Select-Object Name, ObjectClass | Format-Table -AutoSize'
    
    def return_members(self, group=None):
        if group is None:
            group = input("Enter group name: ")
        return f'Get-ADGroup -Filter "Name -like \'*{group}*\'" | ForEach-Object {{ $NomeGrupo = $_.Name; Get-ADGroupMember -Identity $_.DistinguishedName | ForEach-Object {{ $Membro = $_; $AdObj = Get-ADObject -Identity $Membro.DistinguishedName -Properties Enabled; [PSCustomObject]@{{ Grupo = $NomeGrupo; Membro = $Membro.Name; Tipo = $Membro.objectClass; Status = if ($AdObj.Enabled -eq $false) {{ "Inactive" }} else {{ "Active" }} }} }} }} | Format-Table -AutoSize'
    
    def get_all_members_of_all_groups(self, path=None):
        if path is None:
            path = input("Enter Path: ")
        return f'$CaminhoDaOU = "{path}"; Get-ADGroup -Filter * -SearchBase $CaminhoDaOU | ForEach-Object {{ $NomeGrupo = $_.Name; Get-ADGroupMember -Identity $_.DistinguishedName | ForEach-Object {{ $Membro = $_; $AdObj = Get-ADObject -Identity $Membro.DistinguishedName -Properties Enabled; [PSCustomObject]@{{ Grupo = $NomeGrupo; Membro = $Membro.Name; Tipo = $Membro.objectClass; Status = if ($AdObj.Enabled -eq $false) {{ "Inactive" }} else {{ "Active" }} }} }} }} | Format-Table -AutoSize'
    
    def get_empty_groups(self, path=None):
        if path is None:
            path = input("Enter Path: ")
        return f'$CaminhoDaOU = "{path}"; Get-ADGroup -Filter "member -notlike \'*\'" -SearchBase $CaminhoDaOU -Properties member, GroupScope, GroupCategory | Select-Object Name, GroupScope, GroupCategory | Format-Table -AutoSize >> GruposSemMembros.txt'
    def return_users_without_groups(self, path=None):
        if path is None:
            path = input("Enter Path: ")
        return f'$CaminhoDaOU = "{path}"; Get-ADUser -Filter "MemberOf -notlike \'*\'" -SearchBase $CaminhoDaOU -SearchScope Subtree -Properties MemberOf, Enabled | Select-Object Name, UserPrincipalName, @{{Name="Status";Expression={{if ($_.Enabled) {{ "Active" }} else {{ "Inactive" }} }} }} | Format-Table -AutoSize >> UsuariosSemGrupo.txt'
    def return_groups_with_disabled_users(self, path=None):
        if path is None:
            path = input("Enter the path of the folder (OU DistinguishedName) to scan: ")
        
        # 1. Substituído Get-ADGroupMember por $_.member para evitar o limite de 5000 itens.
        # 2. Processamento direto dos membros para evitar o timeout de enumeração inválida.
        return f'$CaminhoDaOU = "{path}"; Get-ADGroup -Filter * -SearchBase $CaminhoDaOU -Properties member | ForEach-Object {{ $NomeGrupo = $_.Name; $_.member | ForEach-Object {{ $MembroDN = $_; $User = Get-ADUser -Identity $MembroDN -ErrorAction SilentlyContinue; if ($User -and $User.Enabled -eq $false) {{ [PSCustomObject]@{{ Grupo = $NomeGrupo; UsuarioDesabilitado = $User.Name }} }} }} }} | Format-Table -AutoSize >> UsuariosIntrusos.txt'