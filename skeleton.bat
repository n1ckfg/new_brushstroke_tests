@echo off

cd %~dp0
python skeleton_from_mesh.py -- %1

@pause