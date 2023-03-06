from tkinter import *
from tkcalendar import DateEntry
from tkinter import colorchooser, messagebox, ttk
from datetime import datetime
import calendar
from data import *
from functools import partial

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class actividad():
  def __init__(self, controlador):
    self.controlador = controlador
    self.skin = self.controlador.skin
    self.id = ''
    self.nombre = ''
    self.color_bg = ''
    self.color_fg = ''
    self.color_borde = ''
    self.anio = ''
    self.mes = ''
    self.dia = ''
    self.hora = ''
    self.segmento = ''
    self.btn = ''
    self.borde = ''
    self.actividad_ref = ''
    self.id_tarea = ''

  def crear_btn(self, frame, hora, columna):
    frame_borde = Frame(frame, bg=self.skin[4], highlightbackground="#000", highlightthickness=1)
    frame_borde.grid(row=1, column=columna, sticky='nwe', padx=[0,5], pady=2)
    button_h1 = Button(frame_borde,text='~ ~ ~', width=20, height=1, bg=self.skin[9], fg="#000", command=lambda:self.editar_btn(), cursor='hand2', relief='flat')
    button_h1.grid(row=1, column=1, sticky='w', ipady=4)
    self.btn = button_h1
    self.borde = frame_borde
    self.hora = str(hora)
    self.segmento = str(columna-1)
    f = self.controlador.fecha_actual
    self.anio = str(f[2])
    self.mes = str(f[1])
    self.dia = str(f[0])

    self.actualizar()
  
  def editar_btn(self):
    if self.controlador.actividad_elegida:
      x = self.controlador.actividad_elegida
      if self.actividad_ref == x:
        self.eliminar()
      else:
        self.btn.config(text=x[1], bg=x[2], fg=x[3])
        self.borde.config(highlightbackground=x[4])
        self.nombre = x[1]
        self.color_bg = x[2]
        self.color_fg = x[3]
        self.color_borde = x[4]
        self.actividad_ref = x
        self.id_tarea = x[0]
        self.guardar()

  def guardar(self):
    x = self.controlador.actividades_tb
    lista = x.cargar_tabla()
    repetida = False
    r_id = 0
    if lista:
      for act in lista:
        if act[5] == self.anio and act[6] == self.mes and act[7] == self.dia and act[8] == self.hora and act[9] == self.segmento:
          repetida = True
          r_id = act[0]
    if repetida == False:
      x.guardar_tabla(self.nombre, self.color_bg, self.color_fg, self.color_borde, self.anio, self.mes, self.dia, self.hora, self.segmento, str(self.id_tarea))
    else:
      x.editar_tabla(r_id, self.nombre, self.color_bg, self.color_fg, self.color_borde, self.anio, self.mes, self.dia, self.hora, self.segmento, str(self.id_tarea))

  def eliminar(self):
    x = self.controlador.actividades_tb
    lista = x.cargar_tabla()
    for actividad in lista:
      if actividad[5] == self.anio and actividad[6] == self.mes and actividad[7] == self.dia and actividad[8] == self.hora and actividad[9] == self.segmento:
        x.borrar_tabla(actividad[0])
        self.btn.config(text='~ ~ ~', bg="#DFF6FF", fg="#000")
        self.borde.config(highlightbackground="#000")
        self.actividad_ref = ''

  def actualizar(self):
    x = self.controlador.actividades_tb
    lista_act = x.cargar_tabla()
    if lista_act:
      for act in lista_act:
        if act[5] == self.anio and act[6] == self.mes and act[7] == self.dia and act[8] == self.hora and act[9] == self.segmento:
          self.btn.config(text=act[1], bg=act[2], fg=act[3])
          self.borde.config(highlightbackground=act[4])
          self.id = act[0]
          self.nombre = act[1]
          self.color_bg = act[2]
          self.color_fg = act[3]
          self.color_borde = act[4]
          self.id_tarea = str(act[10])
    
    y = self.controlador.tareas_tb
    lista_t = y.cargar_tabla()
    if lista_t:
      for t in lista_t:
        if str(t[0]) == str(self.id_tarea):
          self.btn.config(text=t[1], bg=t[2], fg=t[3])
          self.borde.config(highlightbackground=t[4])
    

