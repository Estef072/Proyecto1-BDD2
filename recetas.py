class Recipes:
    def __init__(self,id,name,url,description,autor,ingredients,method):
        self.id= id
        self.name=name
        self.url=url
        self.description=description
        self.autor=autor
        self.ingredients=ingredients
        self.method =method
    def toDBcollection(self):
        return{
            'id': self.id,
            'name':self.name,
            'url':self.url,
            'description':self.description,
            'autor': self.autor,
            'ingredients':self.ingredients,
            'method':self.method
        }
            

        