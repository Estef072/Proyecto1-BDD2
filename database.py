from pymongo import MongoClient
import certifi

MONGO_URI = 'mongodb+srv://estef072:michi123@cluster0.ymu2we0.mongodb.net/?retryWrites=true&w=majority'
ca = certifi.where()

##coneccion para la base de datoss 

def dbConection():
    try:
        client =MongoClient(MONGO_URI,tlsCAFile=ca)
        db= client["prueba"]
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

    return db