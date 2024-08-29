@echo off

setlocal

pushd %~dp0

if not exist dist call build.bat

call .venv\Scripts\python.exe -m bilidown %*

popd
