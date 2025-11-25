import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
from datetime import datetime
import webbrowser
import tempfile

# Constantes
IVA = 0.15

# Base de datos ACTUALIZADA con todos los productos
productos = [
    {"codigo": "P001", "nombre": "Laptop", "precio": 800.00, "imagen": "laptop.jpeg"},
    {"codigo": "P002", "nombre": "Mouse Inalámbrico", "precio": 15.50, "imagen": "mause.jpeg"},
    {"codigo": "P003", "nombre": "Teclado Mecánico", "precio": 55.99, "imagen": "taclado.jpeg"},
    {"codigo": "P004", "nombre": "Monitor 27''", "precio": 250.00, "imagen": "monitor.png"},
    {"codigo": "P005", "nombre": "Webcam HD", "precio": 30.00, "imagen": "webcam.jpeg"},
    {"codigo": "P006", "nombre": "Router WiFi", "precio": 45.00, "imagen": "router.jpeg"},
    {"codigo": "P007", "nombre": "Switch 8 Puertos", "precio": 35.00, "imagen": "swirch.jpeg"},
    {"codigo": "P008", "nombre": "Cable Ethernet", "precio": 8.00, "imagen": "cable.jpeg"},
    {"codigo": "P009", "nombre": "Antena Externa", "precio": 25.00, "imagen": "antena.jpeg"},
    {"codigo": "P010", "nombre": "Servidor Rack", "precio": 1200.00, "imagen": "servidor.jpeg"},
    {"codigo": "P011", "nombre": "Disco Duro SSD", "precio": 89.99, "imagen": "ssd.png"},
    {"codigo": "P012", "nombre": "Memoria RAM 8GB", "precio": 45.00, "imagen": "ram.jpeg"},
    {"codigo": "P013", "nombre": "Tarjeta de Red", "precio": 22.50, "imagen": "tarjeta.jpeg"},
    {"codigo": "P014", "nombre": "UPS", "precio": 150.00, "imagen": "ups.jpeg"},
    {"codigo": "P015", "nombre": "Software Antivirus", "precio": 60.00, "imagen": "antivirus.jpeg"},
]

clientes = [
    {"ruc": "1790000000001", "nombre": "Ana García"},
    {"ruc": "0990000000001", "nombre": "Luis Pérez"}
]

facturas = []

class SistemaFacturacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Facturación")
        self.root.geometry("1200x800")  # Ventana más grande
        self.root.configure(bg='#f0f0f0')
        
        # Estilo para widgets
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10), foreground='black')
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'), foreground='black')
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='black')
        
        # Variables para la factura
        self.cliente_factura = tk.StringVar()
        self.items_factura = []
        self.subtotal_factura = tk.DoubleVar(value=0.0)
        self.iva_factura = tk.DoubleVar(value=0.0)
        self.total_factura = tk.DoubleVar(value=0.0)
        
        # Cargar imágenes redimensionadas
        self.cargar_imagenes()
        
        self.crear_interfaz()
    
    def cargar_imagenes(self):
        # Tamaño deseado para los logos
        logo_width = 80
        logo_height = 80
        
        try:
            # Logo izquierdo - redimensionado
            original_image = Image.open("img2.png")
            resized_image = original_image.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
            self.logo_left = ImageTk.PhotoImage(resized_image)
        except:
            # Si no encuentra la imagen, crea una placeholder más pequeña
            self.logo_left = tk.PhotoImage(width=logo_width, height=logo_height)
            print("No se pudo cargar logo_left.png - usando placeholder")
        
        try:
            # Logo derecho - redimensionado
            original_image = Image.open("img3.png")
            resized_image = original_image.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
            self.logo_right = ImageTk.PhotoImage(resized_image)
        except:
            # Si no encuentra la imagen, crea una placeholder más pequeña
            self.logo_right = tk.PhotoImage(width=logo_width, height=logo_height)
            print("No se pudo cargar logo_right.png - usando placeholder")
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # =============================================
        # ENCABEZADO COMPACTO CON LOGOS E INFORMACIÓN
        # =============================================
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Frame principal para header (logos + info)
        header_content = ttk.Frame(header_frame)
        header_content.pack(fill=tk.X, pady=2)
        
        # Logo izquierdo
        logo_left_label = ttk.Label(header_content, image=self.logo_left)
        logo_left_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Información de la universidad (centro) - más compacta
        info_frame = ttk.Frame(header_content)
        info_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Nombre de la universidad - texto más pequeño
        univ_label = ttk.Label(info_frame, text="UNIVERSIDAD ESTATAL PENÍNSULA DE SANTA ELENA", 
                              font=('Arial', 12, 'bold'), foreground='black')
        univ_label.pack(pady=(0, 2))
        
        # FACULTAD DE SISTEMAS Y TELECOMUNICACIONES
        facultad_label = ttk.Label(info_frame, text="FACULTAD DE SISTEMAS Y TELECOMUNICACIONES", 
                                 font=('Arial', 10, 'bold'), foreground='black')
        facultad_label.pack(pady=(0, 2))
        
        # Tecnología de la información
        tecnologia_label = ttk.Label(info_frame, text="Tecnología de la información", 
                                   font=('Arial', 9, 'bold'), foreground='black')
        tecnologia_label.pack(pady=(0, 2))
        
        # Logo derecho
        logo_right_label = ttk.Label(header_content, image=self.logo_right)
        logo_right_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Separador más delgado
        separator = ttk.Separator(header_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=5)
        
        # Título del sistema de facturación - más pequeño
        title_label = ttk.Label(main_frame, text="SISTEMA DE FACTURACIÓN", 
                               font=('Arial', 16, 'bold'), foreground='black')
        title_label.pack(pady=(0, 15))
        
        # Notebook (pestañas)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de Clientes
        self.crear_pestana_clientes(notebook)
        
        # Pestaña de Productos
        self.crear_pestana_productos(notebook)
        
        # Pestaña de Facturación
        self.crear_pestana_facturacion(notebook)
        
        # Pestaña de Historial
        self.crear_pestana_historial(notebook)
    
    def crear_pestana_clientes(self, notebook):
        # Frame para clientes
        clientes_frame = ttk.Frame(notebook)
        notebook.add(clientes_frame, text="👥 Clientes")
        
        # Título más pequeño
        ttk.Label(clientes_frame, text="GESTIÓN DE CLIENTES", 
                 font=('Arial', 14, 'bold'), foreground='black').pack(pady=8)
        
        # Frame para formulario de registro
        form_frame = ttk.Frame(clientes_frame)
        form_frame.pack(fill=tk.X, padx=20, pady=8)
        
        ttk.Label(form_frame, text="RUC/Cédula:").grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self.ruc_entry = ttk.Entry(form_frame, width=20)
        self.ruc_entry.grid(row=0, column=1, padx=5, pady=3, sticky=tk.W)
        
        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=3, sticky=tk.W)
        self.nombre_entry = ttk.Entry(form_frame, width=30)
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=3, sticky=tk.W)
        
        # Frame para botones
        botones_frame = ttk.Frame(form_frame)
        botones_frame.grid(row=2, column=0, columnspan=2, pady=8)
        
        ttk.Button(botones_frame, text="Registrar Cliente", command=self.registrar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Eliminar Cliente", command=self.eliminar_cliente).pack(side=tk.LEFT, padx=5)
        
        # Treeview para mostrar clientes
        columns = ('RUC', 'Nombre')
        self.clientes_tree = ttk.Treeview(clientes_frame, columns=columns, show='headings', height=12)
        
        # Definir encabezados
        self.clientes_tree.heading('RUC', text='RUC/Cédula')
        self.clientes_tree.heading('Nombre', text='Nombre')
        
        # Configurar columnas
        self.clientes_tree.column('RUC', width=150)
        self.clientes_tree.column('Nombre', width=300)
        
        # Scrollbar para el treeview
        scrollbar = ttk.Scrollbar(clientes_frame, orient=tk.VERTICAL, command=self.clientes_tree.yview)
        self.clientes_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.clientes_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)
        
        # Cargar datos
        self.actualizar_lista_clientes()
    
    def crear_pestana_productos(self, notebook):
        # Frame para productos
        productos_frame = ttk.Frame(notebook)
        notebook.add(productos_frame, text="📦 Productos")
        
        # Título
        ttk.Label(productos_frame, text="PRODUCTOS DISPONIBLES", 
                 font=('Arial', 14, 'bold'), foreground='black').pack(pady=8)
        
        # Frame para mostrar productos con imágenes - MEJORADO
        productos_display_frame = ttk.Frame(productos_frame)
        productos_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)
        
        # Canvas con scrollbar para productos con imágenes
        canvas = tk.Canvas(productos_display_frame, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(productos_display_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding=5)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mostrar productos en una cuadrícula MEJORADA
        self.mostrar_productos_con_imagenes_mejorado(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def mostrar_productos_con_imagenes_mejorado(self, parent_frame):
        # MEJORA: Crear una cuadrícula más compacta y organizada
        row, col = 0, 0
        max_cols = 5  # Aumentamos a 5 columnas para mejor uso del espacio
        
        # Configurar grid para que se expanda uniformemente
        for i in range(max_cols):
            parent_frame.columnconfigure(i, weight=1, uniform="group1")
        
        for producto in productos:
            # Frame para cada producto - más compacto
            producto_frame = ttk.LabelFrame(
                parent_frame, 
                text=producto['nombre'], 
                width=160,  # Más compacto para 5 columnas
                height=200  # Más compacto
            )
            producto_frame.grid(
                row=row, 
                column=col, 
                padx=4,     # Menor padding
                pady=4,     # Menor padding
                sticky="nsew"
            )
            producto_frame.grid_propagate(False)
            
            # Cargar imagen del producto (placeholder si no existe)
            try:
                # Intenta cargar desde la carpeta productos
                img_path = f"productos/{producto['imagen']}"
                if not os.path.exists(img_path):
                    # Si no existe en productos/, busca en el directorio actual
                    img_path = producto['imagen']
                
                img = Image.open(img_path)
                img = img.resize((70, 70), Image.Resampling.LANCZOS)  # Imagen más pequeña
                photo = ImageTk.PhotoImage(img)
            except Exception as e:
                # Crear imagen placeholder con información del producto
                print(f"No se pudo cargar la imagen {producto['imagen']}: {e}")
                # Crear imagen placeholder simple con texto
                img = Image.new('RGB', (70, 70), color='lightgray')
                # Agregar texto a la imagen placeholder
                from PIL import ImageDraw, ImageFont
                draw = ImageDraw.Draw(img)
                try:
                    font = ImageFont.load_default()
                    text = producto['codigo']
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    x = (70 - text_width) / 2
                    y = (70 - text_height) / 2
                    draw.text((x, y), text, fill='black', font=font)
                except:
                    draw.text((10, 25), producto['codigo'], fill='black')
                photo = ImageTk.PhotoImage(img)
            
            # Etiqueta para la imagen
            img_label = ttk.Label(producto_frame, image=photo)
            img_label.image = photo  # Guardar referencia
            img_label.pack(pady=2)  # Menor padding
            
            # Información del producto - texto más compacto
            info_frame = ttk.Frame(producto_frame)
            info_frame.pack(fill=tk.X, padx=3, pady=1)
            
            ttk.Label(info_frame, text=f"Código: {producto['codigo']}", 
                     font=('Arial', 7)).pack(anchor=tk.W)
            ttk.Label(info_frame, text=f"Precio: ${producto['precio']:.2f}", 
                     font=('Arial', 8, 'bold')).pack(anchor=tk.W)
            
            # Actualizar columnas y filas
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def crear_pestana_facturacion(self, notebook):
        # Frame para facturación
        facturacion_frame = ttk.Frame(notebook)
        notebook.add(facturacion_frame, text="📝 Facturación")
        
        # Título
        ttk.Label(facturacion_frame, text="GENERAR FACTURA", 
                 font=('Arial', 14, 'bold'), foreground='black').pack(pady=8)
        
        # Frame para selección de cliente
        cliente_frame = ttk.LabelFrame(facturacion_frame, text="Datos del Cliente")
        cliente_frame.pack(fill=tk.X, padx=20, pady=8)
        
        ttk.Label(cliente_frame, text="Seleccionar Cliente:").grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        
        # Combobox para seleccionar cliente
        self.clientes_combobox = ttk.Combobox(cliente_frame, values=[f"{c['ruc']} - {c['nombre']}" for c in clientes], 
                                             state="readonly", width=50)
        self.clientes_combobox.grid(row=0, column=1, padx=5, pady=3, sticky=tk.W)
        self.clientes_combobox.bind('<<ComboboxSelected>>', self.seleccionar_cliente)
        
        # Frame para agregar productos
        productos_frame = ttk.LabelFrame(facturacion_frame, text="Agregar Productos")
        productos_frame.pack(fill=tk.X, padx=20, pady=8)
        
        ttk.Label(productos_frame, text="Producto:").grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        
        # Combobox para seleccionar producto
        self.productos_combobox = ttk.Combobox(productos_frame, 
                                              values=[f"{p['codigo']} - {p['nombre']} - ${p['precio']:.2f}" for p in productos], 
                                              state="readonly", width=50)
        self.productos_combobox.grid(row=0, column=1, padx=5, pady=3, sticky=tk.W)
        
        ttk.Label(productos_frame, text="Cantidad:").grid(row=1, column=0, padx=5, pady=3, sticky=tk.W)
        self.cantidad_entry = ttk.Entry(productos_frame, width=10)
        self.cantidad_entry.grid(row=1, column=1, padx=5, pady=3, sticky=tk.W)
        
        ttk.Button(productos_frame, text="Agregar Producto", command=self.agregar_producto_factura).grid(row=1, column=2, padx=10, pady=3)
        
        # Treeview para productos en la factura
        columns = ('Código', 'Producto', 'Cantidad', 'Precio', 'Subtotal')
        self.factura_tree = ttk.Treeview(facturacion_frame, columns=columns, show='headings', height=8)
        
        # Definir encabezados
        self.factura_tree.heading('Código', text='Código')
        self.factura_tree.heading('Producto', text='Producto')
        self.factura_tree.heading('Cantidad', text='Cantidad')
        self.factura_tree.heading('Precio', text='Precio Unitario')
        self.factura_tree.heading('Subtotal', text='Subtotal')
        
        # Configurar columnas
        self.factura_tree.column('Código', width=80)
        self.factura_tree.column('Producto', width=200)
        self.factura_tree.column('Cantidad', width=80)
        self.factura_tree.column('Precio', width=120)
        self.factura_tree.column('Subtotal', width=120)
        
        # Scrollbar para el treeview
        scrollbar = ttk.Scrollbar(facturacion_frame, orient=tk.VERTICAL, command=self.factura_tree.yview)
        self.factura_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.factura_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)
        
        # Frame para totales
        totales_frame = ttk.Frame(facturacion_frame)
        totales_frame.pack(fill=tk.X, padx=20, pady=8)
        
        ttk.Label(totales_frame, text="Subtotal:").grid(row=0, column=0, padx=5, pady=3, sticky=tk.E)
        ttk.Label(totales_frame, textvariable=self.subtotal_factura).grid(row=0, column=1, padx=5, pady=3, sticky=tk.W)
        
        ttk.Label(totales_frame, text=f"IVA ({IVA*100:.0f}%):").grid(row=1, column=0, padx=5, pady=3, sticky=tk.E)
        ttk.Label(totales_frame, textvariable=self.iva_factura).grid(row=1, column=1, padx=5, pady=3, sticky=tk.W)
        
        ttk.Label(totales_frame, text="TOTAL:", font=('Arial', 11, 'bold')).grid(row=2, column=0, padx=5, pady=3, sticky=tk.E)
        ttk.Label(totales_frame, textvariable=self.total_factura, font=('Arial', 11, 'bold')).grid(row=2, column=1, padx=5, pady=3, sticky=tk.W)
        
        # Botones
        botones_frame = ttk.Frame(facturacion_frame)
        botones_frame.pack(fill=tk.X, padx=20, pady=8)
        
        ttk.Button(botones_frame, text="Limpiar Factura", command=self.limpiar_factura).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Generar Factura", command=self.generar_factura).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Imprimir Factura (HTML)", command=self.imprimir_factura_html).pack(side=tk.LEFT, padx=5)
    
    def crear_pestana_historial(self, notebook):
        # Frame para historial
        historial_frame = ttk.Frame(notebook)
        notebook.add(historial_frame, text="📋 Historial")
        
        # Título
        ttk.Label(historial_frame, text="HISTORIAL DE FACTURAS", 
                 font=('Arial', 14, 'bold'), foreground='black').pack(pady=8)
        
        # Frame para botones del historial
        botones_frame = ttk.Frame(historial_frame)
        botones_frame.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Button(botones_frame, text="Ver Detalles de Factura", command=self.ver_detalles_factura).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Eliminar Factura", command=self.eliminar_factura).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Limpiar Historial", command=self.limpiar_historial).pack(side=tk.LEFT, padx=5)
        
        # Treeview para mostrar facturas
        columns = ('N°', 'Cliente', 'RUC', 'Fecha', 'Total')
        self.historial_tree = ttk.Treeview(historial_frame, columns=columns, show='headings', height=12)
        
        # Definir encabezados
        self.historial_tree.heading('N°', text='N° Factura')
        self.historial_tree.heading('Cliente', text='Cliente')
        self.historial_tree.heading('RUC', text='RUC')
        self.historial_tree.heading('Fecha', text='Fecha')
        self.historial_tree.heading('Total', text='Total ($)')
        
        # Configurar columnas
        self.historial_tree.column('N°', width=80)
        self.historial_tree.column('Cliente', width=200)
        self.historial_tree.column('RUC', width=120)
        self.historial_tree.column('Fecha', width=100)
        self.historial_tree.column('Total', width=100)
        
        # Scrollbar para el treeview
        scrollbar = ttk.Scrollbar(historial_frame, orient=tk.VERTICAL, command=self.historial_tree.yview)
        self.historial_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.historial_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)
    
    def actualizar_lista_clientes(self):
        # Limpiar treeview
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)
        
        # Agregar clientes
        for cliente in clientes:
            self.clientes_tree.insert('', tk.END, values=(cliente['ruc'], cliente['nombre']))
    
    def registrar_cliente(self):
        ruc = self.ruc_entry.get().strip()
        nombre = self.nombre_entry.get().strip().title()
        
        if not ruc or not nombre:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        # Verificar si el cliente ya existe
        if any(c['ruc'] == ruc for c in clientes):
            messagebox.showerror("Error", "El cliente ya existe")
            return
        
        # Agregar cliente
        clientes.append({"ruc": ruc, "nombre": nombre})
        
        # Actualizar lista
        self.actualizar_lista_clientes()
        
        # Actualizar combobox en facturación
        self.clientes_combobox['values'] = [f"{c['ruc']} - {c['nombre']}" for c in clientes]
        
        # Limpiar campos
        self.ruc_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        
        messagebox.showinfo("Éxito", "Cliente registrado correctamente")
    
    def eliminar_cliente(self):
        # CORRECCIÓN COMPLETA - Función simplificada y robusta
        global clientes
        
        seleccion = self.clientes_tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un cliente para eliminar")
            return
        
        # Obtener el item seleccionado
        item_seleccionado = seleccion[0]
        valores = self.clientes_tree.item(item_seleccionado, 'values')
        
        if not valores or len(valores) < 2:
            messagebox.showerror("Error", "No se pudo obtener la información del cliente")
            return
        
        ruc_cliente = valores[0]  # RUC está en la primera columna
        nombre_cliente = valores[1]  # Nombre está en la segunda columna
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación", 
            f"¿Está seguro de que desea eliminar al cliente?\n\nRUC: {ruc_cliente}\nNombre: {nombre_cliente}"
        )
        
        if not respuesta:
            return
        
        # BUSCAR Y ELIMINAR EL CLIENTE
        cliente_encontrado = False
        for i, cliente in enumerate(clientes):
            if cliente['ruc'] == ruc_cliente:
                # Eliminar cliente de la lista
                cliente_eliminado = clientes.pop(i)
                cliente_encontrado = True
                break
        
        if cliente_encontrado:
            # Actualizar la lista visual
            self.actualizar_lista_clientes()
            
            # Actualizar combobox en facturación
            self.clientes_combobox['values'] = [f"{c['ruc']} - {c['nombre']}" for c in clientes]
            
            # Limpiar selección en facturación si era el cliente seleccionado
            if self.cliente_factura.get() == ruc_cliente:
                self.cliente_factura.set("")
                self.clientes_combobox.set("")
            
            messagebox.showinfo("Éxito", f"Cliente '{nombre_cliente}' eliminado correctamente")
        else:
            messagebox.showerror("Error", f"No se pudo encontrar el cliente con RUC: {ruc_cliente}")
    
    def seleccionar_cliente(self, event):
        seleccion = self.clientes_combobox.get()
        if seleccion:
            ruc = seleccion.split(" - ")[0]
            self.cliente_factura.set(ruc)
    
    def agregar_producto_factura(self):
        if not self.cliente_factura.get():
            messagebox.showerror("Error", "Primero debe seleccionar un cliente")
            return
        
        seleccion = self.productos_combobox.get()
        if not seleccion:
            messagebox.showerror("Error", "Debe seleccionar un producto")
            return
        
        try:
            cantidad = int(self.cantidad_entry.get())
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido")
            return
        
        # Obtener información del producto
        codigo = seleccion.split(" - ")[0]
        producto = next((p for p in productos if p['codigo'] == codigo), None)
        
        if producto:
            subtotal = cantidad * producto['precio']
            
            # Agregar a la lista de items
            self.items_factura.append({
                "codigo": producto['codigo'],
                "producto": producto['nombre'],
                "cantidad": cantidad,
                "precio": producto['precio'],
                "subtotal": subtotal
            })
            
            # Agregar al treeview
            self.factura_tree.insert('', tk.END, values=(
                producto['codigo'],
                producto['nombre'],
                cantidad,
                f"${producto['precio']:.2f}",
                f"${subtotal:.2f}"
            ))
            
            # Actualizar totales
            self.actualizar_totales()
            
            # Limpiar campos
            self.cantidad_entry.delete(0, tk.END)
            self.productos_combobox.set('')
            
            messagebox.showinfo("Éxito", f"Producto agregado a la factura")
    
    def actualizar_totales(self):
        subtotal = sum(item['subtotal'] for item in self.items_factura)
        iva = subtotal * IVA
        total = subtotal + iva
        
        self.subtotal_factura.set(f"${subtotal:.2f}")
        self.iva_factura.set(f"${iva:.2f}")
        self.total_factura.set(f"${total:.2f}")
    
    def limpiar_factura(self):
        self.items_factura = []
        for item in self.factura_tree.get_children():
            self.factura_tree.delete(item)
        
        self.subtotal_factura.set("$0.00")
        self.iva_factura.set("$0.00")
        self.total_factura.set("$0.00")
        self.cliente_factura.set("")
        self.clientes_combobox.set("")
    
    def generar_factura(self):
        if not self.items_factura:
            messagebox.showerror("Error", "No hay productos en la factura")
            return
        
        if not self.cliente_factura.get():
            messagebox.showerror("Error", "No se ha seleccionado un cliente")
            return
        
        # Obtener información del cliente
        ruc = self.cliente_factura.get()
        cliente = next((c for c in clientes if c['ruc'] == ruc), None)
        
        if not cliente:
            messagebox.showerror("Error", "Cliente no encontrado")
            return
        
        # Calcular totales
        subtotal = sum(item['subtotal'] for item in self.items_factura)
        iva = subtotal * IVA
        total = subtotal + iva
        
        # Crear factura
        factura = {
            "numero": len(facturas) + 1,
            "cliente": cliente,
            "items": self.items_factura.copy(),
            "subtotal": subtotal,
            "iva": iva,
            "total": total,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Agregar al historial
        facturas.append(factura)
        
        # Actualizar historial
        self.actualizar_historial()
        
        messagebox.showinfo("Éxito", f"Factura #{factura['numero']} generada correctamente")
        
        # Limpiar factura actual
        self.limpiar_factura()
    
    def actualizar_historial(self):
        # Limpiar treeview
        for item in self.historial_tree.get_children():
            self.historial_tree.delete(item)
        
        # Agregar facturas
        for factura in facturas:
            self.historial_tree.insert('', tk.END, values=(
                factura['numero'],
                factura['cliente']['nombre'],
                factura['cliente']['ruc'],
                factura['fecha'],
                f"${factura['total']:.2f}"
            ))
    
    def eliminar_factura(self):
        # CORRECCIÓN: global declarado al inicio de la función
        global facturas
        
        seleccion = self.historial_tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione una factura para eliminar")
            return
        
        # Obtener número de factura
        item = self.historial_tree.item(seleccion[0])
        numero_factura = item['values'][0]
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar esta factura?")
        if respuesta:
            # CORRECCIÓN MEJORADA: Eliminar usando bucle para mayor precisión
            factura_encontrada = False
            for i, factura in enumerate(facturas):
                if factura['numero'] == numero_factura:
                    del facturas[i]
                    factura_encontrada = True
                    break
            
            if factura_encontrada:
                # Actualizar historial
                self.actualizar_historial()
                messagebox.showinfo("Éxito", "Factura eliminada correctamente")
            else:
                messagebox.showerror("Error", "No se pudo encontrar la factura para eliminar")
    
    def limpiar_historial(self):
        # CORRECCIÓN: global declarado al inicio de la función
        global facturas
        
        if not facturas:
            messagebox.showinfo("Información", "El historial ya está vacío")
            return
        
        # Confirmar limpieza
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de que desea limpiar todo el historial?")
        if respuesta:
            facturas.clear()
            
            # Actualizar treeview
            self.actualizar_historial()
            
            messagebox.showinfo("Éxito", "Historial limpiado correctamente")
    
    def ver_detalles_factura(self):
        seleccion = self.historial_tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione una factura para ver los detalles")
            return
        
        # Obtener número de factura
        item = self.historial_tree.item(seleccion[0])
        numero_factura = item['values'][0]
        
        # Buscar factura
        factura = next((f for f in facturas if f['numero'] == numero_factura), None)
        
        if factura:
            # Crear ventana de detalles
            detalles_window = tk.Toplevel(self.root)
            detalles_window.title(f"Detalles de Factura #{factura['numero']}")
            detalles_window.geometry("600x500")
            detalles_window.configure(bg='#f0f0f0')
            
            # Título
            ttk.Label(detalles_window, text=f"FACTURA #{factura['numero']}", 
                     font=('Arial', 16, 'bold'), foreground='black').pack(pady=10)
            
            # Información del cliente
            info_frame = ttk.LabelFrame(detalles_window, text="Información del Cliente")
            info_frame.pack(fill=tk.X, padx=20, pady=10)
            
            ttk.Label(info_frame, text=f"Nombre: {factura['cliente']['nombre']}").pack(anchor=tk.W, padx=10, pady=5)
            ttk.Label(info_frame, text=f"RUC: {factura['cliente']['ruc']}").pack(anchor=tk.W, padx=10, pady=5)
            ttk.Label(info_frame, text=f"Fecha: {factura['fecha']}").pack(anchor=tk.W, padx=10, pady=5)
            
            # Detalles de productos
            productos_frame = ttk.LabelFrame(detalles_window, text="Detalles de Productos")
            productos_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Crear texto con formato
            texto_detalles = scrolledtext.ScrolledText(productos_frame, width=70, height=15)
            texto_detalles.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Formatear detalles
            texto_detalles.insert(tk.END, f"{'CÓDIGO':<10} {'PRODUCTO':<25} {'CANT':<8} {'PRECIO':<12} {'TOTAL':<12}\n")
            texto_detalles.insert(tk.END, "-" * 70 + "\n")
            
            for item in factura['items']:
                texto_detalles.insert(tk.END, 
                    f"{item['codigo']:<10} {item['producto']:<25} {item['cantidad']:<8} ${item['precio']:<11.2f} ${item['subtotal']:<11.2f}\n")
            
            texto_detalles.insert(tk.END, "-" * 70 + "\n")
            texto_detalles.insert(tk.END, f"SUBTOTAL: ${factura['subtotal']:>52.2f}\n")
            texto_detalles.insert(tk.END, f"IVA ({IVA*100:.0f}%): ${factura['iva']:>50.2f}\n")
            texto_detalles.insert(tk.END, f"TOTAL: ${factura['total']:>55.2f}\n")
            
            texto_detalles.config(state=tk.DISABLED)
    
    def imprimir_factura_html(self):
        if not self.items_factura:
            messagebox.showerror("Error", "No hay productos en la factura para imprimir")
            return
        
        if not self.cliente_factura.get():
            messagebox.showerror("Error", "No se ha seleccionado un cliente")
            return
        
        # Obtener información del cliente
        ruc = self.cliente_factura.get()
        cliente = next((c for c in clientes if c['ruc'] == ruc), None)
        
        if not cliente:
            messagebox.showerror("Error", "Cliente no encontrado")
            return
        
        # Calcular totales
        subtotal = sum(item['subtotal'] for item in self.items_factura)
        iva = subtotal * IVA
        total = subtotal + iva
        
        # Ruta específica para guardar la factura
        ruta_guardado = r"C:\Users\JOSE LUIS\Desktop\proyecto\jueves"
        
        # Verificar si la carpeta existe, si no, crearla
        if not os.path.exists(ruta_guardado):
            try:
                os.makedirs(ruta_guardado)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear la carpeta: {e}")
                return
        
        # Crear archivo HTML en la ruta específica
        nombre_archivo = f"factura_{len(facturas) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        html_path = os.path.join(ruta_guardado, nombre_archivo)
        
        # Generar contenido HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Factura #{len(facturas) + 1}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; }}
                .info {{ margin: 20px 0; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .totals {{ text-align: right; margin-top: 20px; }}
                .total {{ font-weight: bold; font-size: 1.2em; }}
                .footer {{ margin-top: 40px; text-align: center; font-style: italic; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>FACTURA #{len(facturas) + 1}</h1>
                <h2>Sistema de Facturación</h2>
            </div>
            
            <div class="info">
                <p><strong>Cliente:</strong> {cliente['nombre']}</p>
                <p><strong>RUC:</strong> {cliente['ruc']}</p>
                <p><strong>Fecha:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>Código</th>
                        <th>Producto</th>
                        <th>Cantidad</th>
                        <th>Precio Unitario</th>
                        <th>Subtotal</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        # Agregar productos a la tabla
        for item in self.items_factura:
            html_content += f"""
                    <tr>
                        <td>{item['codigo']}</td>
                        <td>{item['producto']}</td>
                        <td>{item['cantidad']}</td>
                        <td>${item['precio']:.2f}</td>
                        <td>${item['subtotal']:.2f}</td>
                    </tr>
            """
        
        # Agregar totales
        html_content += f"""
                </tbody>
            </table>
            
            <div class="totals">
                <p><strong>Subtotal:</strong> ${subtotal:.2f}</p>
                <p><strong>IVA ({IVA*100:.0f}%):</strong> ${iva:.2f}</p>
                <p class="total"><strong>TOTAL:</strong> ${total:.2f}</p>
            </div>
            
            <div class="footer">
                <p><em>¡Gracias por su compra!</em></p>
                <p><small>Factura generada automáticamente por el Sistema de Facturación</small></p>
            </div>
        </body>
        </html>
        """
        
        # Guardar archivo HTML
        try:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Abrir en el navegador
            webbrowser.open(html_path)
            messagebox.showinfo("Éxito", f"Factura guardada en:\n{html_path}")
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la factura: {e}")
    
    def buscar_por_codigo(self, codigo):
        return next((producto for producto in productos if producto['codigo'] == codigo), None)
    
    def buscar_por_ruc(self, ruc):
        return next((cliente for cliente in clientes if cliente['ruc'] == ruc), None)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaFacturacion(root)
    root.mainloop()
