@echo off

cd %~dp0
python contour_from_mesh.py -- %1

@pause