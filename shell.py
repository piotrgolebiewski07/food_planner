from food_planner_app import app

app.app_context().push()

print("Flask context active.")
print("Available objects: db, Ingredient")

