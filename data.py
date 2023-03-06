import sqlite3

class actividades_tabla():
  def __init__(self):
    self.crear_tabla()

  def crear_tabla(self):
    coneccion = sqlite3.connect("./data.bd")
    cursor = coneccion.cursor()

    try:
      cursor.execute("""
      CREATE TABLE actividades_tb (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(50),
        color_bg VARCHAR(50),
        color_fg VARCHAR(50),
        color_borde VARCHAR(50),
        anio VARCHAR(50),
        mes VARCHAR(50),
        dia VARCHAR(50),
        hora VARCHAR(50),
        segmento VARCHAR(50),
        id_tarea VARCHAR(50)
        )
      """)
    except Exception as error:
      print(error)
    
    coneccion.commit()
    coneccion.close()


  def guardar_tabla(self, nombre, color_bg, color_fg, color_borde, anio, mes, dia, hora, segmento, id_tarea):
    coneccion = sqlite3.connect("./data.bd")
    cursor = coneccion.cursor()

    cursor.execute("INSERT INTO actividades_tb VALUES (NULL, '"
      + nombre + "','"
      + color_bg + "','"
      + color_fg + "','"
      + color_borde + "','"
      + anio + "','"
      + mes + "','"
      + dia + "','"
      + hora + "','"
      + segmento + "','"
      + id_tarea +
      "')")

    coneccion.commit()
    coneccion.close()


  def editar_tabla(self, id, nombre, color_bg, color_fg, color_borde, anio, mes, dia, hora, segmento, id_tarea):
    coneccion = sqlite3.connect("./data.bd")
    cursor = coneccion.cursor()

    cursor.execute("""UPDATE actividades_tb SET
      nombre = :nombreN,
      color_bg = :color_bgN,
      color_fg = :color_fgN,
      color_borde = :color_bordeN,
      anio = :anioN,
      mes = :mesN,
      dia = :diaN,
      hora = :horaN,
      segmento = :segmentoN,
      id_tarea = :id_tareaN

      WHERE oid = :oid""",{
        "oid":id,
        "nombreN":nombre,
        "color_bgN":color_bg,
        "color_fgN":color_fg,
        "color_bordeN":color_borde,
        "anioN":anio,
        "mesN":mes,
        "diaN":dia,
        "horaN":hora,
        "segmentoN":segmento,
        "id_tareaN":id_tarea
      }
    )

    coneccion.commit()
    coneccion.close()


  def borrar_tabla(self, id):
    coneccion = sqlite3.connect("./data.bd")
    cursor = coneccion.cursor()

    cursor.execute("DELETE FROM actividades_tb WHERE oid=" + str(id))

    coneccion.commit()
    coneccion.close()

  
  def cargar_tabla(self):
    coneccion = sqlite3.connect("./data.bd")
    cursor = coneccion.cursor()

    cursor.execute("SELECT * FROM actividades_tb")
    r = cursor.fetchall()
    lista = []
    for x in r:
      lista.append(x)

    coneccion.commit()
    coneccion.close()

    return lista


