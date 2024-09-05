from app import create_app
from app.extensions import mongo
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app()

@app.route('/')
def index():
    return "hello world"

if __name__ == '__main__': 
    mongo.init_app(app, os.getenv("MONGODB_URI"))
    app.run(debug= True if os.getenv("ENV", "development") != "production" else False, port=os.getenv("PORT", 8000))