Preserving-and-Randomizing-Data-Responses-in-Web-Application-using-Differential-Privacy

Differential Privacy is assurance over information privacy without damaging the chance of having privacy risk by including some amount of Random noise in the form of robust data to the original dataset. 

Differential Privacy is also a tool with an algorithm that helps maintain Privacy by Preserving and Randomizing data responses—measuring the accuracy of statistical data by performing analysis. To Perform this process of differential privacy, IBM developed an open-sourced algorithm called Diffprivlib[1]. With this library, the project has created a Front-End Web application that can perform data analysis that involves different mechanisms, models, and Tools.
This project is an attempt to integrate all mechanisms, models, and tools involved in DiffPrivLib. The primary purpose of this paper is to showcase the work on differential privacy that consists in developing a user-friendly web application that can be open-sourced. This application is designed in a python programming package and will experiment with the dataset to perform the analysis to show the impact of differential privacy algorithms on different values on epsilon with accuracy and Privacy.

The main scope of the work is to develop a front-end web application developed using digital technologies such as AI/ML, Cryptography, and Security. The study and experiment related to this project can help the enterprise in the following manner
1.The Web application developed for IBM's Differential Privacy library having covered mechanism, model, and tools. 
2.Application developed can perform analysis that is free and cost-effective 
3."Diffprivlib" provides an extensive collection of mechanisms, the fundamental building blocks of differential privacy that handle the addition of noise. The Parameter used to set this value is denoted as epsilon (ε) to the dataset; ε controls so much noise or randomness to a raw dataset.
4.As the application is available opensource can be utilized to perform experiments by small-size companies to high-level companies
5.Helps non-technical person or provides ease of work for a data analyst who can perform different computations and understand the data
6.Experiments were performed only on the supervised dataset. 
7.For Accountant, Data analysts can perform computations to understand if there is any Privacy Leakage.

Framework Installation

1. Installation with pip
The library is to run with Python 3. The library can be installed from the PyPi repository using pip (or pip3):

pip install diffprivlib

2. Manual installation
For the most recent version of the library, either download the source code or clone the repository in your directory of choice:
git clone https://github.com/IBM/differential-privacy-library

To install diffprivlib, do the following in the project folder (alternatively, can run python3 -m pip install.):

pip install

The library comes with a basic set of unit tests for pytest. To check your install, run all the unit tests by calling pytest in the install folder:

pytest

Supporting Libraries is installed using below given command
pip install scikit-learn
pip install numpy
	
Other config files that are required to be installed are given below
pip install flask
pip install Jinja2-2.10.3-py2.py3-none-any.whl


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

	
