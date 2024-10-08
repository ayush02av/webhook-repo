from app import create_app
from app.extensions import mongo
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app()

if __name__ == '__main__': 
    mongo.init_app(app, os.getenv("MONGODB_URI"))
    app.run(
        host= "0.0.0.0",
        port= os.getenv("PORT", 8000),
        debug=True,
    )