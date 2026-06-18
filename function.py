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
    