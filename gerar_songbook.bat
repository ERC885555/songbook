@echo off
REM Vai para a pasta raiz do projeto
cd /d %~dp0

REM Ativa o ambiente virtual
call venv\Scripts\activate

REM Roda o script principal
python -m src.main

REM Mantém a janela aberta para ver as mensagens
pause