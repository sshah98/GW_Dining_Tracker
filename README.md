<p align="center"><img src="https://raw.githubusercontent.com/sshah98/DineMore/master/static/assets/images/dinemorelogo.ico?token=AbbsaoL7ao1dITPyAqjcwrZpm9F6vwGHks5bROPvwA%3D%3D" width="128px"><p>

<br><br>

# [DineMore](https://dinemore.herokuapp.com)



## What is DineMore

GW Students have a notorious experience with the GET App. It does not provide enough information about spending habits or when students will run out of GWorld. The App can be buggy and lack vital information. The goal of this app is to provide a web interface to access information about your GWorld.

## Features

-   Encrypted user authorizaton & user settings
-   Modern user interface
-   Graphs displaying overall spending
-   Visualizations showing percentages and other statistics
-   Predictions of when GWorld will run out
-   Map of all GWorld accepting places
-   Get data about the average amount spent per day (TODO)
-   Data about how much you spend per week (TODO)
-   Get data about places you spend the most money (TODO)
-   More to come!

## How does it work

A python program scrapes the GET website for your information using your provided username and password. This is stored in a postgresql database along with your login information. 

A Flask application with a web interface allows the user to interact with the information retrieved from the database

## Where can I access the App

Please go to the main page [here](https://dinemore.herokuapp.com/)

## Setup

    git clone https://github.com/sshah98/DineMore
    cd DineMore
    pip install -r requirements.txt

comment heroku lines in `spending.py`

    export DATABASE_URL="postgresql://user:password@localhost/database"
    python app.py

## Contributing

Please take a look at the [contributing](https://github.com/sshah98/DineMore/blob/master/CONTRIBUTING.md) guidelines if you're interested in helping!
