# Westridge Maintenance App

## Overview
This application was created to manage equipment maintenance and production productivity. Includes:
  - Assets
  - Work Orders
  - Reminders
  - Dashboard with KPI's
  - Productivity tracking
  ##### Coming up...
  - Equipment parts inventory management

## Getting started
##### Recommended to use python virtual environment
run `pipenv shell`
###### install requirements
run `pip install -r requirements.txt`
###### run server
run `python3 manage.py runserver`

## User Stories
A detailed list of the functionality of your application, told through a user's perspective
As a user, I want the ability to:
  - sign up.
  - sign in. 
  - change my password. 
  - sign out. 
  - create my own assets. 
  - update my assets. 
  - view all of my assets. 
  - read more details of assets WO. 
  - delete assets. 
  - enter production qtys and see productivity

## Wireframes / Screenshots
Diagrams that display what your application will look like, and images from the completed app.
![alt text](media/login.png)
![alt text](media/register.png)
## Entity Relationship Diagrams 
Diagrams that describe the relationships between your resources.
![alt text](media/ERD.png)

### If use pip to install a module, recreate the requirements.txt file

run `pip freeze > requirements.txt` to generate a new requirements file

## Deployment

follow https://docs.render.com/deploy-django#manual-deployment

`python -m pip install gunicorn.`

run command for deployment
`gunicorn mysite.wsgi`

allow new host on settings.py

## Static files

`pip install whitenoise`
`pipenv run pip freeze > requirements.txt`

add middleware
`'whitenoise.middleware.WhiteNoiseMiddleware' `
and
`if not DEBUG:`
    # Tell Django to copy statics to the `staticfiles` directory
    # in your application directory on Render.
    `STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')`

    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`


# RESTfull API Django Framework

root urls: path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
settings: REST_FRAMEWORK
settings: installed apps  'rest_framework',
urls 
views
serializer 


