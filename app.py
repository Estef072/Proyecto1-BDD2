from flask import Flask, render_template, request,Response,jsonify, redirect,url_for
import database as dbase
from recetas import Recipes

db = dbase.dbConection()

app = Flask(__name__)

@app.route('/')
def home():
    recipes = db['recipe_prueba']
    recipesReceived = recipes.find()
    return render_template('index.html',recipes =recipesReceived )

##metod Post
@app.route('/recetas', methods=['POST'])
def addRecipe():
    # Creando colección si en dado caso no existe
    recipes = db['recipe_prueba']
    Name = request.form['Name']
    url = request.form['url']
    Description = request.form['Description']
    Author = request.form['Author']
    Ingredients = request.form['Ingredients']
    Method = request.form['Method']

    if Name and url and Description and Author and Ingredients and Method:
        receta = Recipes(Name,url,Description,Author,Ingredients,Method)
        ##guardando los datos 
        recipes.insert_one(receta.toDBcollection())
        reponse = jsonify({
            'Name':Name,
            'url':url,
            'Description':Description,
            'Author':Author,
            'Ingredients':Ingredients,
            'Method':Method
        })
        return redirect(url_for('home'))
    else:
        return notFound()
    

@app.errorhandler(404)
def notFound(error = None):
    message = {
        'message': 'no encontrado'+request.url,
        'status': '404 No encontrado'

    }
    response = jsonify(message)
    response.status_code= 404
    return response

##metodo para borrar recetas 
@app.route('/delete/<string:name_recipe>')

def delete (name_recipe):
    recipes= db['recipe_prueba']
    recipes.delete_one({'Name':name_recipe})
    return redirect(url_for('home'))


##metodo modify
@app.route('/edit/<string:name_recipe>',methods=['POST'])
def edit(name_recipe):
    recipes = db['recipe_prueba']
    Name = request.form['Name']
    url = request.form['url']
    Description = request.form['Description']
    Author = request.form['Author']
    Ingredients = request.form['Ingredients']
    Method = request.form['Method']

    if  Name and url and Description and Author and Ingredients and Method:
        recipes.update_one({'Name':name_recipe},{'$set':{          
            'Name':Name,
            'url':url,
            'Description':Description,
            'Author':Author,
            'Ingredients':Ingredients,
            'Method':Method}})
        response = jsonify({'message':'receta'+name_recipe + 'actualizado correctamente'})
        return redirect(url_for('home'))
    else:
        return notFound()


#Ejecutarse como archivo princpal
if __name__ == '__main__':
    app.run(debug=True, port=4000)