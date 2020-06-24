# Run local

## Requirements
- Install NodeJS
- Install Python 3.8

## Back-end
- Create a virtual environment `py -m venv venv`.
- Activate the environment `.\venv\Scripts\activate` in Windows.
- Install requirements with pip `pip install -r requirements.txt`.
- Aplicar cambios del modelo `py manage.py makemigrations`.
- Migrar modelos a la base de datos `py manage.py migrate`.
- Run back-end server `py manage.py runserver`.

## Front end

- Go to front-end directory `cd frontend`.
- Install dependencies `npm install`.
- Run server `npm run serve`.

# Deploy in Heroku

## Requirements

Son básicamente los mismos pasos que en [Getting Started](https://devcenter.heroku.com/articles/getting-started-with-python). Pero acá está en español.

## Crear cuenta

Deben tener cuenta en Heroku: [https://signup.heroku.com/dc](https://signup.heroku.com/dc)

## Instalar Heroku

### Linux:

````bash
sudo snap install heroku --classic
````

### Mac:

Link: [https://cli-assets.heroku.com/heroku.pkg](https://cli-assets.heroku.com/heroku.pkg)

````bash
brew install heroku/brew/heroku
````

### Windows:

Link 32 bit: [https://cli-assets.heroku.com/heroku-x86.exe](https://cli-assets.heroku.com/heroku-x86.exe)

Link 64 bit: [https://cli-assets.heroku.com/heroku-x64.exe](https://cli-assets.heroku.com/heroku-x64.exe)

## Logearse

````bash
heroku login
````

Los tira a su browser.

## Clonar repo

Desde BitBucket:

````bash
git clone https://bitbucket.org/tablerodigital/tablero_digital.git
````

Cambiar a carpeta del repo

````bash
cd tablero_digital
````

# Deployar con una sola app

## Crear y setear app

Desde la ventana de comando en la carpeta (paso anterior):

````bash
heroku create tablero-digital
````

Como aun estamos probando, y en pos del aprendizaje, genérenla en su propia cuenta.

### Builpacks

Ahora instalen los buildpack, tienen dos opciones: desde browser, desde comandos.

#### Browser

En Heroku, vayan a Dashboard y ahí a tablero-digital. Luego busquen la pestaña Settings. Y busquen esto:

![buildpacks](https://bitbucket.org/tablerodigital/tablero_digital/raw/443b5649cef732eacb980c1f676713c12b5d01f7/tutorial/buildpacks.png)

Agreguen esos dos **en ese orden**.

#### Comandos

````bash
heroku buildpacks:set https://github.com/negativetwelve/heroku-buildpack-subdir
heroku buildpacks:add heroku/python
````

### Variables

De nuevo desde dos partes:

#### Browser

En Settings de nuevo:

![vals_1](https://bitbucket.org/tablerodigital/tablero_digital/raw/443b5649cef732eacb980c1f676713c12b5d01f7/tutorial/vals_1.png)

Y presionen `Reveal Config vals`:

![vals_2](https://bitbucket.org/tablerodigital/tablero_digital/raw/443b5649cef732eacb980c1f676713c12b5d01f7/tutorial/vals_2.png)

Agreguen esas variables, las repito acá:

````bash
SINGLE_HEROKU_APP=true
DJANGO_DEBUG_MODE=false
DJANGO_SECRET_KEY=gp_gsy)lm8=0@jf!ooyzu7ap*y+88^9vl9u^3!mt27=wut4cs$
DJANGO_JWT_SECRET=fTjWnZr4u7x!A%D*G-KaNdRgUkXp2s5v
DJANGO_PRODUCTION_CORS_ORIGIN=https://tablero-digital.herokuapp.com
NODE_ENV=production
VUE_PUBLIC_PATH=https://tablero-digital.herokuapp.com/
REST_API_URL=https://tablero-digital.herokuapp.com/api/v1.0/
````

#### Terminal

Los comandos son:

````bash
heroku config:set SINGLE_HEROKU_APP=true
heroku config:set DJANGO_DEBUG_MODE=false
heroku config:set DJANGO_SECRET_KEY=gp_gsy)lm8=0@jf!ooyzu7ap*y+88^9vl9u^3!mt27=wut4cs$
heroku config:set DJANGO_JWT_SECRET=fTjWnZr4u7x!A%D*G-KaNdRgUkXp2s5v
heroku config:set DJANGO_PRODUCTION_CORS_ORIGIN=https://tablero-digital.herokuapp.com
heroku config:set NODE_ENV=production
heroku config:set VUE_PUBLIC_PATH=https://tablero-digital.herokuapp.com/
heroku config:set REST_API_URL=https://tablero-digital.herokuapp.com/api/v1.0/
````

Acá recomiendo usar el browser, al menos para las dos secret key (`DJANGO_SECRET_KEY` y `DJANGO_JWT_SECRET`), porque hay valores que la terminal no identifica.

Esos valores deberíamos cambiarlos, pero hay que cambiarlos en la app igual, así que serán esos mientras tanto.

## Correr la app

Comandos:

````bash
git push heroku master # para correr un branch particular usar git push heroku nombreBranch:master
# Toma tiempo
heroku ps:scale web=1
heroku open
````

## Ejecutar migraciones
Recordar que Django debe ejecutar las migraciones para inicializar la base de datos. En general para ejecutar comandos en host remoto que contiene la aplicación, usamos "heroku run":

````bash
heroku run python manage.py migrate
````

# Deployar con dos app

Aquí deberán crear dos aplicaciones. Si quieren puede ser dos nuevas o pueden borrar la anterior y repetir el nombre. En mi caso, usaré `api-tablero` (así está en el README antiguo). No es tan importante guardar las aplicaciones de heroku vivas (después lo será).

````bash
heroku create api-tablero
heroku buildpacks:set heroku/python -a api-tablero
````

**Ojo**: ahora son dos apps, así que para evitar ambigüedades deben usar el argumento `-a` y especificar la app.

Setear las variables:

````bash
DJANGO_DEBUG_MODE=false
DJANGO_SECRET_KEY=gp_gsy)lm8=0@jf!ooyzu7ap*y+88^9vl9u^3!mt27=wut4cs$
DJANGO_JWT_SECRET=fTjWnZr4u7x!A%D*G-KaNdRgUkXp2s5v
DJANGO_PRODUCTION_CORS_ORIGIN=https://front-tablero.herokuapp.com
````

Ahora sí:

````bash
git push https://git.heroku.com/api-tablero.git HEAD:master
heroku ps:scale web=1 -a api-tablero
# heroku open
# No hagn el último no va a salir nada
````

La aplicación vue:

````bash
heroku create front-tablero
heroku buildpacks:set https://github.com/heroku/heroku-buildpack-multi-procfile -a front-tablero
heroku buildpacks:add https://github.com/negativetwelve/heroku-buildpack-subdir -a front-tablero
````

Y las variables:

````bash
heroku config:set NODE_ENV=production -a front-tablero
heroku config:set PORT=443 -a front-tablero
heroku config:set PROCFILE=frontend/Procfile -a front-tablero
heroku config:set VUE_PUBLIC_PATH=https://front-tablero.herokuapp.com/ -a front-tablero
heroku config:set REST_API_URL=https://api-tablero.herokuapp.com/api/v1.0/ -a front-tablero
````

Y correr:

````bash
git push https://git.heroku.com/front-tablero.git HEAD:master
heroku ps:scale web=1 -a front-tablero
heroku open -a front-tablero
````



