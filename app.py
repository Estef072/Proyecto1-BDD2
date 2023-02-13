from flask import Flask, render_template, request
#import database as dbase
#from recetas import Recipes

#db = dbase.dbConnection()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/recetas', methods=['POST'])
# def addRecipe():
    # Creando colección si en dado caso no existe
    #recipes = db['recipes']
    #id = request.form['id'] 

#Ejecutarse como archivo princpal
if __name__ == '__main__':
    app.run(debug=True, port=4000)