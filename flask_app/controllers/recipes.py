from flask_app import app, render_template, request, redirect, session
from flask_app.models.recipe import Recipe


# ! CREATE

@app.route("/recipe/new")
def recipe_new():
    # call the get all classmethod to get all friends
    return render_template("new_recipe.html")


@app.route('/handle_new_recipe', methods=['POST'])
def handle_new_recipe():
    print(request.form)
    Recipe.save(request.form)
    return redirect('/recipes')


# ! READ ONE

@app.route('/recipe/<int:id>')
def show(id):
    data = {'id': id}
    return render_template('show.html', recipe=Recipe.get_one(data))


# ! READ/RETRIEVE ALL

@app.route('/recipes')
def recipes():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('recipes.html', recipes=Recipe.get_all())


# ! UPDATE

@app.route('/edit/<int:id>')
def edit_recipe(id):
    data = {'id': id}
    return render_template('edit_recipe.html', recipe=Recipe.get_one(data))


@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    print(request.form)
    Recipe.update(request.form)
    return redirect('/recipes')


# ! DELETE

@app.route('/delete/<int:id>')
def delete_recipe(id):
    data = {'id': id}
    Recipe.destroy(data)
    return redirect('/recipes')
