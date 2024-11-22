@echo off
setlocal ENABLEEXTENSIONS
echo.
echo Gathering results...
echo =====================================
:: (c) Pourya Gohari 2023
echo.

set part=Part1 Part2 Part3
set level=0-Easy 1-Medium 2-Hard
set l=0-Easy
set length=4 6 8 10 12 14
set length_extended=8 10 12 14 16 18

(for %%p in (%part%) do ( 
   echo %%p Started...
    if %%p==Part2 (
        (for %%l in (%level%) do (
                echo  level: %%l
               (for %%e in (%length_extended%) do (
                echo  length: %%e
                md "%~dp0results\%%p\%%l\%%e"
                for /l %%x in (1, 1, 5) do (
                        copy "%~dp0inputs\%%p\%%l\%%e\%%x_config.txt" "%~dp0config.txt"
                        copy "%~dp0inputs\%%p\%%l\%%e\%%x_mission.txt" "%~dp0mission.txt"
                        main.exe
                        move "%~dp0output.txt" "%~dp0results\%%p\%%l\%%e\%%x_output.txt"
                        del "%~dp0mission.txt"
                        del "%~dp0config.txt"
                    )))
        ))
    ) else (
        (for %%l in (%level%) do (
                echo  level: %%l
               (for %%e in (%length%) do (
                echo  length: %%e
                md "%~dp0results\%%p\%%l\%%e"
                for /l %%x in (1, 1, 5) do (
                        copy "%~dp0inputs\%%p\%%l\%%e\%%x_config.txt" "%~dp0config.txt"
                        copy "%~dp0inputs\%%p\%%l\%%e\%%x_mission.txt" "%~dp0mission.txt"
                        main.exe
                        move "%~dp0output.txt" "%~dp0results\%%p\%%l\%%e\%%x_output.txt"
                        del "%~dp0mission.txt"
                        del "%~dp0config.txt"
                    )))
        ))
    )

))

echo.
echo DONE!
