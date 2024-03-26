so what do we still need to do

- add stats page
- add complaints page
- deploy





What I've done
- add the action performed change to checker model
- updated admin functionality
- changed number of players



now we have to fix self defense leading to multiple people having the same target
(use refresh)


/*******\

Gameplan:
- DONE: create new view that can be accessed with the home page and has similar css
- allow creation of teams on the page (search engine)
- test working of team's game
- Django admin


find some way to reset the many too many in the agent groups admin


If Time:
- Online:
-- 
-- 

\*********/


It is going to be a filter

So first time it shows up if you aren't on a team it gives you an option to make a name and create one

once you have created a team, it shows team name and current players on top

you can scroll or search for specific players divs which will have a button with their pk that says add

if add it will go to an add view that will then add thatr player to the team and reload the page

There will also be an x next to each players name on the team selection that will send to a subtract view that will take that polayer off of the team

https://www.youtube.com/watch?v=VL5ZNCjXEbw


Pretty good, just figured out how to show all the players, now search functionality should be pretty simple

Okay we have adding working. 

Things to do now
- add x's to take players off team
- write function to check if a player is on a team, return that team, or None
- only show players that are not currently on teams



CSS To Do 3/20



Automatic search update?



Don’t need borders, have columns (add button inline)

Frame that scrolls with overflow


Only activate the save button if you make a change

Play with fonts







TO-DO Now:

Be able to delete team or rename team

Admin page!\\



3/26

On to admin!!!