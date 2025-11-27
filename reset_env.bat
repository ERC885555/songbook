@echo off
REM Vai para a pasta raiz do projeto
cd /d %~dp0

REM Remove o ambiente virtual antigo (se existir)
if exist venv (
    echo Apagando ambiente virtual antigo...
    powershell -Command "Remove-Item -Recurse -Force venv"
)

REM Cria um novo ambiente virtual
echo Criando novo ambiente virtual...
python -m venv venv

REM Ativa o ambiente virtual
call venv\Scripts\activate

REM Instala as dependências do requirements.txt
echo Instalando dependencias...
pip install -r requirements.txt

REM Roda o script principal para gerar os HTMLs e o index
echo Gerando songbook...
python -m src.main

echo ============================================
echo ✅ Songbook atualizado com sucesso!
echo Abra o arquivo index.html no navegador :)
echo ============================================

pause