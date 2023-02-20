@echo off
cls
:start
REM 將程式碼推上 Heroku
set PATH=%PATH%;"C:\Program Files\Git\cmd"
cd C:\Users\adamenius\Downloads\line-bot-tutorial-master

set /P commit_msg=Input your commit message:
call git add .
call git commit -m "%commit_msg%"
call git push -f heroku main
pause
goto start