# Lab 0 Redes - Lucas Sabino

## Pregunta 1

¿Como sabe el cliente que termino de recibir la respuesta?

El cliente sabe que termino de recibir la respuesta cuando *recv* devuelve *b''*, lo que indica que el servidor cerro la conexion TCP


## Pregunta 2

¿Que parte del comportamiento depende de TCP y cual de HTTP?

TCP garantiza que los datos lleguen completos y en orden, y sin perdidas.
HTTP define el formato del mensaje: el *get*, headers y el body.
TCP no sabe que hay dentro de los datos y HTTP le da el significado a esos datos

## Pregunta 3

¿Que pasaria si el servidor no cerrara la conexion despues de enviar la respuesta?

El cliente se quedaria colgado para siempre esperando mas datos porque *recv* nunca devolveria *b''* si el servidor no cierra la conexion

## Pregunta 4

¿Por que la IP obtenida para el mismo hostname podria ser distinta entre ejecuciones o entre maquinas?

El mismo hostname puede apuntar a distintas IPs porque los servidores DNS pueden devolver diferentes direcciones segun la carga o la ubicacion geografica del cliente. Permite distribuir el trafico entre multiples servidores

## Pregunta 5

¿Por que DNS usa UDP y HTTP usa TCP? ¿Que pasaria si usaramos TCP para las consultas DNS en este cliente?

DNS usa UDP porque las consultas son chicas, una pregunta y una respuesta, y no tiene sentido conectarse y desconectarse para eso. HTTP usa TCP porque una pagina puede ser grande y necesita que todos los bytes lleguen bien y en orden, si se pierde algo la página se rompe

Si usaramos TCP para DNS en este cliente funcionaria pero seria más lento por el overhead de establecer la conexion. TCP para DNS existe pero se reserva para respuestas muy grandes que no entran en los 512 bytes de UDP

## Tarea estrella


Los dominios con caracteres no ASCII usan un estándar llamado
Internationalized Domain Names (IDN). El problema es que el protocolo DNS solo maneja caracteres ASCII, entonces estos dominios se convierten a ASCII usando una codificación llamada *Punycode*.

Por ejemplo:
- `*caracter no ascii*.tw` se representa internamente como `xn--*codigo caracter no ascii*.tw`

En Python esto se puede ver con *str.encode('idna')*

La conversión la hace el cliente antes de consultar el DNS. El servidor DNS nunca ve el caracter no ASCII, solo ve el *xn--...* correspondiente