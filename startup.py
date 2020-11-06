from utilities import EelApp
from config import app_args

# Destination directory will be deleted, so ensure this is correct..
eel_app = EelApp(app_args)

# Initialize the eel app
if __name__ == '__main__':
    # needs to be imported after eel_app is initialized
    import views
    # Start the eel app
    eel_app.start()