Para poder ejecutar adb.exe:
. Ir a `Ajustes` > `Acerca del teléfono` > `Información de software` > Presionar 7 veces en `Número de compilación`, para poder habilitar `Ajustes` > `Opciones de desarrollador`.

. Ir a `Ajustes` > `Opciones de desarrollador` y habilitar `Depuración por USB`

. La ventana desde donde se ejecutar `python android.py` tiene que haberse abierto como Administrador. Si se abre Visual Studio Code como Administrador, la ventanas de Terminal ya tienen este modo.

. Para probar si adb.exe tiene acceso al celular, probar este comando: `android\platform-tools>adb.exe devices `. Debería listar lo siguiente:
```
List of devices attached 
RFCTA07R21H     device
```

**Conexión inalámbrica:**

1. En `Opciones de desarrollador`  habilitar `Depuración inalámbrica`.

2. Presiona el texto de `Depuración inalámbrica` para ver opciones. Luego presiona `Vincular dispositivo con un código de vinculación`

3.  Toma nota de la dirección IP, el número de puerto y el código de vinculación que se muestran en el dispositivo.

4. Ejecuta `adb pair ipaddr:port` en la terminal de tu estación de trabajo. Usa la dirección IP y el número de puerto que se mencionan arriba.

5. Cuando se te solicite, ingresa el código de vinculación, como se muestra a continuación.

```
$ ./adb pair 192.168.1.ab:<puerto>                                                        
Enter pairing code: zzzxxx
Successfully paired to 192.168.1.ab:<puerto> [....] 
```

6. Ejecutar a continuación `adb devices`. Si el dispositivo no aparece, volver a la opción `Opciones de desarrollador`  -> `Depuración inalámbrica`. Debería aparecer lo siguiente:
```
Nombre del dispositivo
<My nombre de dispositivo>

Dirección IP y puerto
192.158.1.xy:<puerto>
```

7. Ejecutar
```
$ ./adb connect 192.168.1.xy:<puerto>
connected to 192.168.1.xy:<puerto> 
```

8. Validar que la conexión exista:
```
$ ./adb devices   
List of devices attached
192.168.1.xy:<puerto>      device
```

** Paths a los directorios en Android ** 
* Almacenamiento interno:
    
    . Usar `sdcard/` como raíz. Por ejemplo: `sdcard/DCIM/Camera`

* Tarjeta de memoria: seguir estos pasos.

    1. Conectarse al dispositivo usando `./adb connect <ip:puerto>`
    2. Ejecutar `adb shell "ls /storage"`
    3. Eso retorna un output parecido a este:

       ```
       emulated
       self
       XXXX-YYYY
       ```
       . `emulated` -> Internal Storage.
       . `XXXX-YYYY` -> External SD card.

       Then, a typical path for the SD card would be `/storage/XXXX-YYYY/DCIM/Camera`
