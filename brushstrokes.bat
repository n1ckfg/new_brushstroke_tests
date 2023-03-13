@echo off

cd %~dp0
python brushstrokes_from_mesh.py -- %1

@pause