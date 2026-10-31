@echo off
title Campus Lost and Found Management System - Web Portal
echo =========================================================================
echo    CAMPUS LOST AND FOUND MANAGEMENT SYSTEM - WEB APPLICATION
echo    VIT - BCSE302L Database Systems Review III Project
echo    Student: Arahat Gaikwad (Reg No: 24BYB0182)
echo =========================================================================
echo.
echo Launching Web Server and opening browser...
cd /d "%~dp0"
python run_web_app.py
pause
