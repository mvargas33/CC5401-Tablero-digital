'use strict' // Para usar nueva notación de JS

const delay = require('delay');
const bodyParser = require('body-parser'); // Para parsear solicitudes POST y otras
const app = require('express')() // Servidor
const server = require('http').Server(app);
const io = require('socket.io')(server);

const port = process.env.PORT || 3000 // Puerto del servidor

app.use(bodyParser.urlencoded({extended: true })) // Estas dos líneas son estándar
app.use(bodyParser.json()) // Usar formato JSON para POST

server.listen(port, () => { // Pasamos una lambda que solo hace log
    console.log(`Servidor corriendo en http://localhost:${port}`) // Print inicial del servidor
})

io.on('connection', function(socket) {
    console.log('A user connected');

    socket.on('disconnect', () => {
        console.log('A user disconnected');
    })

    socket.on('appenduser' , function(data) {
        console.log('appenduser');
        console.log(data)
        socket.emit('new_user', {user: "Angelica"});
    })

    
})



async function init(){
    while(1){
        io.emit('new_user', {user: "Angelica"});
        await delay(1000)
    }
}
init()