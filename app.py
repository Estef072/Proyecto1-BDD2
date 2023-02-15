from flask import Flask, render_template, request,Response,jsonify, redirect,url_for
import database as dbase
from recipes import Recipes

db = dbase.dbConection()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bdd_add.html')
def add():
    recipes = db['recipe_prueba']
    recipesReceived = recipes.find()
    return render_template('bdd_add.html',recipes =recipesReceived )

@app.route('/bdd_edit_delete.html')
def edit_delete():
    recipes = db['recipe_prueba']
    recipesReceived = recipes.find()
    return render_template('bdd_edit_delete.html',recipes =recipesReceived )

@app.route('/bdd_filter.html')
def filter():
    return render_template('bdd_filter.html')

##method Post
@app.route('/recipes', methods=['POST'])
def addRecipe():
    # Creando colección si en dado caso no existe
    recipes = db['recipe_prueba']
    Name = request.form['Name']
    url = request.form['url']
    Description = request.form['Description']
    Author = request.form['Author']
    Ingredients = request.form.getlist('Ingredients')
    Method = request.form.getlist('Method')

    if Name and url and Description and Author and Ingredients and Method:
        receta = Recipes(Name, url, Description, Author, Ingredients, Method)
        ##guardando los datos 
        recipes.insert_one(receta.toDBcollection())
        reponse = jsonify({
            'Name': Name,
            'url': url,
            'Description': Description,
            'Author': Author,
            'Ingredients': Ingredients,
            'Method': Method
        })
        return redirect(url_for('add'))
    else:
        return notFound()

# Filter by name
@app.route('/filter_recipe.html', methods=['GET'])
def filterRecipes():
    recipes = db['recipe_prueba']

    # Realizar la consulta a la base de datos
    recipess = list(recipes.aggregate([{"$sort": {"Name": 1}}]))
    # Renderizar una plantilla HTML con los resultados de la consulta
    return render_template('filter_recipe.html', recipes = recipess)

# Filter by name 10
@app.route('/filter_recipe10.html', methods=['GET'])
def limit10():
    recipes = db['recipe_prueba']

    # Realizar la consulta a la base de datos
    pipeline = [
        {"$sort": {"Name": 1}},
        {"$limit": 10}
    ]
    recipess = list(recipes.aggregate(pipeline))

    # Renderizar una plantilla HTML con los resultados de la consulta
    return render_template('filter_recipe10.html', recipes = recipess)

# Filter by name 50
@app.route('/filter_recipe50.html', methods=['GET'])
def limit50():
    recipes = db['recipe_prueba']

    # Realizar la consulta a la base de datos
    pipeline = [
        {"$sort": {"Name": 1}},
        {"$limit": 50}
    ]
    recipess = list(recipes.aggregate(pipeline))

    # Renderizar una plantilla HTML con los resultados de la consulta
    return render_template('filter_recipe50.html', recipes = recipess)

# Filter by name 10
@app.route('/filter_ing10.html', methods=['GET'])
def limit10I():
    recipes = db['recipe_prueba']

    # Realizar la consulta a la base de datos
    pipeline = [
        {"$sort": {"Ingredients": 1}},
        {"$limit": 10}
    ]
    recipess = list(recipes.aggregate(pipeline))

    # Renderizar una plantilla HTML con los resultados de la consulta
    return render_template('filter_ing10.html', recipes = recipess)

# Filter by name 50
@app.route('/filter_ing50.html', methods=['GET'])
def limit50I():
    recipes = db['recipe_prueba']

    # Realizar la consulta a la base de datos
    pipeline = [
        {"$sort": {"Ingredients": 1}},
        {"$limit": 50}
    ]
    recipess = list(recipes.aggregate(pipeline))

    # Renderizar una plantilla HTML con los resultados de la consulta
    return render_template('filter_ing50.html', recipes = recipess)

# Filter by ingredient
@app.route('/filter_ing.html', methods=['GET'])
def filterIng():
    recipes = db['recipe_prueba']

    # Realizar la consulta a la base de datos
    recipess = list(recipes.aggregate([{"$sort": {"Ingredients": 1}}]))
    # Renderizar una plantilla HTML con los resultados de la consulta
    return render_template('filter_ing.html', recipes = recipess)

@app.route("/avg_ing.html")
def authors_with_few_recipes():
    recipes = db['recipe_prueba']
    pipeline = [
        { '$group': { '_id': '$Author', 'count': { '$sum': 1 } } },
        { '$sort': { 'count': 1 } },
        { '$limit': 20 }
    ]
    result = list(recipes.aggregate(pipeline))
    return render_template('avg_ing.html', recipes = result)

@app.errorhandler(404)
def notFound(error = None):
    message = {
        'message': 'no encontrado' + request.url,
        'status': '404 No encontrado'

    }
    response = jsonify(message)
    response.status_code= 404
    return response

##metodo para borrar recetas 
@app.route('/delete/<string:name_recipe>')

def delete (name_recipe):
    recipes = db['recipe_prueba']
    recipes.delete_one({'Name': name_recipe})
    return redirect(url_for('edit_delete'))

##metodo modify
@app.route('/edit/<string:name_recipe>', methods = ['POST'])
def edit(name_recipe):
    recipes = db['recipe_prueba']
    Name = request.form['Name']
    url = request.form['url']
    Description = request.form['Description']
    Author = request.form['Author']
    Ingredients = request.form['Ingredients']
    Method = request.form['Method']

    if  Name and url and Description and Author and Ingredients and Method:
        recipes.update_one({'Name': name_recipe}, {'$set': {          
            'Name': Name,
            'url': url,
            'Description': Description,
            'Author': Author,
            'Ingredients': Ingredients,
            'Method': Method}})
        response = jsonify({'message': 'receta' + name_recipe + 'actualizado correctamente'})
        return redirect(url_for('edit_delete'))
    else:
        return notFound()

#Ejecutarse como archivo princpal
if __name__ == '__main__':
    app.run(debug=True, port=4000)
