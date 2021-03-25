# UCLAMenuProcessor
Make yourself hungry by looking at #1 Dorm Food in US's menus, created via webscraper. (Part of LAHacks 2021 Submission)

# How To Use?
During COVID-19 when UCLA's Dining Halls are unopened, use the wayback machine as shown to find past dining hall menu items.  
Normally, simply remove the "https://web.archive.org/web/" part of the URL to grab the current day's menu items!  
Inside of the get_menu_items_from_time_and_hall function, pass in  
your designated meal time ("Breakfast", "Brunch", "Lunch", "Dinner", "LateNight")  
and the specified Dining Hall, ("Covel", "DeNeve", "FeastAtRieber", "BruinPlate")
to return the Hall's Menu Items as a python dictionary, grabbing each entry's name through ["itemName"] and a link to its nutrition facts through  ["recipeLink"]. 




databaseUpdating.py showcases the general structure you can use to update a NoSQL database of choice's values with the daily menu items (my example uses firebase)
