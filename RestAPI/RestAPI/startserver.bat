cd env\Scripts
call activate.bat
cd ../../
python manage.py runserver 0.0.0.0:8000
start http://localhost:8000/
pause