# GW Dining Tracker

### Visit the website [here](https://diningapp-stage.herokuapp.com/)

## Background

GW Students have a notorious experience with the GET App. It does not provide enough information about spending habits or when students will run out of GWorld. The App can be buggy and lack vital information.

## What is GW Dining Tracker

The goal of this app is to proide a web interface to access information about your GWorld. Some examples include:

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
