:: This one is needed for PythonD internaly. Most important
SET PYTHONHOME = C:/PythonD
:: To save ourselves work, we will also set up a DOS PREFIX
SET PYTHONDIR = C:\Python
:: Turn CASE sensitivity OFF under DOS, Win32 (especially without DPMI LFN driver)
SET PYTHONCASEOK=1
:: Turn off memory debugging (Optional)
SET GO32_V2_DEBUG=n
::
:: ADDITIONAL MODULES
:: for curses and terminal enabled programs -
::SET TERM=ansi.sys
:: Watt-erloo Socket support -- Should be a real dospath (needs closing `\Â´ in Wattcp 2.2 R4)
set WATTCP.CFG=%PYTHONDIR%\etc\
set ETC=%PYTHONDIR%\etc
:: DISLIN Mathematical visualization package for DJGPP
SET DISLIN=%PYTHONDIR%\etc\dislin
:: MESA - OpenGL - needed for MMX CPU opts. Factor of 8 (only 8 for NT)
set DMESA_GLUT_BPP=8 
:: DXE - location for system libraries. Note the UNIX convention used now!
SET LD_LIBRARY_PATH=%PYTHONHOME%/lib

set PATH=C:\PYTHOND\BIN\PYTHON;C:\VIM\VIM73;C:\TP\BIN;C:\TOOLS
