#Make python exe file

# My python installation is messed up, so I needed to provide
# the full path to the pyinstaller executable, should be able to
# just use pyinstaller.exe if your python installation is correct

# OR update the path below with your path

C:\Users\eggsb\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\pyinstaller.exe networkScript.py

# Remove existing items in destination directory
Remove-Item -Path "NetworkService\PythonScripts\*" -Recurse -Force

# Copy contents
Copy-Item -Path "dist\networkScript\*" -Destination "NetworkService\PythonScripts\" -Recurse

# Remove build and dist directories
Remove-Item -Path "build" -Recurse -Force
Remove-Item -Path "dist" -Recurse -Force

# Remove the spec file
Remove-Item -Path "networkScript.spec" -Force