class controlador():
  def __init__(self, frame):
    self.frame = frame
    self.dia_actual = 'semana_lista_Es[fecha.weekday()]'
    self.fecha_actual = [fecha.day,fecha.month,fecha.year]
    self.label_dia = ''
    self.data_entry = ''
    self.una = True
    self.segmentos = 2
    self.agregar_wg = ''
    self.tareas_tb = tareas_tabla()
    self.actividades_tb = actividades_tabla()
    self.configuracion_tb = configuracion_tabla()
    self.frame_lista = ''
    self.menu_actual = ''
    self.lista_tareas = []
    self.lista_actividades = []
    self.lista_index_inicio = 0
    self.lista_index_fin = 0
    self.lista_limite = 11
    self.menu_opcion = 'abrir'
    self.actividad_elegida = ''
    self.lista_horas_wg = ''
    self.menu_hora = 'abajo'
    self.frame_dias = ''
    self.frame_menu = ''
    self.skin = ''
    self.version = '1.0'
    self.contacto = 'cricen.7@gmail.com'
    self.idiomas_lista = ["Es", "En"] 
    self.idioma = 'En'
    self.skin_lista = ['1', '2', '3']
    self.skin_seleccionada = '1'
    self.opciones_texto = ''
    self.configuracion = ''
    self.img_lista = []
    self.frame_grafico = ''

  
  def inicio(self):   
    self.cargar_datos()
    self.cambiar_idioma()
    self.cambiar_tema()

    if fecha.hour <= 11:
      self.menu_hora = 'arriba'
    else:
      self.menu_hora = 'abajo'

    self.crear_interfaz(1)


  def al_cerrar(self):
    if self.agregar_wg:
      self.agregar_wg.destroy()
    root.destroy()


  def cargar_datos(self):
    self.lista_tareas = self.tareas_tb.cargar_tabla()
    self.lista_actividades = self.actividades_tb.cargar_tabla()
    self.configuracion = self.configuracion_tb.cargar_tabla()

    if self.configuracion:
      x = self.configuracion[0]
      self.idioma = x[1]
      self.skin_seleccionada = x[2]


  def cambiar_tema(self):

    if self.skin_seleccionada == '1':
      self.skin = ['#fff','#000','#00b2cc','#d0edf0','#00e5ff','#6effff','#c7c7c7','#add8e6', "#06283D", '#DFF6FF']
      
      img_izquierda = PhotoImage(file=r'./img/izquierda_azul.png')
      img_izquierda = img_izquierda.subsample(1,1)
      img_derecha = PhotoImage(file=r'./img/derecha_azul.png')
      img_derecha = img_derecha.subsample(1,1)
      img_f_arriba = PhotoImage(file=r'./img/f_arriba_azul.png')
      img_f_arriba = img_f_arriba.subsample(1,1)
      img_f_abajo = PhotoImage(file=r'./img/f_abajo_azul.png')
      img_f_abajo = img_f_abajo.subsample(1,1)
      img_guardar = PhotoImage(file=r'./img/save_azul.png')
      img_guardar = img_guardar.subsample(1,1)
      img_arriba = PhotoImage(file=r'./img/f_azul_arriba.png')
      img_arriba = img_arriba.subsample(1,1)
      img_abajo = PhotoImage(file=r'./img/f_azul_abajo.png')
      img_abajo = img_abajo.subsample(1,1)
      self.img_lista = [img_izquierda, img_derecha, img_f_arriba, img_f_abajo, img_guardar, img_arriba, img_abajo]

    elif self.skin_seleccionada == '2':
      self.skin = ['#fff','#000','#00cc0e','#d1f0d0','#00ff26','#6eff84','#c7c7c7','#ade6ba', '#063d0c', '#dfffe0']
      
      img_izquierda = PhotoImage(file=r'./img/izquierda_verde.png')
      img_izquierda = img_izquierda.subsample(1,1)
      img_derecha = PhotoImage(file=r'./img/derecha_verde.png')
      img_derecha = img_derecha.subsample(1,1)
      img_f_arriba = PhotoImage(file=r'./img/f_arriba_verde.png')
      img_f_arriba = img_f_arriba.subsample(1,1)
      img_f_abajo = PhotoImage(file=r'./img/f_abajo_verde.png')
      img_f_abajo = img_f_abajo.subsample(1,1)
      img_guardar = PhotoImage(file=r'./img/save_verde.png')
      img_guardar = img_guardar.subsample(1,1)
      img_arriba = PhotoImage(file=r'./img/f_verde_arriba.png')
      img_arriba = img_arriba.subsample(1,1)
      img_abajo = PhotoImage(file=r'./img/f_verde_abajo.png')
      img_abajo = img_abajo.subsample(1,1)

      self.img_lista = [img_izquierda, img_derecha, img_f_arriba, img_f_abajo, img_guardar, img_arriba, img_abajo]

    elif self.skin_seleccionada == '3':
      self.skin = ['#fff','#000','#b50012','#ff7f6e','#ff1500','#e6adad','#c7c7c7','#f0d2d0', '#3d060e', '#ffdfdf']
      
      img_izquierda = PhotoImage(file=r'./img/izquierda_roja.png')
      img_izquierda = img_izquierda.subsample(1,1)
      img_derecha = PhotoImage(file=r'./img/derecha_roja.png')
      img_derecha = img_derecha.subsample(1,1)
      img_f_arriba = PhotoImage(file=r'./img/f_arriba_roja.png')
      img_f_arriba = img_f_arriba.subsample(1,1)
      img_f_abajo = PhotoImage(file=r'./img/f_abajo_roja.png')
      img_f_abajo = img_f_abajo.subsample(1,1)
      img_guardar = PhotoImage(file=r'./img/save_roja.png')
      img_guardar = img_guardar.subsample(1,1)
      img_arriba = PhotoImage(file=r'./img/f_roja_arriba.png')
      img_arriba = img_arriba.subsample(1,1)
      img_abajo = PhotoImage(file=r'./img/f_roja_abajo.png')
      img_abajo = img_abajo.subsample(1,1)

      self.img_lista = [img_izquierda, img_derecha, img_f_arriba, img_f_abajo, img_guardar, img_arriba, img_abajo]
       

  def crear_interfaz(self, opcion):
    def crear_wg_dias():
      def cambiar_dia(opcion):
        if opcion == '>':
          dias_en_mes = calendar.monthrange(self.fecha_actual[2], self.fecha_actual[1])[1]
          if self.fecha_actual[0] < dias_en_mes:
            self.una = True
            self.fecha_actual[0] = self.fecha_actual[0]+1
            actualizar_dia()
          else:
            if self.fecha_actual[1] < 12:
              self.una = True
              self.fecha_actual[1] = self.fecha_actual[1]+1
              self.fecha_actual[0] = 1
              actualizar_dia()
            else:
              self.fecha_actual[2] = self.fecha_actual[2]+1
              self.fecha_actual[1] = 1
              self.fecha_actual[0] = 1
              actualizar_dia()


        elif opcion == '<':
          if self.fecha_actual[0] >= 2:
            self.una = True
            self.fecha_actual[0] = self.fecha_actual[0]-1
            actualizar_dia()
          else:
            if self.fecha_actual[1] > 1:
              self.una = True
              self.fecha_actual[1] = self.fecha_actual[1]-1
              self.fecha_actual[0] = calendar.monthrange(self.fecha_actual[2], self.fecha_actual[1])[1]
              actualizar_dia()
            else:
              self.fecha_actual[2] = self.fecha_actual[2]-1
              self.fecha_actual[1] = 12
              self.fecha_actual[0] = calendar.monthrange(self.fecha_actual[2], self.fecha_actual[1])[1]
              actualizar_dia()


        crear_wg_horas_lista(self.menu_hora)

      def actualizar_dia():
        dia = datetime(self.fecha_actual[2],self.fecha_actual[1],self.fecha_actual[0])
        if self.idioma == 'Es':
          dia_text = semana_lista_Es[dia.weekday()]
          self.label_dia.config(text=dia_text)
        elif self.idioma == 'En':
          dia_text = semana_lista_En[dia.weekday()]
          self.label_dia.config(text=dia_text)
        dt=datetime(self.fecha_actual[2],self.fecha_actual[1],self.fecha_actual[0])
        self.data_entry.set_date(dt)

      def cambiar_fecha_dt(dt):
        if self.una == False:
          fecha_local = dt[1].get_date()
          self.fecha_actual[2] = fecha_local.year
          self.fecha_actual[1] = fecha_local.month
          self.fecha_actual[0] = fecha_local.day
          self.una = True
          actualizar_dia()        
        else:
          self.una = False

        crear_wg_horas_lista(self.menu_hora)

      if self.frame_dias:
        self.frame_dias.destroy()
        self.frame_dias = ''

      frame_borde = Frame(self.frame, bg=self.skin[4], highlightbackground="#000", highlightthickness=1)
      frame_borde.grid(row=1, column=1, sticky='nwe', pady=[0,4])

      self.frame_dias = frame_borde

      frame_dia = Frame(frame_borde, bg=self.skin[2], highlightbackground="#000", highlightthickness=1)
      frame_dia.grid(row=1, column=1, sticky='nwe', pady=1, padx=1)

      frame_borde.columnconfigure(1,weight=1)

      dt_var = StringVar()

      if self.idioma == 'Es':
        calendario = 'es'
      elif self.idioma == 'En':
        calendario = 'en'

      cal = DateEntry(frame_dia, width=8, background=self.skin[8], fg='#fff', font=f_3, justify='center', borderwidth=2, textvariable=dt_var, locale=calendario)
      cal.grid(row=1, column=0, sticky='w', padx=[7,3])

      self.data_entry = cal
      x = [dt_var, cal]

      dt_var.trace("w", lambda name, index, mode, var=x: cambiar_fecha_dt(var))

      label_dia = Label(frame_dia, text=self.dia_actual, font=f_1, bg=self.skin[5], fg="#000", highlightbackground="#000", highlightthickness=1)
      label_dia.grid(row=1, column=2, padx=2, pady=2,sticky='news')

      self.label_dia = label_dia

      frame_dia.columnconfigure(2,weight=1)

      button_atras = Button(frame_dia,text='←', image=self.img_lista[0], width=32,height=32, bg=self.skin[2], fg="#fff", command=lambda:cambiar_dia('<'), cursor='hand2', relief='flat')
      button_atras.grid(row=1, column=1, sticky='w')

      button_adelante = Button(frame_dia, text='→', image=self.img_lista[1], width=32,height=32, bg=self.skin[2], fg="#fff", command=lambda:cambiar_dia('>'), cursor='hand2', relief='flat')
      button_adelante.grid(row=1, column=3, sticky='w')
    
    def crear_wg_hora(frame, fila):
      hora = fila
      if datetime.today().hour == hora:
        bg = self.skin[8]
        fg = self.skin[5]
        hb = self.skin[4]
        if datetime.today().minute <= 9:
          self.minutos = f'0{datetime.today().minute}'
        else:
          self.minutos = datetime.today().minute
        if hora <= 9:
          self.texto_hora = f'0{hora}:{self.minutos}'
        else:
          self.texto_hora = f'{hora}:{self.minutos}'
      else:
        bg = self.skin[3]
        fg = "#000"
        hb = "#000"
        if hora <= 9:
          self.texto_hora = f'0{hora}:00'
        else:
          self.texto_hora = f'{hora}:00'

      frame_hora = Frame(frame, bg=bg, highlightbackground=hb, highlightthickness=0, height=2)
      frame_hora.grid(row=fila, column=1, sticky='we', pady=2, padx=5)

      frame.rowconfigure(2,weight=1)
      frame.columnconfigure(1,weight=1)

      label_hora = Label(frame_hora, text=self.texto_hora, font=f_relog, height=2, width=10, bg=bg, fg=fg)
      label_hora.grid(row=1, column=1, sticky='news', padx=[0,5])

      columna=2
      for x in range(0, self.segmentos):
        a = actividad(self)
        a.crear_btn(frame_hora, hora, columna)
        columna+=1

    def crear_wg_menu():
      def cambiar_hora(btn):
        if self.menu_hora == 'abajo':
          btn.config(image=self.img_lista[3])
          self.menu_hora = 'arriba'
        elif self.menu_hora == 'arriba':
          btn.config(image=self.img_lista[2])
          self.menu_hora = 'abajo'

        crear_wg_horas_lista(self.menu_hora)

      def opciones_wg():
        def al_cerrar():
          if self.agregar_actividad_wg:
            self.agregar_wg.destroy()
            self.agregar_wg = ''
        
        def guardar():      
          idioma = opt.get()
          skin = opt_skin.get()

          idioma_check = False
          for y in self.idiomas_lista:
            if str(y) == str(opt.get()):
              idioma_check = True
          
          skin_check = False
          for y in self.skin_lista:
            if str(y) == str(opt_skin.get()):
              skin_check = True

          if idioma_check == True and skin_check == True:
            self.idioma = idioma
            self.skin_seleccionada = skin
            if self.configuracion:
              self.configuracion_tb.editar_tabla(1, self.idioma, self.skin_seleccionada)
            else:
              self.configuracion_tb.guardar_tabla(self.idioma, self.skin_seleccionada)
            if self.frame_lista:
              self.frame_lista.destroy()
              self.frame_lista = ''

            self.cargar_datos()
            self.cambiar_idioma()
            self.cambiar_tema()

            al_cerrar()
            opciones_wg()
            self.crear_interfaz(1)

            self.texto('guardar_config_exito')
          else:
            if idioma_check == False:
              self.texto('guardar_config_fallo_idioma')
            elif skin_check == False:
              self.texto('guardar_config_fallo_skin')
        
        root2 = Toplevel()
        root2.resizable(False, False)
        root2.title('7C-Cronos')
        root2.iconbitmap(root, './img/7C-Cronos.ico')
        x = root.winfo_x()
        y = root.winfo_y()

        root2.geometry("+%d+%d" % (x -12, y +160))

        root2.grab_set()
        root2.attributes('-topmost', True)
        root2.update()
        
        self.agregar_wg = root2

        lista_textos = []

        frame_principal = Frame(root2, highlightthickness=1, highlightbackground='#000', bg=self.skin[7])
        frame_principal.pack()
        
        frame_titulo = Frame(frame_principal, bg=self.skin[2])
        frame_titulo.grid(row=1,column=1, sticky='we')

        label_titulo = Label(frame_titulo, text=self.opciones_texto[0], font=f_1, height=1, bg=self.skin[5], fg="#000", width=20, highlightthickness=1, highlightbackground='#000')
        label_titulo.grid(row=1, column=1, sticky='we', padx=3, pady=3)
        frame_titulo.columnconfigure(1,weight=1)

        lista_textos.append(label_titulo)

        frame_agregar = Frame(frame_principal, bg=self.skin[0], highlightthickness=1, highlightbackground='#000')
        frame_agregar.grid(row=2,column=1, sticky='we',padx=5, pady=5)

        label_idioma = Label(frame_agregar, text=self.opciones_texto[2], bg=self.skin[0], fg='#000', font=('Helvetica', 8, 'bold'), height=2)
        label_idioma.grid(row=4, column=1, sticky='w', padx=[10,0], pady=5)
        frame_agregar.columnconfigure(1, weight=1)

        lista_textos.append(label_idioma)

        opt = ttk.Combobox(frame_agregar, values=self.idiomas_lista, width=10)
        opt.grid(row=4, column=2, sticky='w')
        opt.set(self.idioma)
        
        frame_agregar.columnconfigure(2, weight=1)

        separador = ttk.Separator(frame_agregar)
        separador.grid(row=5, column=1, columnspan=2, sticky='nwe')

        label_skin = Label(frame_agregar, text=self.opciones_texto[3], bg=self.skin[0], fg='#000', font=('Helvetica', 8, 'bold'), height=2)
        label_skin.grid(row=6, column=1, sticky='w', padx=[10,0], pady=5)
        frame_agregar.columnconfigure(1, weight=1)

        lista_textos.append(label_skin)

        opt_skin = ttk.Combobox(frame_agregar, values=self.skin_lista, width=10)
        opt_skin.grid(row=6, column=2, sticky='w')
        opt_skin.set(self.skin_seleccionada)

        separador = ttk.Separator(frame_agregar)
        separador.grid(row=7, column=1, columnspan=2, sticky='nwe')

        label_version = Label(frame_agregar, text=f'{self.opciones_texto[4]} {self.version} \n {self.opciones_texto[5]}', bg=self.skin[0], fg='#000', font=('Helvetica', 8), height=2, width=65)
        label_version.grid(row=10, column=1, columnspan=2, sticky='news', padx=[10], pady=5)
        frame_agregar.columnconfigure(1, weight=1)

        lista_textos.append(label_version)

        separador = ttk.Separator(frame_agregar)
        separador.grid(row=9, column=1, columnspan=2, sticky='we', pady=[10,0])
        
        guardar_btn = Button(frame_agregar, text="", width=32, height=32, bg=self.skin[7], fg="#fff", cursor='hand2', relief='groove', image=self.img_lista[4], command=lambda:guardar())
        guardar_btn.grid(row=8, column=1, columnspan=2, pady=[30,5], ipadx=5, ipady=5)

        lista_textos.append(guardar_btn)

        root2.protocol("WM_DELETE_WINDOW", al_cerrar)

      if self.frame_menu:
        self.frame_menu.destroy()
        self.frame_menu = ''

      frame_menu = Frame(self.frame, highlightthickness=1,highlightbackground='#000',bg=self.skin[4])
      frame_menu.grid(row=3, column=1, pady=[4,0], sticky='news')

      self.frame_menu = frame_menu

      frame_botones = Frame(frame_menu, highlightthickness=1, highlightbackground='#000',bg=self.skin[2])
      frame_botones.grid(row=1, column=1, sticky='news', padx=1, pady=1)

      frame_menu.rowconfigure(1,weight=1)  
      frame_menu.columnconfigure(1,weight=1)

      img=''
      if self.menu_hora == 'abajo':
        img = self.img_lista[2]
      elif self.menu_hora == 'arriba':
        img = self.img_lista[3]
      
      button_menu = Button(frame_botones, text=self.menu_hora, image=img, width=32,height=32, bg=self.skin[2], fg="#fff", cursor='hand2', relief='flat', command=lambda:cambiar_hora(button_menu))
      button_menu.grid(row=1, column=1, sticky='w', padx=22, pady=5)

      label_hora = Label(frame_botones, text='Menu', font=f_2, width=5, height=1, bg=self.skin[8], fg="#fff")
      label_hora.grid(row=1, column=2, sticky='news')
      
      button_agregar = Button(frame_botones, text='Agregar',width=32, height=32, bg=self.skin[2], fg="#fff", image=img_agregar, cursor='hand2', relief='groove', command=lambda:self.agregar_actividad_wg())
      button_agregar.grid(row=1, column=3, sticky='w', padx=[10,10], pady=[2,0], ipadx=2, ipady=2)
       
      button_editar = Button(frame_botones, text='Editar',width=32,height=32, bg=self.skin[2], fg="#fff", image=img_editar, cursor='hand2', relief='groove', command=lambda:self.lista_actividades_wg('editar'))
      button_editar.grid(row=1, column=4, sticky='w', padx=[0,0], pady=[2,0], ipadx=2, ipady=2)
      
      button_eliminar = Button(frame_botones, text='Eliminar', width=32, height=32, bg=self.skin[2], fg="#fff", image=img_eliminar, cursor='hand2', relief='groove', command=lambda:self.lista_actividades_wg('eliminar'))
      button_eliminar.grid(row=1, column=5, sticky='w', padx=[10,10], pady=[2,0], ipadx=2, ipady=2)

      button_ver = Button(frame_botones, text='Ver Lista', width=32, height=32, bg=self.skin[2], fg="#fff", image=img_lista, cursor='hand2', relief='groove', command=lambda:self.lista_actividades_wg('lista'))
      button_ver.grid(row=1, column=6, sticky='w', padx=[0,10], pady=[2,0], ipadx=2, ipady=2)

      button_ver = Button(frame_botones, text='Opciones', width=32, height=32, bg=self.skin[2], fg="#fff", image=img_opciones, cursor='hand2', relief='groove', command=lambda:opciones_wg())
      button_ver.grid(row=1, column=7, sticky='w', padx=[0,10], pady=[2,0], ipadx=2, ipady=2)
      
      # button_agregar = Button(frame_botones, text='Estadistica',width=32, height=32, bg=self.skin[2], fg="#fff", image=img_estadistica, cursor='hand2', relief='groove', command=lambda:self.estadistica())
      # button_agregar.grid(row=2, column=3, sticky='w', padx=[10,10], pady=[2,0], ipadx=2, ipady=2)

    def crear_wg_horas_lista(up_down):

      if self.lista_horas_wg:
        self.lista_horas_wg.destroy()
        self.lista_horas_wg = ''

      lista_horas = Frame(self.frame)
      lista_horas.grid(row=2, column=1,sticky='news')
      fila=2


      self.lista_horas_wg = lista_horas
      if up_down == 'arriba':
        for x in range(0,12):
          crear_wg_hora(lista_horas, x)
          fila+=1
          
      elif up_down == 'abajo':
        for x in range(12,24):
          crear_wg_hora(lista_horas, x)
          fila+=1

    if opcion == 1:
      crear_wg_dias()

      crear_wg_horas_lista(self.menu_hora)

      crear_wg_menu()

    else:
      crear_wg_horas_lista(self.menu_hora)


  def agregar_actividad_wg(self):
    def al_cerrar():
      if self.agregar_wg:
        self.agregar_wg.destroy()
        self.agregar_wg = ''

    def elegir_color(label, opcion):
      color_select = colorchooser.askcolor(parent=self.agregar_wg)[1]
      if opcion == 'fondo':
        label.config(bg=color_select)
      elif opcion == 'letra':
        label.config(fg=color_select)
      elif opcion == 'borde':
        label.config(highlightbackground=color_select)
      
    def elegir_nombre(nombre):
      button_h1.config(text=nombre.get())

    def guardar_actividad():
      nombre = button_h1.cget('text')
      color_bg = button_h1.cget('bg')
      color_fg = button_h1.cget('fg')
      color_bd = frame_borde.cget('highlightbackground')
      
      if nombre and nombre != '~ ~ ~':
        self.tareas_tb.guardar_tabla(nombre, color_bg, color_fg, color_bd)
        self.cargar_datos()

        self.menu_opcion = 'abrir'

        if self.lista_index_fin >= len(self.lista_tareas):
          self.lista_index_fin = self.lista_index_inicio + self.lista_limite

        self.lista_actividades_wg('')
        self.texto('guardar_tarea_exito')
      else:  
        self.texto('guardar_tarea_fallo')

    if self.agregar_wg:
      self.agregar_wg.destroy()
      self.agregar_wg = ''

    root2 = Toplevel()
    root2.resizable(False, False)
    root2.title('7C-Cronos') 
    root2.iconbitmap(root, './img/7C-Cronos.ico')
    root2.geometry("+%d+%d" % (root.winfo_x() +80, root.winfo_y() +150))

    root2.grab_set()
    root2.attributes('-topmost', True)
    root2.update()
    
    self.agregar_wg = root2

    frame_principal = Frame(root2, highlightthickness=1, highlightbackground='#000', bg=self.skin[7])
    frame_principal.pack()
    
    frame_titulo = Frame(frame_principal, bg=self.skin[2])
    frame_titulo.grid(row=1,column=1, sticky='we')

    if self.idioma == 'Es':
      t = 'Nueva actividad'
      n = 'Nombre'
    elif self.idioma == 'En':
      t = 'New activity'
      n = 'Name'

    label_titulo = Label(frame_titulo, text=t, font=f_1, height=1, bg=self.skin[5], fg="#000", width=20, highlightthickness=1, highlightbackground='#000')
    label_titulo.grid(row=1, column=1, sticky='we', padx=3, pady=3)
    frame_titulo.columnconfigure(1,weight=1)  

    frame_agregar = Frame(frame_principal,bg=self.skin[0], highlightthickness=1, highlightbackground='#000')
    frame_agregar.grid(row=2,column=1, sticky='we',padx=5, pady=5)

    label_text = Label(frame_agregar, text=n, font=f_3, height=2, bg=self.skin[8], fg='#fff', width=12)
    label_text.grid(row=1, column=1, sticky='news', pady=[8,0], padx=[5,0])
    frame_agregar.columnconfigure(1,weight=1) 
    
    palabra_var = StringVar()

    entry_tarea = Entry(frame_agregar, justify='center', textvariable=palabra_var, bg=self.skin[0], fg="#000", width=22, highlightthickness=1, highlightbackground='#c7c7c7')
    entry_tarea.grid(row=1,column=2, sticky='news', pady=[8,0], padx=5)
    frame_agregar.columnconfigure(2,weight=1) 

    palabra_var.trace('w', lambda name, index, mode, var=palabra_var: elegir_nombre(var))


    frame_colores = Frame(frame_agregar, bg=self.skin[0])
    frame_colores.grid(row=2, column=1, columnspan=2, sticky='we', pady=[20,10])
    
    color_fondo_btn = Button(frame_colores,text="bg", image=img_color_bg, width=32, height=32, relief='groove', cursor='hand2', bg=self.skin[0], fg="#fff",command=lambda:elegir_color(button_h1,'fondo'))
    color_fondo_btn.grid(row=1,column=1, padx=[30,0], ipadx=5, ipady=5)
    frame_colores.columnconfigure(1,weight=1)

    color_letra_btn = Button(frame_colores,text="fg", image=img_color_fg, width=32, height=32, relief='groove', cursor='hand2', bg=self.skin[0], fg="#000", command=lambda:elegir_color(button_h1,'letra'))
    color_letra_btn.grid(row=1,column=2, ipadx=5, ipady=5)    
    frame_colores.columnconfigure(2,weight=1)
    
    color_borde_btn = Button(frame_colores,text="bd", image=img_color_bd, width=32, height=32, relief='groove', cursor='hand2', bg=self.skin[0], fg="#fff",command=lambda:elegir_color(frame_borde,'borde'))
    color_borde_btn.grid(row=1,column=3, padx=[0,30], ipadx=5, ipady=5)
    frame_colores.columnconfigure(3,weight=1)

    
    frame_btn_ej = Frame(frame_agregar, bg=self.skin[0])
    frame_btn_ej.grid(row=3, column=1, columnspan=2, sticky='we', pady=10)
    frame_agregar.columnconfigure(1,weight=1)
    
    frame_borde = Frame(frame_btn_ej, bg=self.skin[4], highlightbackground="#000", highlightthickness=1)
    frame_borde.grid(row=1, column=1)
    frame_btn_ej.columnconfigure(1,weight=1)

    button_h1 = Button(frame_borde, text='~ ~ ~', width=20, height=1, bg=self.skin[9], fg="#000", cursor='hand2', relief='flat')
    button_h1.grid(row=1, column=1, ipady=4)

    separador = ttk.Separator(frame_agregar)
    separador.grid(row=4, column=1, columnspan=2, sticky='we', pady=[10,0])
    
    guardar_btn = Button(frame_agregar,text="", width=32,height=32, bg=self.skin[7], fg="#fff", cursor='hand2', relief='groove', image=self.img_lista[4], command=lambda:guardar_actividad())
    guardar_btn.grid(row=5, column=1, columnspan=2, pady=10, ipadx=5, ipady=5)

    root2.protocol("WM_DELETE_WINDOW", al_cerrar)


  def lista_actividades_wg(self, opcion):
    def cambiar_lista_wg(o):
      if o == '+':
        if self.lista_index_fin < len(self.lista_tareas):
          self.lista_index_inicio = self.lista_index_fin
          self.lista_index_fin = self.lista_index_fin+self.lista_limite
          self.menu_opcion = 'abrir'
          self.lista_actividades_wg(opcion)
      elif o == '-':
        if not(self.lista_index_inicio-self.lista_limite < 0): 
          self.lista_index_fin = self.lista_index_inicio
          self.lista_index_inicio = self.lista_index_fin-self.lista_limite
          self.menu_opcion = 'abrir'
          self.lista_actividades_wg(opcion)

    def eliminar_actividad(actividad):    
      confirmacion = messagebox.askquestion('Confirma eliminacion de actividad', f'¿Seguro quieres eliminar "{actividad[1]}"?')
      if confirmacion == "yes": 
        self.tareas_tb.borrar_tabla(actividad[0])
        self.cargar_datos()        
        for x in self.lista_actividades:
          if str(x[10]) == str(actividad[0]):
            self.actividades_tb.borrar_tabla(x[0])
        self.menu_opcion = 'abrir'

        if self.lista_index_fin >= len(self.lista_tareas):
          self.lista_index_fin = self.lista_index_inicio + self.lista_limite

        self.lista_actividades_wg(opcion)
        self.crear_interfaz('')
        self.texto('eliminar_tarea_exito')

    def elegir_actividad(actividad):
      self.actividad_elegida = actividad
    
    if self.frame_lista:
        self.frame_lista.destroy()
        self.frame_lista = ''

    if self.menu_opcion == 'cerrar':
      self.menu_opcion = 'abrir'

    elif self.menu_opcion == 'abrir':
      self.menu_opcion = 'cerrar'

      frame_lista = Frame(self.frame, highlightthickness=1,highlightbackground='#000',bg=self.skin[4])
      frame_lista.grid(row=1, column=2, rowspan=3, sticky='news')
        
      self.frame_lista = frame_lista

      frame_botones = Frame(frame_lista, highlightthickness=1, highlightbackground='#000')
      frame_botones.grid(row=1, column=1, sticky='news', padx=1, pady=1)

      self.frame_lista.rowconfigure(1,weight=1)

      # self.lista_tareas = self.tareas_tb.cargar_tabla()

      if self.lista_index_fin == 0:
        if len(self.lista_tareas) >= self.lista_limite:
          self.lista_index_fin = self.lista_limite
        else:
          self.lista_index_fin = len(self.lista_tareas)

      columna=1
      if opcion == 'editar' or opcion == 'eliminar':
        columna = 2

      if self.idioma == 'Es':
        t = 'Actividades'
      elif self.idioma == 'En':
        t = 'Activities'

      label_lista = Button(frame_botones, text=t, font=('Helvetica', 8, 'bold'), width=20, height=2, bg=self.skin[5], fg='#000', relief='groove', cursor='hand2', command=lambda:'self.estadistica()')
      label_lista.grid(row=1, column=1, sticky='we', ipady=1, columnspan=columna)
          
      if self.lista_tareas:
        button_subir = Button(frame_botones, text='↑',image=self.img_lista[5], bg=self.skin[2], fg='#fff', relief='groove', cursor='hand2', command=lambda:cambiar_lista_wg('-'))
        button_subir.grid(row=2, column=1, sticky='wes', pady=[0,2], columnspan=columna)
        separador = ttk.Separator(frame_botones)
        separador.grid(row=3, column=1, sticky='we', pady=[6,3], columnspan=columna)
        fila=4

        for actividad in self.lista_tareas[self.lista_index_inicio:self.lista_index_fin]:

          frame_borde = Frame(frame_botones, bg=self.skin[0], highlightbackground=actividad[4], highlightthickness=1)
          frame_borde.grid(row=fila, column=1, padx=5, pady=[0,5])

          button_h1 = Button(frame_borde, text=actividad[1], width=20, height=1, bg=actividad[2], fg=actividad[3], command=partial(elegir_actividad, actividad), cursor='hand2', relief='flat')
          button_h1.grid(row=1, column=1, ipady=4)

          if opcion == 'editar':
            button_eliminar = Button(frame_botones, text='editar', command=partial(self.editar_actividad, actividad), height=16, width=16, image=img_editar1, bg="#d0edf0", cursor='hand2', relief='groove')
            button_eliminar.grid(row=fila, column=2, padx=5, sticky='e', ipadx=3, ipady=3)

          elif opcion == 'eliminar':
            button_eliminar = Button(frame_botones, text='eliminar', command=partial(eliminar_actividad, actividad), height=16, width=16, image=img_borrar, bg="#d0edf0", cursor='hand2', relief='groove')
            button_eliminar.grid(row=fila, column=2, padx=5, sticky='e', ipadx=3, ipady=3)

          separador = ttk.Separator(frame_botones)
          separador.grid(row=fila+1, column=1, sticky='we', pady=[0,5], columnspan=columna)
          fila+=2
          
        button_bajar = Button(frame_botones, text='↓',image=self.img_lista[6], bg=self.skin[2], fg='#fff', relief='groove', cursor='hand2', command=lambda:cambiar_lista_wg('+'))
        button_bajar.grid(row=fila, column=1, sticky='wes', columnspan=columna)
        frame_botones.rowconfigure(fila, weight=1)
        self.menu_actual = 'lista'
      
      else:
        if self.idioma == 'Es':
          t = 'Sin actividades'
        elif self.idioma == 'En':
          t = 'No activities'
        label_vacio = Label(frame_botones, text=t, bg='#d0edf0', font=f_3)
        label_vacio.grid(row=2, column=1, sticky='news')
        frame_botones.rowconfigure(2,weight=1)


  def editar_actividad(self, actividad):
    def al_cerrar():
      if self.agregar_wg:
        self.agregar_wg.destroy()
        self.agregar_wg = ''

    def elegir_color(label, opcion):
      color_select = colorchooser.askcolor(parent=self.agregar_wg)[1]
      if opcion == 'fondo':
        label.config(bg=color_select)
      elif opcion == 'letra':
        label.config(fg=color_select)
      elif opcion == 'borde':
        label.config(highlightbackground=color_select)
      
    def elegir_nombre(nombre):
      button_h1.config(text=nombre.get())

    def guardar_actividad():
      nombre = button_h1.cget('text')
      color_bg = button_h1.cget('bg')
      color_fg = button_h1.cget('fg')
      color_bd = frame_borde.cget('highlightbackground')
      
      if nombre and nombre != '~ ~ ~':
        self.tareas_tb.editar_tabla(actividad[0], nombre, color_bg, color_fg, color_bd)
        self.cargar_datos()

        for x in self.lista_actividades:
          print(x[10], actividad[0])
          if str(x[10]) == str(actividad[0]):
            self.actividades_tb.editar_tabla(x[0], nombre, color_bg, color_fg, color_bd, x[5], x[6], x[7], x[8], x[9], x[10])

        self.crear_interfaz('')
        self.lista_actividades_wg('cerrar')
        self.lista_actividades_wg('abrir')
        self.texto('editar_tarea_exito')
        al_cerrar()
      else:  
        self.texto('editar_tarea_fallo')


    if self.agregar_wg:
      self.agregar_wg.destroy()
      self.agregar_wg = ''

    root2 = Toplevel()
    root2.resizable(False, False)
    root2.title('7C-Cronos') 
    x = root.winfo_x()
    y = root.winfo_y()
    root2.geometry("+%d+%d" % (x +80, y +150))

    root2.grab_set()
    root2.attributes('-topmost', True)
    root2.update()
    
    self.agregar_wg = root2

    frame_principal = Frame(root2, highlightthickness=1, highlightbackground='#000', bg=self.skin[7])
    frame_principal.pack()
    
    frame_titulo = Frame(frame_principal, bg=self.skin[2])
    frame_titulo.grid(row=1,column=1, sticky='we')

    label_titulo = Label(frame_titulo, text=f'Editar actividad', font=f_1, height=1, bg=self.skin[5], fg="#000", width=20, highlightthickness=1, highlightbackground='#000')
    label_titulo.grid(row=1, column=1, sticky='we', padx=3, pady=3)
    frame_titulo.columnconfigure(1,weight=1)  

    frame_agregar = Frame(frame_principal,bg=self.skin[0], highlightthickness=1, highlightbackground='#000')
    frame_agregar.grid(row=2,column=1, sticky='we',padx=5, pady=5)

    label_text = Label(frame_agregar, text='Nombre:', font=f_3, height=2, bg=self.skin[8], fg='#fff', width=12)
    label_text.grid(row=1, column=1, sticky='news', pady=[8,0], padx=[5,0])
    frame_agregar.columnconfigure(1,weight=1) 

    palabra_var = StringVar()
    palabra_var.set(actividad[1])

    entry_tarea = Entry(frame_agregar, justify='center', textvariable=palabra_var, bg=self.skin[0], fg="#000", width=22, highlightthickness=1, highlightbackground='#c7c7c7')
    entry_tarea.grid(row=1,column=2, sticky='news', pady=[8,0], padx=5)
    frame_agregar.columnconfigure(2,weight=1) 

    palabra_var.trace('w', lambda name, index, mode, var=palabra_var: elegir_nombre(var))


    frame_colores = Frame(frame_agregar, bg=self.skin[0])
    frame_colores.grid(row=2, column=1, columnspan=2, sticky='we', pady=[20,10])
    
    color_fondo_btn = Button(frame_colores,text="bg", image=img_color_bg, width=32, height=32, relief='groove', cursor='hand2', bg=self.skin[0], fg="#fff",command=lambda:elegir_color(button_h1,'fondo'))
    color_fondo_btn.grid(row=1,column=1, padx=[30,0], ipadx=5, ipady=5)
    frame_colores.columnconfigure(1,weight=1)

    color_letra_btn = Button(frame_colores,text="fg", image=img_color_fg, width=32, height=32, relief='groove', cursor='hand2', bg=self.skin[0], fg="#000", command=lambda:elegir_color(button_h1,'letra'))
    color_letra_btn.grid(row=1,column=2, ipadx=5, ipady=5)    
    frame_colores.columnconfigure(2,weight=1)
    
    color_borde_btn = Button(frame_colores,text="bd", image=img_color_bd, width=32, height=32, relief='groove', cursor='hand2', bg=self.skin[0], fg="#fff",command=lambda:elegir_color(frame_borde,'borde'))
    color_borde_btn.grid(row=1,column=3, padx=[0,30], ipadx=5, ipady=5)
    frame_colores.columnconfigure(3,weight=1)

    
    frame_btn_ej = Frame(frame_agregar, bg=self.skin[0])
    frame_btn_ej.grid(row=3, column=1, columnspan=2, sticky='we', pady=10)
    frame_agregar.columnconfigure(1,weight=1)
    
    frame_borde = Frame(frame_btn_ej, bg=self.skin[4], highlightbackground=actividad[4], highlightthickness=1)
    frame_borde.grid(row=1, column=1)
    frame_btn_ej.columnconfigure(1,weight=1)

    button_h1 = Button(frame_borde, text=actividad[1], width=20, height=1, bg=actividad[2], fg=actividad[3], cursor='hand2', relief='flat')
    button_h1.grid(row=1, column=1, ipady=4)

    separador = ttk.Separator(frame_agregar)
    separador.grid(row=4, column=1, columnspan=2, sticky='we', pady=[10,0])
    
    guardar_btn = Button(frame_agregar,text="", width=32,height=32, bg=self.skin[7], fg="#fff", cursor='hand2', relief='groove', image=self.img_lista[4], command=lambda:guardar_actividad())
    guardar_btn.grid(row=5, column=1, columnspan=2, pady=10, ipadx=5, ipady=5)

    root2.protocol("WM_DELETE_WINDOW", al_cerrar)


  def cambiar_idioma(self):
    if self.idioma == 'Es':
      self.dia_actual = semana_lista_Es[fecha.weekday()]
      self.opciones_texto = ['Configuracion', 'Segmentos:', 'Idioma:', 'Tema:', 'Version:', f'Desarrollado por Cricen - Copyright © 2020-{datetime.today().year} - Contacto: {self.contacto}']
    elif self.idioma == 'En':
      self.dia_actual = semana_lista_En[fecha.weekday()]
      self.opciones_texto = ['Settings', 'Segments:', 'Language:', 'Skin:', 'Version:', f'Developed by Cricen - Copyright © 2020-{datetime.today().year} - Contac: {self.contacto}']


  def estadistica(self):

    def al_cerrar():
      if self.agregar_wg:
        self.agregar_wg.destroy()
        self.agregar_wg = ''

    def crear_grafico_bar(frame, mes):
      actividades_lista = []
      cantidad_lista = []
      colores_lista = []

      if mes:
        for act in self.lista_actividades:
          if act[1] not in actividades_lista and act[6] == str(mes):
            actividades_lista.append(act[1])
            colores_lista.append(act[2])
      else:
        for act in self.lista_actividades:
          if act[1] not in actividades_lista:
            actividades_lista.append(act[1])
            colores_lista.append(act[2])

      for x in actividades_lista:
        contador=0
        for act in self.lista_actividades:
          if x == act[1]:
            contador+=1
        cantidad_lista.append(contador/2)

      lista_nombre_cantidad = []
      contador=0
      for x in actividades_lista:
        lista_nombre_cantidad.append(f'{x} - {cantidad_lista[contador]}')
        contador+=1

      if self.frame_grafico:
        self.frame_grafico.destroy()
        self.frame_grafico=''
      
      frame_grafico = Frame(frame, bg=self.skin[0])
      frame_grafico.grid(row=3,column=1, sticky='we', padx=5, pady=[5,5])

      self.frame_grafico = frame_grafico

      fig, axs = plt.subplots(figsize=(12,6), dpi=70)

      # fig.suptitle('Grafico')
      axs.barh(lista_nombre_cantidad, cantidad_lista, color=colores_lista, edgecolor='black', linewidth=1)
      axs.set_title('Grafico')

      chart = FigureCanvasTkAgg(fig,frame_grafico)
      chart.get_tk_widget().grid(row=1, column=1, sticky='we', padx=5, pady=5)

      plt.close()

    def crear_grafico_pico(frame, mes):
      actividades_lista = []
      cantidad_lista = []
      diccionario = {}
      diccionario_completo = {}

      dias_en_mes = calendar.monthrange(self.fecha_actual[2], int(mes))[1]

      for tarea in self.lista_tareas:
        diccionario = {}
        dia=1
        for x in range(0,dias_en_mes):
          contador=0
          for act in self.lista_actividades:
            if act[7] == str(dia) and act[1] == tarea[1]:
              contador+=1
          diccionario[dia] = contador/2  
          dia+=1
        diccionario_completo[tarea[1]] = diccionario

      
      if self.frame_grafico:
        self.frame_grafico.destroy()
        self.frame_grafico=''
      
      frame_grafico = Frame(frame, bg=self.skin[0])
      frame_grafico.grid(row=3,column=1, sticky='we', padx=5, pady=[5,5])

      self.frame_grafico = frame_grafico

      fig, axs = plt.subplots(figsize=(12,6), dpi=70)

      for nombre,lista in diccionario_completo.items():
        actividades_lista = list(lista.keys())
        cantidad_lista = list(lista.values())
        axs.plot(actividades_lista, cantidad_lista, linewidth=2, label=nombre)

      axs.set_title('Grafico')
      axs.legend()

      chart = FigureCanvasTkAgg(fig,frame_grafico)
      chart.get_tk_widget().grid(row=1, column=1, sticky='we', padx=5, pady=5)

      plt.close()

    def por_mes(var):
      if var.get():
        x_int = int(var.get())
        if x_int >= 1 and x_int <= 12:
          if self.frame_grafico:
            self.frame_grafico.destroy()
            self.frame_grafico = ''

          crear_grafico_bar(frame_principal, var.get())
        

    if self.agregar_wg:
      self.agregar_wg.destroy()
      self.agregar_wg = ''

    root2 = Toplevel()
    root2.resizable(False, False)
    root2.title('7C-Cronos') 
    root2.iconbitmap(root, './img/7C-Cronos.ico')
    root2.geometry("+%d+%d" % (root.winfo_x() +80, root.winfo_y() +150))

    root2.grab_set()
    root2.attributes('-topmost', True)
    root2.update()
    
    self.agregar_wg = root2

    frame_principal = Frame(root2, highlightthickness=1, highlightbackground='#000', bg=self.skin[7])
    frame_principal.pack()
    
    frame_titulo = Frame(frame_principal, bg=self.skin[2])
    frame_titulo.grid(row=0,column=1, sticky='we')

    if self.idioma == 'Es':
      t = 'Estadistica'
    elif self.idioma == 'En':
      t = 'Statistic'

    label_titulo = Label(frame_titulo, text=t, font=f_1, height=1, bg=self.skin[5], fg="#000", width=20, highlightthickness=1, highlightbackground='#000')
    label_titulo.grid(row=1, column=1, sticky='we', padx=3, pady=3)
    frame_titulo.columnconfigure(1,weight=1) 

    frame_entry = Frame(frame_principal, bg=self.skin[0])
    frame_entry.grid(row=1,column=1, sticky='we', padx=5, pady=[5,0])


    label_mes = Label(frame_entry, text='Mes:', bg=self.skin[0])
    label_mes.grid(row=1, column=1, padx=[5,0])
    
    palabra_var = StringVar()
    
    entry_tarea = Entry(frame_entry, justify='center', textvariable=palabra_var, bg=self.skin[0], fg="#000", width=10, highlightthickness=1, highlightbackground='#c7c7c7')
    entry_tarea.grid(row=1,column=2, padx=5, pady=10)

    palabra_var.trace('w', lambda name, index, mode, var=palabra_var: por_mes(var))

    frame_botones = Frame(frame_principal, bg=self.skin[0])
    frame_botones.grid(row=2,column=1, sticky='we', padx=5, pady=[5,5])

    btn_act_xmes = Button(frame_botones, text='Total', width=10, height=1, command=lambda:crear_grafico_bar(frame_principal, ''))
    btn_act_xmes.grid(row=1, column=1)

    btn_act_xmes = Button(frame_botones, text='Diario', width=10, height=1, command=lambda:crear_grafico_pico(frame_principal, '9'))
    btn_act_xmes.grid(row=1, column=2)


    root2.protocol("WM_DELETE_WINDOW", al_cerrar)


  def texto(self, opcion):
    if opcion == 'guardar_tarea_fallo':
      if self.idioma == 'Es':        
        messagebox.showerror('Error al guardar nueva actividad', 'Debes escribir un nombre.')
      elif self.idioma == 'En':
        messagebox.showerror('Error saving new activity', 'You must enter a name.')

    elif opcion == 'guardar_tarea_exito':
      if self.idioma == 'Es':        
        messagebox.showinfo('Exito al guardar', 'La actividad se guardo correctamente.')
      elif self.idioma == 'En':
        messagebox.showinfo('Save success', 'Activity saved successfully.')

    elif opcion == 'eliminar_tarea_exito':
      if self.idioma == 'Es':        
        messagebox.showinfo('Exito al eliminar', 'La actividad se elimino correctamente.')
      elif self.idioma == 'En':
        messagebox.showinfo('Delete success', 'The activity was deleted successfully.')

    elif opcion == 'editar_tarea_fallo':
      if self.idioma == 'Es':        
        messagebox.showerror('Fallo al guardar edicion', 'Debes escribir un nombre.')
      elif self.idioma == 'En':
        messagebox.showerror('Failed to save edit', 'You must enter a name.')

    elif opcion == 'editar_tarea_exito':
      if self.idioma == 'Es':        
        messagebox.showinfo('Exito al guardar edicion', 'La actividad se edito correctamente.')
      elif self.idioma == 'En':
        messagebox.showinfo('Successfully saving edit', 'The activity was edited successfully.')

    elif opcion == 'guardar_config_exito':
      if self.idioma == 'Es':        
        messagebox.showinfo('Exito al guardar configuracion', 'La configuracion se guardo correctamente.')
      elif self.idioma == 'En':
        messagebox.showinfo('Successful saving configuration', 'The configuration was saved successfully.')

    elif opcion == 'guardar_config_fallo_idioma':
      if self.idioma == 'Es':        
        messagebox.showerror('Fallo al guardar configuracion', 'Idioma seleccionado incorrecto. Por favor selecciona uno de la lista.')
      elif self.idioma == 'En':
        messagebox.showerror('Failed to save configuration', 'Wrong selected language. Please select one from the list.')

    elif opcion == 'guardar_config_fallo_skin':
      if self.idioma == 'Es':        
        messagebox.showerror('Fallo al guardar configuracion', 'Tema seleccionado incorrecto. Por favor selecciona uno de la lista.')
      elif self.idioma == 'En':
        messagebox.showerror('Failed to save configuration', 'Wrong selected skin. Please select one from the list.')

