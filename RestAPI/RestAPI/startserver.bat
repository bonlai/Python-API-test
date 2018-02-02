cd env\Scripts
call activate.bat
start http://localhost:8000/
cd ../../
python manage.py runserver 0.0.0.0:8000
pause