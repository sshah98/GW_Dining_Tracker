# GW Dining Tracker

### Visit the website [here](https://diningapp-stage.herokuapp.com/)

## Background

GW Students have a notorious experience with the GET App. It does not provide enough information about spending habits or when students will run out of GWorld. The App can be buggy and lack vital information.

## What is GW Dining Tracker

The goal of this app is to provide a web interface to access information about your GWorld. Some examples include:

-   Graphs displaying overall spending
-   Visualizations showing percentages and other statistics (TODO)
-   Predictions of when GWorld will run out (TODO)
-   Map of all GWorld accepting places (TODO)
-   Get data about the average amount spent per day (TODO)
-   Data about how much you spend per week (TODO)
-   Get data about places you spend the most money (TODO)

-   More to come!

## How does it work

A python program scrapes the GET website for your information using your provided username and password. This is stored in a postgres database along with your login information. 

A flask app with a web interface allows the user to interact with the information retreived from the database

## Where can I access the App

Please go to the main page [here](https://diningapp-stage.herokuapp.com/)



<p align="center"><img src="https://raw.githubusercontent.com/anfederico/Flaskex/master/media/flaskex-logo.png" width="128px"><p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/python-v3.6-blue.svg)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![GitHub Issues](https://img.shields.io/github/issues/anfederico/flaskex.svg)](https://github.com/anfederico/flaskex/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ef2f8f65c67a4043a9362fa6fb4f487a)](https://www.codacy.com/app/RDCH106/Flaskex?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=RDCH106/Flaskex&amp;utm_campaign=Badge_Grade)

<br><br>

<p align="center"><img src="https://raw.githubusercontent.com/anfederico/Flaskex/master/media/flaskex-demo.png" width="100%"><p>

## Features
- Encrypted user authorizaton
- Database initialization
- New user signup
- User login/logout
- User settings
- Modern user interface
- Bulma framework
- Limited custom css/js
- Easily customizable

## Setup
``` 
git clone https://github.com/anfederico/Flaskex
cd Flaskex
pip install -r requirements.txt
python app.py
```

## Contributing
Please take a look at our [contributing](https://github.com/anfederico/Flaskex/blob/master/CONTRIBUTING.md) guidelines if you're interested in helping!
