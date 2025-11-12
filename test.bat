@echo off
echo ========================================
echo Testing correct config:
echo ========================================
call :run_test config.csv
echo.

echo ========================================
echo Testing package name error:
echo ========================================
call :run_test test_package_name.csv
echo.

echo ========================================
echo Testing repository URL error:
echo ========================================
call :run_test test_repository_url.csv
echo.

echo ========================================
echo Testing test mode error:
echo ========================================
call :run_test test_test_mode.csv
echo.

echo ========================================
echo Testing version error:
echo ========================================
call :run_test test_version.csv
echo.

echo ========================================
echo Testing output file error:
echo ========================================
call :run_test test_output_file.csv
echo.

echo ========================================
echo Testing ascii mode error:
echo ========================================
call :run_test test_ascii_mode.csv
echo.

echo ========================================
echo Testing max depth error:
echo ========================================
call :run_test test_max_depth.csv
echo.

echo All tests completed.
pause
exit /b

:run_test
echo Running test with file: %1
python config1.py %1
if errorlevel 1 (
    echo Test completed with errors (as expected)
) else (
    echo Test completed successfully
)
exit /b