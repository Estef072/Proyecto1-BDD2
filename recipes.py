class Recipes:
    def __init__(self,Name,url,Description,Author,Ingredients,Method):
        self.Name=Name
        self.url=url
        self.Description=Description
        self.Author=Author
        self.Ingredients=Ingredients
        self.Method =Method
    def toDBcollection(self):
        return{
            'Name':self.Name,
            'url':self.url,
            'Description':self.Description,
            'Author': self.Author,
            'Ingredients':self.Ingredients,
            'Method':self.Method
        }
            

        