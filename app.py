from flask import Flask, render_template
 
app = Flask(__name__)
 
# dados dos personagens (a página usa um {% for %} pra montar os cards)
PERSONAGENS = [
    {
        "nome": "Manny Ribera",
        "descricao": "Amigo e parceiro de Tony durante grande parte da história. "
                     "Com ele, Tony compartilha momentos de lealdade, amizade e também de tragédias.",
    },
    {
        "nome": "Frank Lopez",
        "descricao": "Um dos primeiros chefes de Tony no mundo do crime e uma "
                     "figura importante para a ascensão do personagem.",
    },
    {
        "nome": "Elvira Hancock",
        "descricao": "Personagem que passa a fazer parte da vida de Tony após "
                     "diversos conflitos e que acaba se tornando sua esposa.",
    },
    {
        "nome": "Alejandro Sosa",
        "descricao": "Um poderoso traficante de drogas que possui uma relação "
                     "importante com Tony durante o desenvolvimento da história.",
    },
]
 
 
@app.route("/")
def index():
    return render_template("index.html")
 
 
@app.route("/tony")
def tony():
    return render_template("tony.html")
 
 
@app.route("/enredo")
def enredo():
    return render_template("enredo.html")
 
 
@app.route("/personagens")
def personagens():
    return render_template("personagens.html", personagens=PERSONAGENS)
 
 
if __name__ == "__main__":
    app.run(debug=True)