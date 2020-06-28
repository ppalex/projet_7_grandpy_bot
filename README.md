# Projet 7: GrandPy Robot

## Description

This project aims to develop a web application with Flask.

The user can enter a question in the text area about an address or a place.

The app will then answer with the exact address of the place and a story about
a point of interest near this area.

The app is deployed on Heroku. You can find it at: https://projet-7-grandpy.herokuapp.com/


## Language

* Python

## Requirements

Use the following command in terminal to install requirements:

```
pip install -r requirements.txt
```

## Features

* AJAX to send the question to the back-end.
* Using of Google Maps and Media Wiki API to get the information and data to display.
* The project has been developed by following a Test Driven Development methodology.
* Using of Bootstrap to make the app responsive.


## Prerequisite

You have to put a valid Google API key in the config.yml file.

Check this URL for more information: https://console.developers.google.com/

## Launch the app

* For windows user, launch the folling command:
```
set FLASK_APP=flaskr\run.py
```

* To launch the app in debug mode:
```
set FLASK_ENV=development
```

* Then launch the following command:
```
Flask run
```


## To create a test coverage report

* Launch:

```
pytest --cov=flaskr --cov-report html
```

## Attribution

Icon made by Pixel perfect from www.flaticon.com.