# Deploy to Heroku

You can deploy the project to Heroku as a single application or with two
separate apps for frontend and backend. In either case you will have to
provision a **PostgreSql add-on** in Heroku for the database of the app, then
the [django-heroku](https://elements.heroku.com/buildpacks/heroku/django-heroku)
library used in the project will take care of the configurations for the
connections.


## Setup with a single app in Heroku

Create a single app in Heroku (e.g. tablero-digital).

Install the following buildpacks:

* https://github.com/negativetwelve/heroku-buildpack-subdir
* heroku/python

Set the following environment variables in Heroku:

```
SINGLE_HEROKU_APP=true
DJANGO_DEBUG_MODE=false
DJANGO_SECRET_KEY=gp_gsy)lm8=0@jf!ooyzu7ap*y+88^9vl9u^3!mt27=wut4cs$
DJANGO_JWT_SECRET=fTjWnZr4u7x!A%D*G-KaNdRgUkXp2s5v
DJANGO_PRODUCTION_CORS_ORIGIN=https://tablero-digital.herokuapp.com
NODE_ENV=production
VUE_PUBLIC_PATH=https://tablero-digital.herokuapp.com/
REST_API_URL=https://tablero-digital.herokuapp.com/api/v1.0/
```

**Replace `DJANGO_SECRET_KEY` and `DJANGO_JWT_SECRET` with your own new secret
keys.**

**Note we use `tablero-digital` in the urls, replace it with the corresponding
app name.**


## Setup with two separate apps in Heroku

In Heroku create one app for Django (e.g. api-tablero) and one app for the Vue
frontend (e.g. front-tablero).

### Setup for the Django app:

Install the following buildpacks:

* heroku/python

Set these environment variables in Heroku:

```
DJANGO_DEBUG_MODE=false
DJANGO_SECRET_KEY=gp_gsy)lm8=0@jf!ooyzu7ap*y+88^9vl9u^3!mt27=wut4cs$
DJANGO_JWT_SECRET=fTjWnZr4u7x!A%D*G-KaNdRgUkXp2s5v
DJANGO_PRODUCTION_CORS_ORIGIN=https://front-tablero.herokuapp.com
```

**Replace `DJANGO_SECRET_KEY` and `DJANGO_JWT_SECRET` with your own new secret
keys.**

**Note we use `front-tablero` in the url for `DJANGO_PRODUCTION_CORS_ORIGIN`,
replace it with the corresponding app name.**

### Setup for the Vue app:

Install the following buildpacks:

* https://github.com/heroku/heroku-buildpack-multi-procfile
* https://github.com/negativetwelve/heroku-buildpack-subdir

Set the next environment variables in Heroku:

```
NODE_ENV=production
PORT=443
PROCFILE=frontend/Procfile
VUE_PUBLIC_PATH=https://front-tablero.herokuapp.com/
REST_API_URL=https://api-tablero.herokuapp.com/api/v1.0/
```
**Same as before, we use the names we gave as examples for the urls, replace them
with the corresponding app names.**

