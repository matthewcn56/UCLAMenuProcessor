import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import firebase_admin.db
from time import ctime, time
from menuScraper import get_menu_items_from_time_and_hall
from hallHours import get_hall_hours_from_meal_time_and_hall

mealTimes = ["Breakfast", "Brunch", "Lunch", "Dinner", "LateNight"]
halls = ["Covel", "DeNeve", "FeastAtRieber", "BruinPlate"]

cred =credentials.Certificate(YOUR_JSON_KEYFILE_PATH)

default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': YOUR_FIREBASE_URL
})
print(default_app.name)

def hall_path_switcher(pathName):
    translatedPath = {
        "Covel" : "Covel",
        "DeNeve" : "De Neve",
        "FeastAtRieber" : "Feast",
        "BruinPlate" : "BPlate"
    }
    return translatedPath.get(pathName, "ERROR")

def hours_path_switcher(pathName):
    translatedPath = {
        "Covel" : "Covel",
        "DeNeve" : "De Neve",
        "FeastAtRieber" : "FEAST at Rieber",
        "BruinPlate" : "Bruin Plate"
    }
    return translatedPath.get(pathName, "ERROR")



for mealTime in mealTimes:
    for designatedHall in halls:
        MEAL_TIME = mealTime
        DESIGNATED_HALL = designatedHall
        menuItems = get_menu_items_from_time_and_hall(MEAL_TIME, DESIGNATED_HALL)
        openHours = get_hall_hours_from_meal_time_and_hall(MEAL_TIME, hours_path_switcher(DESIGNATED_HALL))
        # #delete previous menu
        firebase_admin.db.reference("menus/" + hall_path_switcher(DESIGNATED_HALL) + "/" + MEAL_TIME).delete()
        #delete previous hours
        firebase_admin.db.reference("hours/" + hall_path_switcher(DESIGNATED_HALL) + "/" +MEAL_TIME).delete()

        #update the hours
        hoursPath = firebase_admin.db.reference("hours/" + hall_path_switcher(DESIGNATED_HALL) +"/" + MEAL_TIME)
        if openHours is None:
            hoursPath.delete()
        else:
            hoursPath.set(openHours)
        if hoursPath.get() == "":
            hoursPath.delete()

        #add new menu items
        for menuItem in menuItems:
            #taking care of invalid tokens
            for c in ["/", "-", "#", "$", "[", "]", "."]:
                menuItem["itemName"]=  menuItem["itemName"].replace(c, "")
            try:  
                path = firebase_admin.db.reference("menus/" +  hall_path_switcher(DESIGNATED_HALL) + "/" + MEAL_TIME + "/"
                +menuItem["itemName"])
                path.set(menuItem["recipeLink"])
            except ValueError:
                print("Invalid Path!")
            except TypeError:
                print("Invalid Path!")
            except firebase_admin.exceptions.FirebaseError:
                print("Invalid Path!")
       
            firebase_admin.db.reference("menus/" + DESIGNATED_HALL + "/" + MEAL_TIME + "/"
            +menuItem["itemName"]).set(menuItem["recipeLink"])
        

