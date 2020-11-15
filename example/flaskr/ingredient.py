import functools

from flask import Blueprint, json
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flaskr.db import get_db

bp = Blueprint("ingredient", __name__, url_prefix="/ingredient")
RATINGS = [ 'r_nourishment',
            'r_value',
            'r_human_welfare',
            'r_animal_welfare',
            'r_resource_cons',
            'r_biodiversity',
            'r_global_warming',]

@bp.route("/<str:ingredientName>", methods=("GET", "POST"))
def getIngredient():
    """Retrieve an Ingredient by name
    Returns None if Ingredient not present
    """
    if request.method == "GET":
        db = get_db()
        error = None

        if not ingredientName:
            error = "Ingredient name is required."
        else:
            ingredient = db.execute(
                "SELECT * FROM ingredient WHERE name = ?", ingredientName)
                .fetchone()
        
        if ingredient is None:
            abort(404, f"Ingredient with name {ingredientName} doesn't exist.")
        
        return ingredient


@bp.route("/<str:ingredientName>/alt", methods=("GET"))
def getAlternatives():
    """ Retrieve a list of Ingredients that may be substituted for 
    ingredientName
    """
    if request.method == "GET":
        db = get_db()
        error = None

        if not ingredientName:
            error = "Ingredient name is required."
        else:
            alternatives = db.execute(
                "SELECT * FROM ingredient WHERE category_id = "
                "(SELECT category_id FROM ingredient WHERE name = ?)", ingredientName)

        if alternatives is None:
            abort(404, f"Ingredient with name {ingredientName} has no alternatives.")
        
        return alternatives

def getAlternativesByRating(ratingName):
    """ Retrieve a list of Ingredients that may be subsituted for ingredientName 
    with a higher score on a particular ethical rating
    """
    if request.method == "GET":
        db = get_db()
        error = None

        if not ingredientName:
            error = "Ingredient name is required."
        else:
            alternatives = db.execute(
                "SELECT * FROM ingredient WHERE category_id="
                "(SELECT category_id FROM ingredient WHERE name = ?)" 
                "AND ? > (SELECT ? FROM ingredient WHERE name= ?)", 
                ingredientName, ratingName, ratingName, ingredientName)

        if alternatives is None:
            abort(
                404, f"Ingredient with name {ingredientName} has no alternatives.")

        return alternatives


def getAlternativesByRatingAvg():
    """ Retrieve a list of Ingredients that may be subsituted for ingredientName 
    with a higher average of all ratings
    """
    if request.method == "GET":
        db = get_db()
        error = None

        if not ingredientName:
            error = "Ingredient name is required."
        else:
            alternatives = db.execute(
                "SELECT * FROM ingredient WHERE r_Average > "
                "(SELECT r_Average FROM ingredient WHERE name = ?)",
                ingredientName)
            # TODO: store the r_Average as a column in the database

        if alternatives is None:
            abort(
                404, f"Ingredient with name {ingredientName} has no alternatives.")

        return alternatives
