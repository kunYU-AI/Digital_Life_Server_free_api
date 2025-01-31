@echo off
set SCRIPT_NAME=SocketServer_free_api.py
set STREAM=False
set CHARACTER=paimon
set MODEL=gpt-3.5-turbo
set APIKEY=输入自己免费的API KEY
set URL=输入HOST的地址 https://api.chatanywhere.tech/v1

.\venv\Scripts\python.exe %SCRIPT_NAME% --stream %STREAM% --character %CHARACTER% --model %MODEL% --APIKey %APIKEY% --url %URL% --proxy %PROXY%