""""""""""""""""""""""""""""""""""""""""""

root = Tk() 
root.resizable(False, False)
root.iconbitmap('./img/7C-Cronos.ico')
root.title('7C-Cronos')
"""~~~~~~~~~"""
# pyinstaller.exe --onefile --windowed --icon=logox64.ico main.py

colores = ['#fff','#000','#00e5ff', '#6effff', '#1363DF', '#47B5FF', '#06283D', '#DFF6FF']
skin_1 = ['#fff','#000','#00b2cc','#d0edf0','#00e5ff','#6effff','#c7c7c7','#add8e6', '#1363DF', '#47B5FF', '#06283D', '#DFF6FF']

f_1 = ('Segoe Script', 12, 'bold')
f_2 = ('Helvetica', 10, 'bold')
f_3 = ('Helvetica', 8, 'normal')
f_relog = ('ds-digital', 10, 'bold')

img_agregar = PhotoImage(file=r'./img/agregar.png')
img_agregar = img_agregar.subsample(1,1)
img_editar = PhotoImage(file=r'./img/edit.png')
img_editar = img_editar.subsample(1,1)
img_editar1 = PhotoImage(file=r'./img/editar.png')
img_editar1 = img_editar1.subsample(1,1)
img_eliminar = PhotoImage(file=r'./img/delete.png')
img_eliminar = img_eliminar.subsample(1,1)
img_borrar = PhotoImage(file=r'./img/remove.png')
img_borrar = img_borrar.subsample(1,1)
img_lista = PhotoImage(file=r'./img/lista.png')
img_lista = img_lista.subsample(1,1)
img_opciones = PhotoImage(file=r'./img/opciones.png')
img_opciones = img_opciones.subsample(1,1)

img_color_bg = PhotoImage(file=r'./img/fondo.png')
img_color_bg = img_color_bg.subsample(1,1)
img_color_fg = PhotoImage(file=r'./img/texto.png')
img_color_fg = img_color_fg.subsample(1,1)
img_color_bd = PhotoImage(file=r'./img/borde.png')
img_color_bd = img_color_bd.subsample(1,1)

semana_lista_Es = ('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo')
semana_lista_En = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

fecha = datetime.today()

"""~~~~~~~~~"""
main_window = Frame(root)
main_window.pack(fill=BOTH, expand=1)

c = controlador(main_window)
c.inicio()

root.protocol("WM_DELETE_WINDOW", c.al_cerrar)
root.mainloop()   