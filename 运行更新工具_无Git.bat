@echo off
chcp 65001 >nul
title EraTW Magic DLC 自动更新工具（无Git版本）

echo.
echo ========================================
echo   EraTW Magic DLC 自动更新工具
echo   （无需安装Git）
echo ========================================
echo.

python update_github_no_git.py

if errorlevel 1 (
    echo.
    echo 程序运行出错，请检查Python是否已安装
    echo 下载地址：https://www.python.org/downloads/
    echo.
    pause
)
