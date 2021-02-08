from tkinter import ttk
from tkinter import *

import sqlite3

class Product():

    db_name = 'database.db'  # nombrando db

    def __init__(self, window):  # creando la parte visual y las variabless id, name, price y la tabla tree
        self.wind = windows
        self.wind.title('Aplicacion de Productos')
        
        # Creando un Frame Container. Es como un recuadro con titulo
        frame = LabelFrame(self.wind, text='Registrar nuevo producto')
        frame.grid(row=0, column=0, columnspan=3, pady=20)  # Acomodando el contenedor

        # Ingreso de articulo
        Label(frame, text='Nombre: ').grid(row=1, column=0)
        self.name = Entry(frame)  # input
        self.name.focus()  # hace que el cursor se coloque aqui
        self.name.grid(row=1, column=1)  # acomodando el input

        # Ingreso de precio
        Label(frame, text='Precio: ').grid(row=2, column=0)
        self.price = Entry(frame)  # input
        self.price.grid(row=2, column=1)  # acomodando el input

        # Boton guardar producto
        ttk.Button(frame, text='Guardar producto', command=self.add_products).grid(row=3, columnspan=2, sticky= W + E)  # Sticky <-> screen

        # Botones de borrar y actualizar
        ttk.Button(text='BORRAR', command=self.delete_product).grid(row=5, column=0, sticky=W+E)
        ttk.Button(text='EDITAR', command=self.edit_product).grid(row=5, column=1, sticky=W+E)

        # Mensaje luego de guardar un producto
        self.message = Label(text='', fg='red')  # sin texto y de color rojo
        self.message.grid(row=3, column=0, columnspan=2, sticky= W + E)

        # Creacion de Tabla
        self.tree = ttk.Treeview(height=10, columns=2)  # Tabla, con alto y columnas. this es una prop para reutilizar
        self.tree.grid(row=4, column=0, columnspan=2)  # Acomodando la tabla
        self.tree.heading('#0', text='Nombre', anchor=CENTER)  # #0 es la column, anchor es la justificacion
        self.tree.heading('#1', text='Precio', anchor=CENTER)  # #0 es la column, anchor es la justificacion

        self.get_products()  # llama a la funcion mostrar la db llenando la tabla

    def run_query(self, query, parameters=()):  # ejectuar consulta a db, con la consulta y los parametros si existiecen
        with sqlite3.connect(self.db_name) as conn:  # me conecto a la base de datos y el as conn permite guardar la misma
            cursor = conn.cursor()  # el metodo permite conocer la coordenada de posicion en la db, se almacena
            result = cursor.execute(query, parameters)  # prepara la consulta en si con parametros o no, esa consulta se almacena en result
            conn.commit()  # ejecuta la consulta preparada
        return result  # devuelvo el resultado

    def get_products(self):  # limpia pantalla, consulta db y muestra los datos
        # limpiando la tabla visible, NO la base de datos
        records = self.tree.get_children()  # este metodo obtiene todos los datos de la tabla en pantalla
        for element in records:
            self.tree.delete(element)
        # consultando la base de datos
        query = 'SELECT * FROM product ORDER BY name DESC'  # selecionar desde la tabla ordenados por nombre desc
        db_rows = self.run_query(query)  # cuando ejecuto la consulta, devuelve las filas
        # recorriendo y mostrando los datos
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=row[2])  # el primer parametro vacio y el 0 no se, luego le sigue lo que quiero imprimir

    def validation(self):  # permite validar que el name y price no esten en cero cuando se guarde el nuevo product
        return len(self.name.get()) != 0 and len(self.price.get()) != 0  # con el get se toma solo lo que el user ingresa dentro de input

    def add_products(self):  # permite agregar productos a la db
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'  # le aviso a la db que voy a insertar tres valores
            parameters = (self.name.get(), self.price.get())  # defino los parametros que metere en los signos de pregunta
            self.run_query(query, parameters)
            self.message['text'] = 'Producto {} agregado satisfactoriamente'.format(self.name.get())  # llamamos la funcion message y en la propiedad text le pasamos lo que esta en {} llamandolo con .format
            self.name.delete(0, END)  # vaciamos los inputs
            self.price.delete(0, END)  # vaciamos los inputs

        else:
            self.message['text'] = 'Precio y nombre requerido'  # cartel cuando no se carga precio ni nombre
        self.get_products()  # llamos a la fucnion que actualiza la planilla en la interfaz grafica

    def delete_product(self):  # borra un producto
        self.message['text'] = ''  # para que limpie el mensaje de pantalla
        try:  # si el item esta seleccionado
            self.tree.item(self.tree.selection())['text'][0]  # dentro de la tabla, seleccionar el texto y el indice cero
        except:  # si no selecciono ningun item
            self.message['text'] = 'Por favor, seleccione un articulo'
            return  # para que termine la ejecucion del except
        self.message['text'] = ''  # para que limpie el mensaje de pantalla
        name = self.tree.item(self.tree.selection())['text']  # guardo el texto seleccionado en una variable
        query = 'DELETE FROM product WHERE name = ?'  # escribo la consulta a la db
        self.run_query(query, (name, ))  # ejecuto la funcion que hace las consultas pasando como parametro el name que es el articulo seleccionado, con la coma digo que es una
        self.message['text'] = 'El articulo {} ha sido borrado con exito'.format(name)  # texto en pantalla
        self.get_products()  # para que la tabla en al grafica se actualice
    
    def edit_product(self):
        self.message['text'] = ''  # para que limpie el mensaje de pantalla
        try:  # si el item esta seleccionado
            self.tree.item(self.tree.selection())['text'][0]  # dentro de la tabla, seleccionar el texto y el indice cero
        except:  # si no selecciono ningun item
            self.message['text'] = 'Por favor, seleccione un articulo'
            return  # para que termine la ejecucion del except
        name = self.tree.item(self.tree.selection())['text']  # obtengo el nombre actual del articulo seleccionado
        old_price = self.tree.item(self.tree.selection())['values'][0]  # obtengo el precioo actual del articulo seleccionado en el indice 0
        self.edit_window = Toplevel()  # el metodo top level crea una ventana desde una existente
        self.edit_window.title = 'Editar producto'  # titulo de la nueva ventana

        # nombre anterior
        Label(self.edit_window, text='Nombre antiguo: ').grid(row=0, column=1)  # una etiqueta para senialar el valor que se va a mostrar
        Entry(self.edit_window, textvariable=StringVar(self.edit_window, value=name), state='readonly').grid(row=0, column=2)  # un input, con una varible de txt tipo stg que dentro tendra el name, con el estado de solo lectura
        # nuevo nombre
        Label(self.edit_window, text='Nuevo nombre: ').grid(row=1, column=1)  # posicionando la etiqueta de diga nuevo nombre
        new_name = Entry(self.edit_window)  # crendo la caja de texto para el ingreso
        new_name.grid(row=1, column=2)  # posicionando la caja de texto

        # precio anterior
        Label(self.edit_window, text='Precio antiguo: ').grid(row=2, column=1)  # una etiqueta para senialar el valor que se va a mostrar
        Entry(self.edit_window, textvariable=StringVar(self.edit_window, value=old_price), state='readonly').grid(row=2, column=2)  # un input, con una varible de int tipo stg que dentro tendra el old_price, con el estado de solo lectura
        # nuevo precio
        Label(self.edit_window, text='Nuevo precio: ').grid(row=3, column=1)  # posicionando la etiqueta de diga nuevo precio
        new_price = Entry(self.edit_window)  # crendo la caja de texto para el ingreso
        new_price.grid(row=3, column=2)  # posicionando la caja de texto
        # Boton agregar producto
        ttk.Button(self.edit_window, text='Guardar cambios', command=lambda:self.edit_database(new_name.get(), name, new_price.get(), old_price)).grid(row=4, columnspan=4, sticky= W + E)  # Sticky <-> screen

    def edit_database(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'  # en leguaje db le decimos que actualice el name y price, ? (valor dado) en donde estaban anteriormente
        parameters = (new_name, new_price, name, old_price)  # pongo los parametros en un variable para ser usada por la funcion run query
        self.run_query(query, parameters)  # a la funcion run query le paso los parametros y la query misma
        self.edit_window.destroy()  # hago que se cierre la window de edicion de producto
        self.message['text'] = 'El producto {} ha sido actualizado'.format(name)  # texto en pantalla
        self.get_products()  # para que la tabla en al grafica se actualice

if __name__ == "__main__":
    windows = Tk()  # ejecuta la ventana
    application = Product(windows)  # ejecuta la clase Producto pasando como parametro la ventana
    windows.mainloop()  # permite el uso de la ventana
