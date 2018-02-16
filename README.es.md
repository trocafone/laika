
# Reports

*reports* es una bibliotéca que sirve para generar reportes y guardarlos en
un formato específico y en un lugar específico. Por ejemplo: se le puede especificar
un reporte con datos tomados de una base de datos y que se guarde en Google Drive.

TODO

## Instalación

TODO

## Ejemplo de uso

La herramienta se utiliza desde la línea de comando de la siguiente forma:

```bash
$ ./reporter.py some_report
```
Este comando correrá el reporte definido con el nombre *some_report*.


Se le puede pasar el archivo de configuración a usar por parámetro.

```bash
$ ./reporter.py -c my_config.json
```

Tambien la ruta al archivo de configuración se puede guardar en la variable de
entorno `REPORTER_CONFIG_FILE_PATH`.

```bash
$ export REPORTER_CONFIG_FILE='/home/me/my_config.json'
./reporter.py my_report
```

Otro parámetro que se le puede pasar es `--pwd` para especificar el directorio
de trabajo. Tambien se puede especificar en el archivo de configuración o la
variable de entorno `REPORTER_PWD`.

### Argumentos

Todos los arguments definidos en el reporte se pueden ver usando `--help` flag.

Los argumentos que no estén definidos por el reporter se van a agregar a la
configuración del reporte, y sobreescribirán la misma. De esta forma si, por
ejemplo, la configuración de un reporte `my_report` define un campo `my_field` con
un valor `foo`, si se lo llama de la siguiente forma:

```bash
$ ./reporter.py my_report --my_field bar
```

La configuración `my_field` tendrá el valor `bar` a la hora de ejecutarlo.


## Configuración

Reporter toma los reportes posibles desde un archivo en formato json. Este archivo tiene que tener la siguiente estructura:

```json
{
  "include": [...],
  "reports": [...],
  "connections": [...],
  "profiles": [...]
}
```


La configuración se puede dividir en varios archivos. Es necesario tener un
archivo de configuración base, y éste puede tener un campo `"include"` con
un listado de archivos:

```json
"include": [
  "another_config.json",
  "/some/config.json"
]
```

Estos archivos se van a incluir en la configuración. La restricción que tienen
es que solo pueden tener definidos campos `reports`, `connections` y `profiles`.


### Profiles

Los profiles son todo tipo de credenciales, necesarios para acceder a APIs
externas (por ejemplo, Google Drive). Se le tiene que especificar el nombre y el
archivo con credenciales. Ejemplo de un perfil:

```json
{
  "name": "my_drive",
  "credentials": "secret.json"
}
```

El campo credentials tiene que apuntar a un archivo en formato json, cuyo contenido
depende de cada caso. Por ejemplo las credenciales de email pueden ser:

```json
{
  "username": "me@gmail.com",
  "password": "secret"
}
```

### Connections

Connections son conecciones a fuentes de datos o destinos de resultados.
Necesitan un *name*, un *type* y campos específicos de la conección. Las
siguientes son las conecciones existentes.

#### Postgres

Ejemplo de una conección a una base de datos PostgreSQL:

```json
{
  "name": "local",
  "type": "postgre",
  "constring": "postgresql://user@localhost:5432/database"
}
```

#### Email

Ejemplo de una conección email:

```json
{
  "name": "gmail_smtp",
  "type": "email",
  "host": "smtp.gmail.com",
  "port": 587
}
```

#### Ftp

Ejemplo de una conección ftp:

```json
{
  "name": "some_ftp",
  "type": "ftp",
  "host": "ftp.home.com"
}
```


### Reportes

Los reportes se especifican como objetos json, los siguientes campos son
requiridos:

  - name: El nombre del reporte, el cual luego se va a poder usar por línea de comando.
  - type: El tipo de reporte. Los tipos existentes al momento: *query* y *redash*.
  - results: Listado de configuraciones de como guardar el resultado. Cada result en esa
    lista Tiene que ser un objeto. *type* es el campo requirido para
    todos los resultados, el resto de los campos se detallarán más adelante.

#### Query