class tareas_tabla():
  def __init__(self):
    self.crear_tabla()

  def crear_tabla(self):
    coneccion = sqlite3.connect("./data.bd")
    cursor = coneccion.cursor()

    try:
      cursor.execute("""
      CREATE TABLE tareas_tb (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(50),
        color_bg VARCHAR(50),
        color_fg VARCHAR(50),
        color_borde VARCHAR(50)
        )
      """)
    except Exception as error:
      print(error)
    
    coneccion.commit()
    coneccion.close()


  def guardar_tabla(self, nombre, color_bg, color_fg, color_borde):
    coneccion = sqlite3.connect("./data.bd")
    cursor = coneccion.cursor()

    cursor.execute("INSERT INTO tareas_tb VALUES (NULL, '"
      + nombre + "','"
      + color_bg + "','"
      + color_fg + "','"
      + color_borde + 
      "')")

    coneccion.commit()
    coneccion.close()


  def editar_tabla(self, id, nombre, color_bg, color_fg, color_borde):
    coneccion = sqlite3.connect("./data.bd")
    cursor = coneccion.cursor()

    cursor.execute("""UPDATE tareas_tb SET
      nombre = :nombreN,
      color_bg = :color_bgN,
      color_fg = :color_fgN,
      color_borde = :color_bordeN

      WHERE oid = :oid""",{
        "oid":id,
        "nombreN":nombre,
        "color_bgN":color_bg,
        "color_fgN":color_fg,
        "color_bordeN":color_borde
      }
    )

    coneccion.commit()
    coneccion.close()


  def borrar_tabla(self, id):
    coneccion = sqlite3.connect("./data.bd")
    cursor = coneccion.cursor()

    cursor.execute("DELETE FROM tareas_tb WHERE oid=" + str(id))

    coneccion.commit()
    coneccion.close()

  
  def cargar_tabla(self):
    coneccion = sqlite3.connect("./data.bd")
    cursor = coneccion.cursor()

    cursor.execute("SELECT * FROM tareas_tb")
    r = cursor.fetchall()
    lista = []
    for x in r:
      lista.append(x)

    coneccion.commit()
    coneccion.close()

    return lista

    
class configuracion_tabla():
  def __init__(self):
    self.crear_tabla()

  def crear_tabla(self):
    coneccion = sqlite3.connect("./data.bd")
    cursor = coneccion.cursor()

    try:
      cursor.execute("""
      CREATE TABLE configuracion_tb (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        idioma VARCHAR(50),
        skin VARCHAR(50)
        )
      """)
    except Exception as error:
      print(error)
    
    coneccion.commit()
    coneccion.close()


  def guardar_tabla(self, idioma, skin):
    coneccion = sqlite3.connect("./data.bd")
    cursor = coneccion.cursor()

    cursor.execute("INSERT INTO configuracion_tb VALUES (NULL, '"
      + idioma + "','"
      + skin + 
      "')")

    coneccion.commit()
    coneccion.close()


  def editar_tabla(self, id, idioma, skin):
    coneccion = sqlite3.connect("./data.bd")
    cursor = coneccion.cursor()

    cursor.execute("""UPDATE configuracion_tb SET
      idioma = :idiomaN,
      skin = :skinN

      WHERE oid = :oid""",{
        "oid":id,
        "idiomaN":idioma,
        "skinN":skin
      }
    )

    coneccion.commit()
    coneccion.close()


  def borrar_tabla(self, id):
    coneccion = sqlite3.connect("./data.bd")
    cursor = coneccion.cursor()

    cursor.execute("DELETE FROM configuracion_tb WHERE oid=" + str(id))

    coneccion.commit()
    coneccion.close()

  
  def cargar_tabla(self):
    coneccion = sqlite3.connect("./data.bd")
    cursor = coneccion.cursor()

    cursor.execute("SELECT * FROM configuracion_tb")
    r = cursor.fetchall()
    lista = []
    for x in r:
      lista.append(x)

    coneccion.commit()
    coneccion.close()

    return lista


# colores = ['#fff','#000','#00e5ff', '#6effff', '#1363DF', '#47B5FF', '#06283D', '#DFF6FF']
# skin_1 = ['#fff','#000','#00b2cc','#d0edf0','#00e5ff','#6effff','#c7c7c7','#add8e6', '#1363DF', '#47B5FF', '#06283D', '#DFF6FF']
# self.skin = ['#fff','#000','#00b2cc','#d0edf0','#00e5ff','#6effff','#c7c7c7','#add8e6']

skin_1 = ['#fff','#000','#00b2cc','#d0edf0','#00e5ff','#6effff','#c7c7c7','#add8e6', "#06283D"]

skin_2 = ['#fff','#000','#00cc0e','#d1f0d0','#00ff26','#6eff84','#c7c7c7','#ade6ba']

skin_3 = ['#fff','#000','#cc0022','#ff7f6e','#ff1500','#e6afad','#c7c7c7','#f0d2d0']

          # 0       1       2          3        4         5         6          7        8