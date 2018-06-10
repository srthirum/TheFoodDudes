def get_recipes():
    logger.info("get_recipes")

    q = (db.recipes.id > 0)
    recipes = db(q).select()

    response_recipes = []

    for r in recipes:
        tag_names = []
        if r.tags:
            for tagid in r.tags:
                tag = (db(db.tags.id == tagid).select().first())
                if tag:
                    tag_names.append(tag.name)

        logger.info(tag_names)

        response_recipes.append(dict(
            id = r.id,
            name = r.name,
            image = r.image,
            description = r.description,
            instr = r.instr,
            prep_time = r.prep_time,
            cook_time = r.cook_time,
            ingredients = r.ingredients,
            tags = tag_names
        ))

    return response.json(dict(recipes = response_recipes))


def get_recipe():
    logger.info("get_recipe")

    if request.vars.recipe_id == None:
        logger.info("error")

    recipe_id = request.vars.recipe_id

    q = (db.recipes.id == recipe_id)
    r = db(q).select().first()
    logger.info(r)
    tag_names = []

    if not r:
        logger.info("no such recipe")

    if r.tags:
        for tagid in r.tags:
            tag = (db(db.tags.id == tagid).select().first())
            if tag:
                tag_names.append(tag.name)

    recipe = {
        'id': r.id,
        'name': r.name,
        'image': r.image,
        'description': r.description,
        'instr': r.instr,
        'prep_time': r.prep_time,
        'cook_time': r.cook_time,
        'ingredients': r.ingredients,
        'tags': tag_names
    }

    return response.json(dict(recipe=recipe))