`type: query`. Este tipo de reporte corre una query contra la base de datos.
Las configuraciones necesarias son:

  - query_file: el archivo que contiene el código de la query (plano).
  - connection: el nombre de la conección a utilizar
  - variables: es un diccionario con valores a reemplazar en la query. Cómo
  funciona es explicado en [Parametrizando reportes](#parametrizando-reportes).

Ejemplo de un reporte de tipo query:

```json
{
  "name": "my_shiny_query",
  "type": "query",
  "query_file": "query.sql",
  "connection": "local",
  "variables": {
    "foo": "bar"
  },
  "results": [...]
}
```

#### Redash

`type: redash`. Este reporte se conecta a la API de redash y toma los datos
actuales de la query especificada. Sus configuraciones son:

  - redash_url: la url de redash, a cuya API se va a comunicar.
  - query_id: el identificador de la query a usar. Es la última parte de la url
  de la query (por ejemplo: en `https://some.redash.com/queries/67`, 67 es el
  id de la query)
  - api_key: el token para acceder a la query. Existen 2 tipos: api key de query
  y de usuario. El de la query se puede encontrar yendo a la página de la query
  y presionando el botón con el ícono de llave (al lado de *Download Dataset*).
  El de usuario se puede encontrar en el perfil.

Ejemplo de una query redash:

```json
{
  "name": "some_redash_query",
  "type": "redash",
  "api_key": "some api key",
  "query_id": "123",
  "redash_url": "https://some.redash.com",
  "results": [...]
}
```

#### Bash Script

`type: bash`. Este reporte, ejecuta un comando bash y toma lo que imprime por consola.
Como analogia para entender, utiliza el PIPE de unix para redirigir todos los outputs del script,
y levantarlos como resultado de una query. Ej:
```bash
$ bash_script | read_output
```


Sus configuraciones son:

  - script: el comando a ejecutar para obtener el resultado.
  - script_file: el archivo que contiene el código bash. Este campo se ignora
  si *script* está definido
  - result_type: el tipo de formato que van a tener los datos entrantes. Puede
  ser *csv*, *json* o *raw*. En el caso de *raw*, el contenido de lo devuelto
  por el script no se va a procesar y se va a enviar directamente a los
  resultados. El formato de json que se espera está explicado [más abajo](#bash-script-json)

Ejemplo de una query json:

```json
{
  "name": "some_bash_script",
  "type": "bash",
  "script_file": "some_script.bash",
  "result_type": "json",
  "results": [...]
}
```

##### Bash Script - JSON

El formato del json puede ser de dos tipos:

Pasanrle un objeto, especificando la columna como key y pasandole como value
un array con los datos para cada fila.
** Nota: ** Requerido que todos los arrays tengan el mismo tamaño

```json
{
  "column_1": ["data_row_1", "data_row_2", "data_row_3"],
  "column_2": ["data_row_1", "data_row_2", "data_row_3"],
  "column_3": ["data_row_1", "data_row_2", "data_row_3"],
  "column_4": ["data_row_1", "data_row_2", "data_row_3"]
}
```

Pasandole un array de Filas, la cual cada Fila, va a ser un objeto.
Cada key del objeto Fila, va a ser el nombre de la columna y su value será
el dato para esa fila y columna.

**Nota:** A diferencia del formato anterior, no es necesario que todas las filas
tengan la misma cantidad de columnas. Las filas que no definan un valor para una columna,
quedaran vacias.

```json
[
  {
    "column_1": "data_row_1",
    "column_2": "data_row_1",
    "column_3": "data_row_1",
  },
  {
    "column_1": "data_row_2",
    "column_3": "data_row_2",
  },
  {
    "column_1": "data_row_3",
    "column_2": "data_row_3",
    "column_4": "data_row_3",
  },
  {
    "column_1": "data_row_4",
    "column_2": "data_row_4",
    "column_3": "data_row_4",
    "column_4": "data_row_4",
  }
]
```


#### Adwords


`type: adwords`. Este reporte se genera de la API de adwords de google. Se hace uso de la biblioteca [googleads](https://github.com/googleads/googleads-python-lib/). Sus configuraciones son:

  - profile: El perfil con las credenciales a usar. El archivo de credenciales es un archivo .yaml, [en el tutorial de adwords](https://developers.google.com/adwords/api/docs/guides/start) se puede leer un poco más sobre este archivo.
  - report_definition: La definición del reporte a descargar. Se pasa tal como está
  definido al método [DownloadReport](http://googleads.github.io/googleads-python-lib/googleads.adwords.ReportDownloader-class.html#DownloadReport) de la api de googleads.
  Suele definir los campos `reportName`, `dateRangeType`, `reportType`, `downloadFormat`,
  `selector`, pero varian dependiendo del tipo del reporte.
  - reportName: Para no repetir la definición del reporte, se puede especificar el
  nombre del reporte y se va a utilizar el report_definition correspondiente al otro
  reporte (debe ser el mismo que el especificado adentro del report_definition del
  otro reporte).
  - dateRangeType: si se utiliza el report_definition de otro reporte, se le puede
  pisar la configuración del rango de fechas con este campo.
  - [client_customer_id](https://support.google.com/adwords/answer/29198?hl=en):
  El id o ids de customers, para los datos de los cuales se va a generar un reporte.
  Puede ser un solo id como string, o una lista de ids.

Ejemplo de una query adwords:

```json
{
  "name": "some_adwords_report",
  "type": "adwords",
  "client_customer_id": "123-456-7890",
  "report_definition": {
    "reportName": "Shopping Performance Last Month",
    "dateRangeType": "THIS_MONTH",
    "reportType": "SHOPPING_PERFORMANCE_REPORT",
    "downloadFormat": "CSV",
    "selector": {
        "fields": [
            "AccountDescriptiveName",
            "CampaignId",
            "CampaignName",
            "AdGroupName",
            "AdGroupId",
            "Clicks",
            "Impressions",
            "AverageCpc",
            "Cost",
            "ConvertedClicks",
            "CrossDeviceConversions",
            "SearchImpressionShare",
            "SearchClickShare",
            "CustomAttribute1",
            "CustomAttribute2",
            "Brand"
        ]
    }
  },
  "results": [...]
}
```

#### Facebook Insights

TODO: document

#### Download From Google Drive

`type: drive`. Este reporte descarga un archivo de google drive.

  Configuración:

  - profile: El perfil a utilizar. Las credenciales de este perfil tendrán que ser
  las de una cuenta de servicio con acceso a la API de Google Drive.
  - grant: Email del usuario, es el nombre de quien se va a descargar el documento.
  Tiene que tener el acceso al folder especificado.
  - filename: Archivo a descargar.
  - folder: En que directorio se encuentra el archivo a descargar.
  - folder_id: Evita confusiones con nombres repetidos, no es necesario especificar
  folder.
  - subfolder: Parametro opcional. Busca una subfolder dentro de la folder especificada,
  evita confusiones.
  - file_id: id del archivo a descargar, no es necesario especifiar folders y filename.

Ejemplo de un reporte Drive:

```json
{
  "type": "drive",
  "profile": "drive_service_account",
  "grant": "me@mail.com",
  "folder_id": "my_folder_id",
  "folder": "TestFolder",
  "subfolder": "TestSubFolder",
  "file_id": "my_file_id",
  "filename":"file_to_download.xlsx"
}
```


#### Download From S3

`type: s3`. Este reporte descarga un archivo de amazon s3. Para usar este
reporte, es necesario instalar [boto3](http://boto3.readthedocs.io/en/latest/guide/quickstart.html#installation).

Configuración:

  - profile: El perfil a utilizar. Es el perfil de reporter, no confundir con
  los perfiles de amazon. El archivo, específicado en credentials tendrá
  que contener datos para pasarle al constructor de [Session](http://boto3.readthedocs.io/en/latest/reference/core/session.html#boto3.session.Session). Ejemplo de un
  archivo de credenciales de s3 mínimo:

  ```json
  {
    "aws_access_key_id": "my key id",
    "aws_secret_access_key": "my secret access key"
  }
  ```

  - bucket: Bucket de s3 del cual descargar el archivo.
  - filename: Archivo a descargar. Este dato es la *key* del archivo a descargar
  del bucket.

Ejemplo de un reporte a descargar de s3:

```json
{
  "name": "s3_report_example",
  "type": "s3",
  "profile": "my_aws_profile",
  "bucket": "some.bucket",
  "filename": "reports/custom_report.csv",
  "results": [...]
}
```


#### Module

TODO: document


### Results

#### File

`type: file`. Guardar el resultado del reporte en un archivo. Las configuraciones
de este Result son:

  - filename: El nombre de archivo resultante. Si tiene extensiones `xls` o `xlsx`,
  se guardará en formato Excel, sino se va a guardar como csv.

Ejemplo de un resultado File:

```json
"result": {
  "type": "file",
  "filename": "output.csv"
}
```

#### Email

`type: email`. Enviar el resultado del reporte como archivo adjunto por email.
Las configuraciones son:

  - profile: El perfil con credenciales a utilizar. Las credenciales tienen que
  tener el usuario y la contraseña del servicio smtp a utilizar (campos
  `username` y `password`).
  - connection: Una conección de tipo email.
  - filename: El nombre del archivo a adjuntar.
  - recipients: El o los receptores del email. Puede ser string con un receptor
  o lista de strings con varios. Este campo es obligatorio.
  - subject: El tema del email.
  - body: El texto del email. Se puede formatear igual que el filename (Ver la sección [Parametrizando el nombre del archivo](#parametrizando-el-nombre-del-archivo))
  - attachments: Lista de archivos para attachear al emails. Deben ser rutas a archivos.

Ejemplo de un resultado Email:

```json
{
  "type": "email",
  "filename": "report_{Y}-{m}-{d}_{H}-{M}.xlsx",
  "recipients": ["some_recipient@mail.com", "another_recipient@foo.com"],
  "subject": "Some report",
  "body": "Report generated {Y}-{m}-{d} {H}:{M}. \nDo not reply this email!",
  "profile": "my_gmail",
  "connection": "gmail_smtp"
}
```

#### Ftp

`type: ftp`. Subir el resultado del reporte a un servidor ftp..
Las configuraciones son:

  - profile: El perfil con credenciales a utilizar. Las credenciales tienen que
  tener el usuario y la contraseña del servicio ftp a utilizar (campos
  `username` y `password`).
  - connection: Una conección de tipo ftp.
  - filename: El nombre del archivo a adjuntar.

Ejemplo de un resultado Email:

```json
{
  "type": "ftp",
  "profile": "my_ftp_profile",
  "connection": "some_ftp",
  "filename": "my_report.csv"
}
```

#### Drive

`type: drive`. Guarda el resultado del reporte en Google Drive.

  Estas son las configuraciones:

  - profile: El perfil a utilizar. Las credenciales de este perfil tendrán que ser
  las de una cuenta de servicio con acceso a la API de Google Drive.
  - filename: El nombre de archivo resultante.
  - folder: En qué directorio guardarlo, opcional. Si no se pasa, el reporte se
  guardará en la raiz. El directorio tiene que existir. En el caso de existir dos
  directorios con el mismo nombre, se guardará en el primero.
  - folder_id: El id de directorio, en el cuál se guardará el archivo. Ese dato
  evitará confusiones de nombre, que puede presentar el parametro anterior. El
  id de la carpeta se puede obtener de la última parte de la url desde la interfaz
  de google drive.
  - grant: Email del usuario, en el nombre de quien se va a guardar el documento.
  Tiene que tener el acceso al folder especificado.

Ejemplo de un resultado Drive:

```json
{
  "type": "drive",
  "filename": "report.xlsx",
  "profile": "my_service_drive_account",
  "folder": "TestFolder",
  "grant": "me@mail.com"
}
```

#### Module

`type: module`. Permite definir un archivo python con una clase de Resultado
definida por el usuario. Estos son los campos que se requieren:

  - result_file: El archivo con el resultado definido.
  - result_class: La clase de resultado. Tiene que heredar de `Result` y
  tener definido el método `save`. Ejemplo de una clase customizada:

    ```python
    from reports import Result

    class FooResult(Result):

        def save(self):
            # using some custom configs
            filename = self.custom_filename
            # doing the actual save
            print str(self.data)
    ```

Notese que el resultado custom se va a ejecutar como cualquier otro resultado -
se le va a pasar la configuración y las configuraciones del resultado, por ende
es buena idea definir las configuraciones para el resultado creado.

**Advertencia**: reporter va a cargar y ejecutar el archivo, y luego va a
utilizar la clase del resultado, con todas los agujeros de seguridad que eso
implica.

```json
{
  "type": "module",
  "result_file": "./some_folder/my_custom_result.py",
  "result_class": "MyResult",
  "my_custom_config": "value"
}
```


#### Redash

`type: redash`. Guarda el resultado del reporte como un archivo *json* que se
puede servir a redash mediante una API. Redash lo puede consumir utilizando el
datasource de url. En cuanto a la configuración, admite los mismos campos que
el resultado [File](#file), con la excepción de que el archivo tiene que ser un
json (siempre se va a guardar como json, independientemente de la extensión).


#### S3

`type: s3`. Guarda el resultado en amazon s3. Para usar este
reporte, es necesario instalar [boto3](http://boto3.readthedocs.io/en/latest/guide/quickstart.html#installation).

Configuración:

  - profile: El perfil a utilizar. Es el perfil de reporter, no confundir con
  los perfiles de amazon. El archivo, específicado en credentials tendrá
  que contener datos para pasarle al constructor de [Session](http://boto3.readthedocs.io/en/latest/reference/core/session.html#boto3.session.Session). Ejemplo de un
  archivo de credenciales de s3 mínimo:

  ```json
  {
    "aws_access_key_id": "my key id",
    "aws_secret_access_key": "my secret access key"
  }
  ```

  - bucket: Bucket de s3 en el cual se va a guardar el archivo.
  - filename: Nombre del archivo a guardar. Este dato es la *key* del archivo a
  escribir en el bucket.

Ejemplo de un resultado escrito s3:

```json
{
  "type": "s3",
  "profile": "my_aws_profile",
  "bucket": "some.bucket",
  "filename": "reports/custom_report.csv"
}
```


### Configuración global

Además de reportes, conecciones y perfiles se permiten configurar algunos datos
estáticos:

  - timezone: la string del timezone a usar. Por defecto todas las fechas se
  generan en utc. Esta configuración puede ser reescrita para cada reporte
  particular.

  - pwd: el directorio por defecto desde el cual reporter va a leer los archivos
  de querys y guardar los resultados (en el caso de que se especifiquen con ruta
  relativa).


## Parametrizando reportes

En la definición de una query (u otras templates formateables) se pueden especificar fechas dinámicas de la siguiente forma:

```sql
select * from some_table where date >= '{m}' and date < '{m+1m}'
```

reports va a reemplazar esas variables por (suponiendo que estamos en Febrero del 2016):

```sql
select * from some_table where date >= '2016-02-01 00:00:00' and date < '2016-03-01 00:00:00'
```

Las fechas por defecto son UTC, esto se puede modificar en la configuración
`timezone` global o para cada reporte particular.

Todas las variables que se pueden utilizar:

  - `{now}`: la fecha actual exacta
  - `{d}` o `{t}`: el comienzo del día de hoy (00:00:00 de hoy)
  - `{m}`: el comienzo del primer día de este mes
  - `{y}`: el comienzo del año (primer día de Enero)
  - `{H}`: el comienzo de la hora actual
  - `{M}`: el comienzo del minuto
  - `{w}`: el comienzo de la semana (Lunes)

A estas variables se les pueden agregar modificadores. Las expresiones con
modificadores siempre tienen que comenzar con alguna de las variables anteriores,
seguir con un signo (`+` o `-`), un número y terminar con la magnitud. Las magnitudes
aceptadas son:

  - `{y}`: años
  - `{m}`: meses
  - `{d}`: días
  - `{h}`: horas
  - `{M}`: minutos
  - `{w}`: semanas

Por ejemplo:

```
{now}, {now-1d}, {now+1y}, {now+15h}, {t-3m}
```

Resulta en:

```
2016-02-12 18:19:09, 2016-02-11 18:19:09, 2017-02-12 18:19:09, 2016-02-13 09:19:09, 2015-11-12 00:00:00
```

Otra pisbilidad es especificar un día de la semana:

  - `{f}`: Mueve la fecha una cantidad de Lunes. Por ejemplo, {d-1f} moverá la
  fecha al Lunes actual y {d+2f} moverá la fecha al Lunes dentro de 2 semanas.

Si el reporte tiene un diccionario de variables especificado, estas se reemplazan
de la misma forma, previo al reemplazo de fechas. Por ejemplo, si tenemos
las siguientes variables:

```json
{
  "variables": {
    "yesterday": "{t-1d}"
  }
}
```

Entonces `{yesterday}` resultará en `2016-02-12 17:19:09`


### Parametrizando el nombre del archivo

Los reportes `file` y `drive` toman como parámetro el nombre del archivo. Este
nombre se puede formatear de la misma forma. Por ejemplo, si se define:

```json
{"filename": "report_{Y}-{m}"}
```

El nombre resultante será `report_2016-02` (Asumiendo que se corrió en Febrero del 2016).

Se puede usar los mismos modificadores que para el reporte. Por ejemplo:

```json
{"filename": "report_{Y}-{m-1m}"}
```

Resultará en `report_2016-01`.


### Testeo

Para correr los tests, hay que instalar las dependencias de test:

TODO: document this

Luego, hace falta estar en el directorio de reporter:

```bash
$ cd path/to/reporter
```

y ejecutar la siguiente linea:

```bash
$ python -m unittest discover
```


