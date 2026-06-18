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
        return f'Get-ADOrganizationalUnit -Filter \'Name -like "*{name_like}*"\' | Select-Object Name, DistinguishedName'
    def get_forest(self):
        return "Get-ADForest"
        
    