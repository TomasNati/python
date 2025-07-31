Para poder ejecutar adb.exe:
. Ir a `Ajustes` > `Acerca del teléfono` > `Información de software` > Presionar 7 veces en `Número de compilación`, para poder habilitar `Ajustes` > `Opciones de desarrollador`.

. Ir a `Ajustes` > `Opciones de desarrollador` y habilitar `Depuración por USB`

. La ventana desde donde se ejecutar `python android.py` tiene que haberse abierto como Administrador. Si se abre Visual Studio Code como Administrador, la ventanas de Terminal ya tienen este modo.

. Para probar si adb.exe tiene acceso al celular, probar este comando: `android\platform-tools>adb.exe devices `. Debería listar lo siguiente:
```
List of devices attached 
RFCTA07R21H     device
```