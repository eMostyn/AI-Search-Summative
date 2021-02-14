@echo off
cls
Set Sleep=0
:start
if %Sleep% == 30 ( goto end )
py ACOElitist.py AISearchFile535.txt
echo This is a loop
Set /A Sleep+=1
echo %Sleep%
goto start
:end
echo "am 30 now"
pause