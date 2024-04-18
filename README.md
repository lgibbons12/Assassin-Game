# Cannon 007

This is the django web application for the Cannon 007 Senior game. The game consists of seniors
targeting other seniors and eliminating them with golden knives until one remains.

This documentation provides an overview of the entire codebase for this project along with recommended 
hotspots of where to go when problems arise and how different files work in conjunction with each other.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Folder Structure](#folder-structure)
5. [Files](#files)
   - [settings.py](#settingspy)
   - [apps.py](#appspy)
   - [urls.py](#urlspy)
   - [views.py](#viewspy)
   - [models.py](#modelspy)
   - [game.py](#gamespy)
   - [stats.py](#statspy)
   - [templates/](#templates)
   - [static/](#static)
6. [Contributing](#contributing)

## Project Overview

This django project consists of a single app (users) which handles all relevant information and processing for the web app.
Users handles the players (which login using the Google API) with a SQLite3 database, and the information for all the pages
is handled on the backend through the python files, which is sent to the frontend which is supported with the templates
and static directories. There is also a tests directory which houses the tests that I used throughout the development
process to ensure the game was working as expected.

## Installation

This project is currently housed at [Cannon 007](http://www.cannon007.com) which itself is hosted through PythonAnywhere. The domain is 
handled under GoDaddy, which is then CNamed into the project. To install and work on this project yourself, here is how you do it.

1. Make a new home directory and set up a python virtual environment in it
2. Git clone this repository into that directory
3. Run "pip install -r requirements.txt" in terminal to collect packages
4. Navigate to the directory "Assassin-Game" and run "python manage.py runserver" to ensure everything is working correctly
5. Code to your heart's content!


## Usage

### From Actual Website

Under the Cannon 007 site, you can make changes to the game through the admin page, please contact the owner
of this repository if you do not have admin access to get approved. Through the admin page, you can
make changes to the database and all the models that reside within it

### From the Code

Make any code changes that you want, and run "python manage.py runserver" to run a local server of the website
to test those changes. If making changes to models or settings.py, run "python manage.py makemigrations" and 
then "python manage.py migrate"

If wanting to push changes to the repository, please submit a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)

## Folder Structure

`Assassin-Game` holds all relevant code to the game:
- `algo.py` and `grouping.py` hold test python files that I used to figure out the feasability of new features
- `requirements.txt` holds the current versions of all packages used in the project
- `README.md` is what you are reading right now
- `db.sqlite3` is the database that holds all current information on models
- `manage.py` is the django out-of-the-box command line toolkit that should not require any editing
- `assassin` contains website-wide files like `settings.py`
- `users` contains all information on the users app 

## Files

### `settings.py`

This file holds all the settings that the server uses to set up the Django website.
Let's go through the important information in here

- SITE_ID: This is an abstract constant that tells the code which of the sites stored in the database is currently being used, if there is a problem with the website not loading, trying numbers between 1-10 could help
- INSTALLED_APPS: This holds all django based apps that are used in the project
- JAZZMIN_SETTINGS: This holds all the settings for the Jazzmin updated admin page
- SOCIALACCOUNT_PROVIDERS: Allows the website to access the Google API
- STATIC_URL: Points the website to where the static files are held

### `apps.py`

This file sets up the users app so that we can use its associated code in the project

### `urls.py`

There are 2 `urls.py` files. One in the assassin directory and one in the users directory

1. `assassin`: This controls how urls and formatted across the app, so all admin urls start with "admin/", while the users app has no path which allows all of its urls to not need an initial path

2. `users`: This controls the flow of urls throughout the users app. The first part of each path is the link that users see, the second part consists of the view in `views.py` that the code will be directed to, and the third part shows what the path is called so different functions can access that page.

### `views.py`

This is one of the most important files in the repository. It holds the backend python processing for each page in the website. The file is formatted so each page is its own python function with the form:

`def "page name"(request):`

In each view, whatever python processing you want to occur happens, and then the views create "contexts" filled with python variables which are then sent to the frontend templates with the return render() call

The views consist of:

1. Home: The first page users see which uses StatManager to show up to date stats, allow users to login via Google, and see their assignment

2. Assigment Direction: This is a "ghost-page" that isn't viewable by the user but instead handles backend information and redirects the user to another page. When the user clicks on the "See Assignment" button from the homepage, this file determines whether to send them to the single-player or group assignment page along with doing a check on all checkers

3. Group Assignment: This page gets information on the players group and then shows relevant information to the user using templates.

4. Assignment: Very similar to group assignment except for single-player games.

5. Placement: This page is how players are able to create teams for group games. It allows players to create a team with a new name if they are not in one, and handles search functionality within the page.

6. Logout: Self-explanatory

7. Submit Complaint: Directs to html file

8. Rules: Uses rule model to display up-to-date rules of the game

9. Handling: Function users are sent to in single-player games after they click a button on the assignment page. Handles backend checking and player eliminating when actions are performed

10. Group Handling: handling but for group games


### `models.py`

This file sets up each model that is used to store information in the SQLite3 database. These models are used mainly in the `views.py` and `game.py` to store and retrieve information across pages.

The models consist of:

- Custom User: This is an extension of each player's google profile that sets up a full name for them that can be used throughout the web app

- Player: This is the model that houses information for every player. It contains functions to eliminate themselves and to handle when they have eliminated their target. The reciever at the bottom creates a player model for a user whenever they sign up.

- Checker: The checker model handles checking for all eliminations. Each checker has a "target" and a "killer" and it saves whether both have confirmed the elimination. Once they have, the "checking" function handles all backend code to eliminate the player and set up a new target

- AgentGroup: This model oversees the groups for the groups game. If includes a `ManyToManyField` which allows it to have a list of the Player models in the group. It can set a group target, but eliminations in group games are still handled by the Player models

- Game: This model keeps track of whether the current game is a single-player or group game

- Rule: This model keeps track of the rules to show on the rules page

### `game.py`

This file is not a django-specific file, rather it is a module I created to house `GameManager`, a catch-all class with many functions that can be used in the game. It contains checking functions such as `player_on_team`, `is_group_game`, `is_placing_groups`, and `win_condition` that files such as `views.py` can access to get current game states. The rest of `game.py` deals with targeting, with functions that assign players and groups new targets based on who their target was targeting, and functions that assign targets at the start of games using for loops.

### `stats.py`

This file is similar in its modular nature to `game.py`, but its primary function is to return statistics that are displayed on the home page of the site.

### `templates/`

The `templates/` directory houses all of the HTML files in use in the project. The HTML files present the code in a way browsers can understand. They format all the data handled on the backend with the `.py` files so that it can be displayed to the user. 

There are three subdirectories that are important to mention

- `admin` has templates that modulate the base admin templates that come out of the box with django
- `socialaccount` has templates that change the base sign-in and sign-up templates that come out of the box with django's package `allauth`
- `users` holds the html files that serve data from the python views listed above

### `static/`

The `static/` directory stores static files such as CSS and images to be served in the project.

## Contributing

Thank you for reading to the end! If you would like to contribute, follow the installation functions above and submit a pull request when you are done!

If you have any questions, please use this [contact form](https://forms.gle/gn8xsvcP5Mtt8Kud9)


