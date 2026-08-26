from importlib.resources import path
import os, json, subprocess

class PowerShellCommands:
    def __init__(self, dir=None):
        self.dir = dir if dir else os.getcwd()
    
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
    
    def return_objetcs2(self, path=None):
            if path is None:
                path = input("Enter path: ")
            return f'$CaminhoDaPasta = "{path}"; Get-ADObject -Filter "ObjectClass -eq \'user\' -or ObjectClass -eq \'group\' " -SearchBase $CaminhoDaPasta -Properties ObjectClass, Name | Select-Object Name | Format-Table -AutoSize >> Terminais.txt'
    
    def return_members(self, group=None):
        if group is None:
            group = input("Enter group name: ")
        return f'Get-ADGroup -Filter "Name -like \'*{group}*\'" | ForEach-Object {{ $NomeGrupo = $_.Name; Get-ADGroupMember -Identity $_.DistinguishedName | ForEach-Object {{ $Membro = $_; $AdObj = Get-ADObject -Identity $Membro.DistinguishedName -Properties Enabled; [PSCustomObject]@{{ Grupo = $NomeGrupo; Membro = $Membro.Name; Tipo = $Membro.objectClass; Status = if ($AdObj.Enabled -eq $false) {{ "Inactive" }} else {{ "Active" }} }} }} }} | Format-Table -AutoSize'
    
    def get_all_members_of_all_groups(self, path=None):
        if path is None:
            path = input("Enter Path: ")        
        return f'$CaminhoDaOU = "{path}"; Get-ADGroup -Filter * -SearchBase $CaminhoDaOU -Properties member | ForEach-Object {{ $NomeGrupo = $_.Name; $_.member | ForEach-Object {{ $MembroDN = $_; $User = Get-ADUser -Identity $MembroDN -ErrorAction SilentlyContinue; if ($User) {{ [PSCustomObject]@{{ Grupo = $NomeGrupo; Membro = $User.Name; Tipo = "user"; Status = $User.Enabled.ToString().Replace("True","Active").Replace("False","Inactive") }} }} }} }} | Format-Table -AutoSize'
    
    def get_empty_groups(self, path=None):
        if path is None:
            path = input("Enter Path: ")
        return f'$CaminhoDaOU = "{path}"; Get-ADGroup -Filter "member -notlike \'*\'" -SearchBase $CaminhoDaOU -Properties member, GroupScope, GroupCategory | Select-Object Name, GroupScope, GroupCategory | Format-Table -AutoSize'
    
    def return_users_without_groups(self, path=None):
        if path is None:
            path = input("Enter Path: ")
        return f'$CaminhoDaOU = "{path}"; Get-ADUser -Filter "MemberOf -notlike \'*\'" -SearchBase $CaminhoDaOU -SearchScope Subtree -Properties MemberOf, Enabled | Select-Object Name, UserPrincipalName, @{{Name="Status";Expression={{if ($_.Enabled) {{ "Active" }} else {{ "Inactive" }} }} }} | Format-Table -AutoSize'
    
    def return_groups_with_disabled_users(self, path=None):
        if path is None:
            path = input("Enter Path: ")    
        return f'$CaminhoDaOU = "{path}"; Get-ADGroup -Filter * -SearchBase $CaminhoDaOU -Properties member | ForEach-Object {{ $NomeGrupo = $_.Name; $_.member | ForEach-Object {{ $MembroDN = $_; $User = Get-ADUser -Identity $MembroDN -ErrorAction SilentlyContinue; if ($User -and $User.Enabled -eq $false) {{ [PSCustomObject]@{{ Grupo = $NomeGrupo; UsuarioDesabilitado = $User.Name }} }} }} }} | Format-Table -AutoSize'
    
    def return_inactive_active_users(self, path=None, days=90):
        if path is None:
            path = input("Enter Path: ")
        return f'$Corte = (Get-Date).AddDays(-{days}); $CaminhoDaOU = "{path}"; Get-ADUser -Filter "Enabled -eq \'$true\'" -SearchBase $CaminhoDaOU -SearchScope Subtree -Properties LastLogonDate | Where-Object {{ $_.LastLogonDate -lt $Corte -or $null -eq $_.LastLogonDate }} | Select-Object Name, UserPrincipalName, @{{Name="UltimoLogon";Expression={{ if ($_.LastLogonDate) {{ $_.LastLogonDate.ToString("dd/MM/yyyy") }} else {{ "NUNCA LOGOU" }} }} }} | Format-Table -AutoSize'
    
    def return_user_groups(self, user=None):
        if user is None:
            user = input("Digite o Nome, E-mail ou Login do usuário: ")
        return f'$UsuarioInput = "{user}"; $User = Get-ADUser -Filter "Name -like \'*$UsuarioInput*\' -or UserPrincipalName -like \'*$UsuarioInput*\' -or SamAccountName -like \'*$UsuarioInput*\'" -Properties MemberOf, Enabled | Select-Object -First 1; if ($User) {{ $Status = if ($User.Enabled) {{ "Active" }} else {{ "Inactive" }}; Write-Host "`n=========================================="; Write-Host "USUARIO: $($User.Name) | STATUS: $Status"; Write-Host "=========================================="; if ($User.MemberOf) {{ $User.MemberOf | ForEach-Object {{ $GroupDN = $_; (Get-ADGroup -Identity $GroupDN).Name }} | ForEach-Object {{ [PSCustomObject]@{{ Grupo = $_ }} }} | Format-Table -AutoSize }} else {{ Write-Host "Usuário não pertence a nenhum grupo." }} }} else {{ Write-Host "Usuario não encontrado no AD." }}'
    
    def get_users_office_location(self, file_path=None):
        if file_path is None:
            file_path = 'relatório_fevereiro.txt'
        
        # O pipe (|) foi adicionado antes do Out-File para passar os dados corretamente
        return f'$Path = "{file_path}"; if (Test-Path $Path) {{ (Get-Content $Path | ForEach-Object {{ $_.Replace(",", "").Trim() }} | Where-Object {{ $_ -ne "" }} | ForEach-Object {{ $Matricula = $_; $User = Get-ADUser -Filter "SamAccountName -eq \'$Matricula\' -or UserPrincipalName -like \'*$Matricula*\'" -Properties physicalDeliveryOfficeName | Select-Object -First 1; if ($User) {{ [PSCustomObject]@{{ Matricula = $Matricula; Nome = $User.Name; Sede = if ($User.physicalDeliveryOfficeName) {{ $User.physicalDeliveryOfficeName }} else {{ "NAO INFORMADO" }} }} }} else {{ [PSCustomObject]@{{ Matricula = $Matricula; Nome = "NAO ENCONTRADO"; Sede = "N/A" }} }} }} | Format-Table -AutoSize) | Out-File -FilePath "levantamento_fevereiro.txt" -Encoding utf8; Write-Host "Processamento concluido! Salvo em localidades.txt" }} else {{ Write-Host "Arquivo $Path nao encontrado no diretório atual." }}'
    
    def get_mac_from_file(self, input_file=None, output_file="resultado_macs.txt"):
        if input_file is None:
            input_file = input("Digite o caminho do arquivo TXT com a lista de computadores: ")
        
        full_input_path = os.path.join(self.dir, input_file).replace("\\", "/")
        full_output_path = os.path.join(self.dir, output_file).replace("\\", "/")
            
        return (
            f'$InputFile = "{full_input_path}"; '
            f'$OutputFile = "{full_output_path}"; '
            f'if (Test-Path $InputFile) {{ '
                f'(Get-Content $InputFile | Where-Object {{ $_.Trim() -ne "" }} | ForEach-Object {{ '
                    # Conversao forçada e explicita para String e remoçao de caracteres nulos ou especiais de quebra de linha
                    f'$ComputerName = [string]$_.Trim().Replace("`r", "").Replace("`n", ""); '
                    f'try {{ '
                        # Resolve o IP garantindo que a saída seja uma string pura do IPAddress
                        f'$DNS = Resolve-DnsName -Name $ComputerName -Type A -ErrorAction Stop | Select-Object -First 1; '
                        f'$IP = [string]$DNS.IPAddress; '
                        
                        # Ping utilizando parametro universal de compatibilidade (-ComputerName)
                        f'$null = Test-Connection -ComputerName $IP -Count 1 -Quiet -ErrorAction SilentlyContinue; '
                        
                        # Consulta do MAC com tempo de respiro para o ARP
                        f'Start-Sleep -Milliseconds 50; '
                        f'$Neighbor = Get-NetNeighbor -IPAddress $IP -ErrorAction SilentlyContinue | Select-Object -First 1; '
                        
                        f'[PSCustomObject]@{{ '
                            f'ComputerName = $ComputerName; '
                            f'IPAddress    = $IP; '
                            f'MACAddress   = if ($Neighbor.LinkLayerAddress) {{ $Neighbor.LinkLayerAddress }} else {{ "Sem resposta no ARP" }} '
                        f'}} '
                    f'}} catch {{ '
                        f'[PSCustomObject]@{{ '
                            f'ComputerName = $ComputerName; '
                            f'IPAddress    = "Falha DNS"; '
                            f'MACAddress   = "N/A" '
                        f'}} '
                    f'}} '
                f'}} | Format-Table -AutoSize) | Out-File -FilePath $OutputFile -Encoding utf8; '
                f'Write-Host "Processamento concluido! Resultado salvo em: $OutputFile"'
            f'}} else {{ '
                f'Write-Host "Arquivo $InputFile nao encontrado."'
            f'}}'
        )