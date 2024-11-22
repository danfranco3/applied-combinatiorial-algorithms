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
del "%~dp0final_result.csv"
(for %%p in (%part%) do ( 
   echo %%p Started...
    (for %%l in (%level%) do (
            echo  level: %%l
            if %%p==Part2 (
               (for %%e in (%length_extended%) do (
                echo  length: %%e
                for /l %%x in (1, 1, 5) do (
                        copy "%~dp0inputs\%%p\%%l\%%e\%%x_config.txt" "%~dp0config.txt"
                        copy "%~dp0inputs\%%p\%%l\%%e\%%x_mission.txt" "%~dp0mission.txt"
                        copy "%~dp0results\%%p\%%l\%%e\%%x_output.txt" "%~dp0output.txt"
                        ::::::::::::::::::::::::::::
                                python ./sanity_check.py
                                python ./write_csv.py
                        ::::::::::::::::::::::::::::
                        del "%~dp0mission.txt"
                        del "%~dp0config.txt"
                        del "%~dp0output.txt"
                        del "%~dp0result.txt"
                    )))
            )else (
                    (for %%e in (%length%) do (
                        echo  length: %%e
                        for /l %%x in (1, 1, 5) do (
                                copy "%~dp0inputs\%%p\%%l\%%e\%%x_config.txt" "%~dp0config.txt"
                                copy "%~dp0inputs\%%p\%%l\%%e\%%x_mission.txt" "%~dp0mission.txt"
                                copy "%~dp0results\%%p\%%l\%%e\%%x_output.txt" "%~dp0output.txt"
                                ::::::::::::::::::::::::::::
                                        python ./sanity_check.py
                                        python ./write_csv.py
                                ::::::::::::::::::::::::::::
                                del "%~dp0mission.txt"
                                del "%~dp0config.txt"
                                del "%~dp0output.txt"
                                del "%~dp0result.txt"
                            )))
                    )
    ))

))

echo.
echo DONE!
