# Pasos previos: Heroku

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

![buildpacks]()

Agreguen esos dos **en ese orden**.

#### Comandos

````bash
heroku set:buildpack https://github.com/negativetwelve/heroku-buildpack-subdir
heroku add:buildpack heroku/python
````

### Variables

De nuevo desde dos partes:

#### Browser

En Settings de nuevo:

![vals_1]()

Y presionen `Reveal Config vals`:

![vals_2]()

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

Esos valores deberiamos cambiarlos, pero hay que cambiarlos en la app igual, así que serán esos mientras tanto.

## Correr la app

Comandos:

````bash
git push master heroku
# Toma tiempo
heroku ps:scale web=1
heroku open
````

# Deployar con dos app

Trabajo en ello...