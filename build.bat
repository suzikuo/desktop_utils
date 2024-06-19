@echo off
call .\.env\Scripts\activate
pyinstaller .\MyTools.spec
