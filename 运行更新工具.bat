@echo off
chcp 936 >nul
title EraTW Magic DLC Auto Updater

echo.
echo ========================================
echo   EraTW Magic DLC Auto Updater
echo   (No Git Required)
echo ========================================
echo.

python update_github_no_git.py

if errorlevel 1 (
    echo.
    echo Error: Python not found or execution failed
    echo Download: https://www.python.org/downloads/
    echo.
    pause
)
