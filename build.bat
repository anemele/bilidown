@echo off

pushd %~dp0client
call npm run build-only
popd

echo *>dist\.gitignore