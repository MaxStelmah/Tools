@echo off
chcp 861>nul
sc query SecurityHealthService > "D:\Tools\svc cheker\Files\resSecur.txt"