### About
The aim of this application is to display weather information on a kindle device.
For this project I have used a Kindle 4th generation (from year 2012) and a Raspberry Pi3 model B running the server on my local network.

The Experimental Browser is pointed to a page running on the server. This will refresh from time to time to get the latest information.
A full refresh of the page is done because doing partial refresh (i.e.: using Ajax) will create problems on the e-ink display (showing some shaddows from previously displayed info). A refresh of the entire page ensures a finer painting.


### Weather Forecast Source
I use weather.com site for information about the weather.
I do not use the API it provides as it is quite limited and needs registration for limited use.
Instead I parse the html page and extract the information I need

### Running the project
This project uses python3 and pip3.
#### Create a virtualenv
Create a virtualenv in python using the command: *virtualenv:  python3 -m venv env*
Activate the virtualenv using the command: *virtualenv: source env/bin/activate*

#### Install Dependencies
The required depedendencies are saved into [requirements.txt](requirements.txt) using *pip freeze > requirements.txt*
  To install all dependencies, run *pip install –r requirements.txt*

##### Some possible issues with dependencies
There may be an issue when running the install of dependencies from the requirements.txt file. Namely, the **pkg-resources==0.0.0** might fail to install properly. The solution is to simply comment this one and run again.

#### Run the server
- Make sure you have your virtualenv active: *source env/bin/activate*
- Run the server using *python app.py*.
- To run the server in background *nohup python app.py &*

#### Open Experimental Browser on Kindle
*Note: The server that was started at the previous step should run in a location accessible from Kindle (e.g.: local network)*
Point the Experimental Browser in Kindle to the address: **<server_address>:<server_port>/weather/now**
By default the port is **5000**.

### Deploying to Raspberry
- Run *deploy-to-raspberry.sh* to deploy the files to raspberry.
This will copy the necessary files remotely (except downloaded modules and pycache).


### Docker
A docker image is also provided in *Dockerfile*.
The script *reload-container.sh* can be run using *sudo* where the container needs to run (e.g: on raspberry). It will stop the container (if it is already running, e.g: when updating the application) and then start it again.

### User Interface
- The user interface looks 'old-style' html with tables and so on because the user interface to the user is an html page displayed in the Experimental Browser included on the Kindle. This is a very basic browser and does not support modern specs la html5, css3, etc.

### Backend
- As a server framework I use Flask.
- The entry point into the application is app.py.
