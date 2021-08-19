System Setup:
------------------------------------------------------------------------

1. Install Python 3 (Python 3.6.0 used while development). You may find your matching distributions here: https://www.python.org/downloads/
2. While installing, choose the option to add Python to PATH
3. Download and install Python package manager - PIP. More information can be found here: https://www.w3schools.com/python/python_pip.asp
4. Then, use PIP to install below packages:
		Flask==2.0.1
		Jinja2==2.11.3
		numpy==1.19.5
		pandas==0.25.3
		scikit-learn==0.24.2
		scipy==1.5.4
	which may install other dependencies automatically. Versions might cause a bit of problem while setup in Windows. Should work great with Linux and its distributions.

5. Open Terminal/Command Prompt and type command: "python DiffPrivApplication.py". This should start the applicationserver. 
6. Open a web browser of your choice and visit: http://localhost:5000/
7. This should open the application UI.

	