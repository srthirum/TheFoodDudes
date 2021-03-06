# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

# Front-end entry points

def aboutus():
    logger.info("aboutus")
    return dict(page = "aboutus")

def favorites():
    logger.info("favorites")
    return dict(page = "favorites")

def index():
    logger.info("index")
    return dict(page = "index")

def upload():
    logger.info("upload")
    logger.info("request.vars before form stuff:")
    logger.info(request.vars)

    form = SQLFORM(db.recipes)

    #form.vars.name = request.vars.name
    #form.vars.image = request.vars.image

    logger.info("form.vars before process()")
    logger.info(form.vars)

    if form.process(onvalidation=print_form_vars).accepted:
        logger.info("accepted form:")
        redirect(URL('recipe', args=form.vars.id))
    elif form.errors:
        logger.info("errors")
    else:
        logger.info("something wrong?")

    return dict(
        page = "upload",
        form = form,
    )

def print_form_vars(form):
    logger.info("printing form vars")
    logger.info(form.vars)


# specific recipe
# will get tags, ingredients, etc. and return everything
# expected format of /recipe/id
def recipe():
    logger.info("recipe")

    if request.args(0) is None:
        redirect(URL('default', 'index'))

    recipe_id = request.args(0)

    logger.info("recipe_id: ")
    logger.info(recipe_id)

    return dict(
        page = "recipe",
        recipe_id = recipe_id
    )



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(
            page = "user",
            form=auth()
    )


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
