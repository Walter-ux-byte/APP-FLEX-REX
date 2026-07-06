from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle, Line
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton, MDFillRoundFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import platform
from kivy.metrics import dp
import os
import math
import json

try:
    from plyer import accelerometer
except ImportError:
    accelerometer = None

if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.CAMERA])

DATOS_USUARIO = {
    "nombre": "",
    "edad": "",
    "sexo": "Seleccionar...",
    "altura": "",
    "peso": "",
    "ejercicio": None,
    "plan_sugerido": None,
    "membresia": "Gratis",
    "membresia_activa": False
}

COLOR_AMARILLO = (1, 0.84, 0, 1)
COLOR_BLANCO = (1, 1, 1, 1)
CONTENIDO_PLANES = {
    "Premium Mensual": "Incluye:\n- Todos los ejercicios\n- Historial ilimitado\n- Rutinas personalizadas con IA",
    "Premium Anual": "Incluye:\n- Todo lo del plan mensual\n- Ahorro del 33%\n- Soporte prioritario",
    "Gratis": "Incluye:\n- 3 ejercicios básicos\n- Historial limitado\n- Sin rutinas personalizadas"
}

def get_userdata_path():
    if platform == "android" and App.get_running_app():
        base_dir = App.get_running_app().user_data_dir
    else:
        base_dir = os.path.dirname(__file__)
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, "userdata.json")

def save_user_data():
    path = get_userdata_path()
    try:
        with open(path, "w", encoding="utf-8") as archivo:
            json.dump(DATOS_USUARIO, archivo, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[FlexRex] Error guardando: {e}")

def load_user_data():
    path = get_userdata_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            if isinstance(datos, dict):
                DATOS_USUARIO.update(datos)
        except Exception as e:
            print(f"[FlexRex] Error leyendo: {e}")

def animar_boton_en_movimiento(boton, delay=0):
    if getattr(boton, "_animacion_movimiento_activa", False):
        return boton
    boton._animacion_movimiento_activa = True
    def iniciar_animacion(dt):
        anim = Animation(opacity=0.85, duration=0.8, t='in_out_sine') + Animation(opacity=1, duration=0.8, t='in_out_sine')
        anim.repeat = True
        anim.start(boton)
    Clock.schedule_once(iniciar_animacion, delay)
    return boton

def animar_botones_en_layout(layout, delay_base=0.04):
    botones = (MDRaisedButton, MDFlatButton, MDIconButton, MDFillRoundFlatButton)
    delay = 0
    for widget in layout.walk():
        if isinstance(widget, botones):
            animar_boton_en_movimiento(widget, delay)
            delay += delay_base

# PANTALLA 1: BIENVENIDA (Ajustada para que no se encima con barras del teléfono)
class PantallaBienvenida(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout_pantalla = FloatLayout()
        
        self.logo = Image(
            source="logo_cropped.png", 
            size_hint=(0.9, 0.45),
            pos_hint={"center_x": 0.5, "center_y": 0.60},
            fit_mode="contain"
        )
        layout_pantalla.add_widget(self.logo)
        
        # Textos con alturas fijas controladas
        layout_pantalla.add_widget(MDLabel(
            text="FLEX-REX", halign="center", font_style="H3", bold=True,
            theme_text_color="Custom", text_color=(1, 1, 1, 1),
            size_hint=(1, None), height=dp(50), pos_hint={"center_x": 0.5, "top": 0.95}
        ))
        layout_pantalla.add_widget(MDLabel(
            text="Tu entrenador personal dinámico", halign="center", font_style="Subtitle1",
            theme_text_color="Custom", text_color=(0.85, 0.85, 0.85, 1),
            size_hint=(1, None), height=dp(30), pos_hint={"center_x": 0.5, "top": 0.88}
        ))
        
        # Bloque inferior de botones ordenados de abajo hacia arriba de forma segura
        self.btn_comenzar = MDFillRoundFlatButton(
            text="Comenzar Ahora", 
            pos_hint={"center_x": 0.5, "center_y": 0.22},
            size_hint=(0.85, None), height=dp(54),
            md_bg_color=(1, 0.2, 0.2, 1), font_size="18sp",
            on_release=lambda x: self.ir_a_registro()
        )
        layout_pantalla.add_widget(self.btn_comenzar)
        
        btn_planes = MDFillRoundFlatButton(
            text="Ver Planes Premium",
            pos_hint={"center_x": 0.5, "center_y": 0.10},
            size_hint=(0.85, None), height=dp(48),
            md_bg_color=COLOR_AMARILLO, text_color=(0,0,0,1), font_size="16sp",
            on_release=lambda x: self.ir_a_membresias()
        )
        layout_pantalla.add_widget(btn_planes)
        
        btn_perfil = MDIconButton(
            icon="account-circle", icon_size="32sp",
            pos_hint={"right": 0.96, "top": 0.96},
            theme_text_color="Custom", text_color=(1, 1, 1, 1),
            on_release=lambda x: self.ir_a_perfil()
        )
        layout_pantalla.add_widget(btn_perfil)
        
        self.add_widget(layout_pantalla)
        animar_botones_en_layout(layout_pantalla)

    def ir_a_registro(self):
        self.manager.transition.direction = "left"
        self.manager.current = "registro"

    def ir_a_membresias(self):
        self.manager.transition.direction = "left"
        self.manager.current = "membresias"

    def ir_a_perfil(self):
        self.manager.transition.direction = "left"
        self.manager.current = "perfil"


# PANTALLA 2: REGISTRO (Usa ScrollView dinámico para prevenir que el teclado encime campos)
class PantallaRegistro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout_pantalla = FloatLayout()
        
        scroll = ScrollView(size_hint=(1, 0.88), pos_hint={"x": 0, "y": 0})
        layout_principal = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(18), size_hint_y=None)
        layout_principal.bind(minimum_height=layout_principal.setter('height'))
        
        layout_principal.add_widget(MDLabel(
            text="¡Bienvenido!\nCuéntanos un poco sobre ti", 
            halign="center", font_style="H5", size_hint_y=None, height=dp(60)
        ))
        
        self.txt_nombre = MDTextField(hint_text="¿Cómo te llamas?", size_hint_y=None, height=dp(50), mode="rectangle", icon_left="account")
        self.txt_edad = MDTextField(hint_text="¿Qué edad tienes?", size_hint_y=None, height=dp(50), mode="rectangle", icon_left="calendar")
        self.txt_altura = MDTextField(hint_text="Altura (cm)", size_hint_y=None, height=dp(50), mode="rectangle", icon_left="human-male-height")
        self.txt_peso = MDTextField(hint_text="Peso (kg)", size_hint_y=None, height=dp(50), mode="rectangle", icon_left="weight")
        
        layout_principal.add_widget(self.txt_nombre)
        layout_principal.add_widget(self.txt_edad)
        layout_principal.add_widget(self.txt_altura)
        layout_principal.add_widget(self.txt_peso)
        
        layout_sexo = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None, height=dp(70))
        layout_sexo.add_widget(MDLabel(text="Sexo:", font_style="Caption", theme_text_color="Secondary", size_hint_y=None, height=dp(15)))
        
        self.btn_sexo_dropdown = MDFillRoundFlatButton(
            text=DATOS_USUARIO["sexo"], size_hint=(1, None), height=dp(45), 
            md_bg_color=(0.2, 0.2, 0.2, 1), on_release=self.abrir_menu_sexo
        )
        layout_sexo.add_widget(self.btn_sexo_dropdown)
        layout_principal.add_widget(layout_sexo)
        
        opciones = ["Masculino", "Femenino", "Prefiero no decirlo"]
        self.menu_sexo = MDDropdownMenu(
            caller=self.btn_sexo_dropdown,
            items=[{"text": op, "viewclass": "OneLineListItem", "on_release": lambda x=op: self.cambiar_sexo(x)} for op in opciones],
            width_mult=4,
        )
        
        btn_siguiente = MDFillRoundFlatButton(
            text="Continuar", size_hint=(0.9, None), height=dp(50),
            pos_hint={"center_x": 0.5}, md_bg_color=(1, 0.2, 0.2, 1), on_release=lambda x: self.ir_a_sugerencia()
        )
        layout_principal.add_widget(btn_siguiente)
        
        scroll.add_widget(layout_principal)
        layout_pantalla.add_widget(scroll)
        
        self.btn_regresar_flotante = MDIconButton(
            icon="arrow-left", md_bg_color=(0.25, 0.25, 0.25, 1),     
            pos_hint={"x": 0.04, "top": 0.98}, on_release=lambda x: self.regresar_pantalla()
        )
        layout_pantalla.add_widget(self.btn_regresar_flotante)
        self.add_widget(layout_pantalla)

    def abrir_menu_sexo(self, boton):
        self.menu_sexo.open()

    def cambiar_sexo(self, sexo_elegido):
        self.btn_sexo_dropdown.text = sexo_elegido
        DATOS_USUARIO["sexo"] = sexo_elegido
        self.menu_sexo.dismiss()

    def regresar_pantalla(self):
        self.manager.transition.direction = "right"
        self.manager.current = "bienvenida"

    def ir_a_sugerencia(self):
        DATOS_USUARIO["nombre"] = self.txt_nombre.text if self.txt_nombre.text else "Anónimo"
        DATOS_USUARIO["edad"] = self.txt_edad.text if self.txt_edad.text else "25"
        DATOS_USUARIO["altura"] = self.txt_altura.text if self.txt_altura.text else "170"
        DATOS_USUARIO["peso"] = self.txt_peso.text if self.txt_peso.text else "70"
        self.manager.transition.direction = "left"
        self.manager.current = "sugerencia"


# PANTALLA 3: SUGERENCIA DE PLAN (Protegida contra desbordamientos)
class PantallaSugerenciaPlan(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plan_generado = None
        
    def on_enter(self, *args):
        self.generar_plan_personalizado()
    
    def generar_plan_personalizado(self):
        altura = DATOS_USUARIO["altura"]
        peso = DATOS_USUARIO["peso"]
        try:
            imc = float(peso) / ((float(altura) / 100) ** 2)
        except ZeroDivisionError:
            imc = 22.0
        
        if imc < 18.5:
            self.plan_generado = {"objetivo": "Ganar masa muscular", "ejercicio_recomendado": "Sentadillas", "repeticiones": "Meta: 10 repeticiones", "consejo": "Enfócate en la técnica baja."}
        elif imc < 25:
            self.plan_generado = {"objetivo": "Mantener y tonificar", "ejercicio_recomendado": "Flexiones", "repeticiones": "Meta: 15 repeticiones", "consejo": "Controla el descenso suave."}
        else:
            self.plan_generado = {"objetivo": "Acondicionamiento", "ejercicio_recomendado": "Sentadillas", "repeticiones": "Meta: 12 repeticiones", "consejo": "Mantén la espalda recta."}
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        layout_pantalla = FloatLayout()
        
        layout_principal = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint=(1, 0.9), pos_hint={"center_x":0.5, "top":0.95})
        
        layout_principal.add_widget(MDLabel(text=f"Plan para {DATOS_USUARIO['nombre']}", halign="center", font_style="H5", bold=True, size_hint_y=None, height=dp(40)))
        
        card_plan = MDCard(orientation='vertical', padding=dp(20), spacing=dp(10), size_hint=(1, 0.65), md_bg_color=(0.1, 0.1, 0.15, 1), radius=[20])
        card_plan.add_widget(MDLabel(text="RECOMENDACIÓN IA", font_style="Caption", bold=True, text_color=(0, 0.8, 1, 1), theme_text_color="Custom", size_hint_y=None, height=dp(20)))
        card_plan.add_widget(MDLabel(text=f"Objetivo: {self.plan_generado['objetivo']}", font_style="Subtitle1", size_hint_y=None, height=dp(30)))
        card_plan.add_widget(MDLabel(text=f"SUGERIDO: {self.plan_generado['ejercicio_recomendado']}", font_style="H6", bold=True, text_color=(1,0.5,0.2,1), theme_text_color="Custom", size_hint_y=None, height=dp(35)))
        card_plan.add_widget(MDLabel(text=f"{self.plan_generado['repeticiones']}", font_style="Body1", size_hint_y=None, height=dp(30)))
        card_plan.add_widget(MDLabel(text=f"Consejo: {self.plan_generado['consejo']}", font_style="Body2", theme_text_color="Secondary"))
        layout_principal.add_widget(card_plan)
        
        # Contenedor horizontal seguro para botones inferiores
        contenedor_botones = BoxLayout(orientation='horizontal', spacing=dp(15), size_hint_y=None, height=dp(50))
        btn_aceptar = MDFillRoundFlatButton(text="Aceptar Plan", size_hint=(0.5, 1), md_bg_color=(0.1, 0.7, 0.1, 1), on_release=lambda x: self.aceptar_plan())
        btn_omitir = MDFlatButton(text="Elegir Yo", size_hint=(0.5, 1), theme_text_color="Custom", text_color=(0.8, 0.8, 0.8, 1), on_release=lambda x: self.omitir_plan())
        contenedor_botones.add_widget(btn_omitir)
        contenedor_botones.add_widget(btn_aceptar)
        layout_principal.add_widget(contenedor_botones)
        
        layout_pantalla.add_widget(layout_principal)
        self.add_widget(layout_pantalla)
        animar_botones_en_layout(layout_pantalla)

    def aceptar_plan(self):
        DATOS_USUARIO["plan_sugerido"] = self.plan_generado
        DATOS_USUARIO["ejercicio"] = self.plan_generado['ejercicio_recomendado']
        self.ir_a_ejercicios()
    
    def omitir_plan(self):
        DATOS_USUARIO["plan_sugerido"] = None
        DATOS_USUARIO["ejercicio"] = None
        self.ir_a_ejercicios()
    
    def ir_a_ejercicios(self):
        self.manager.transition.direction = "left"
        self.manager.current = "ejercicios"


# PANTALLA 4: SELECCIÓN DE EJERCICIOS (Sección de imágenes y tutorial con Scroll)
class PantallaEjercicios(Screen):
    def on_enter(self, *args):
        self.actualizar_resumen()
        if DATOS_USUARIO["plan_sugerido"]:
            self.lbl_titulo.text = "Plan recomendado por la IA activo"
            self.container_botones.size_hint_y = None
            self.container_botones.height = 0
            self.container_botones.opacity = 0
            self.mostrar_video_tutorial(DATOS_USUARIO["ejercicio"])
        else:
            self.lbl_titulo.text = "¿Qué vas a entrenar hoy?"
            self.container_botones.size_hint_y = None
            self.container_botones.height = dp(140)
            self.container_botones.opacity = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout_pantalla = FloatLayout()
        
        scroll = ScrollView(size_hint=(1, 0.88), pos_hint={"x": 0, "y": 0})
        layout_principal = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint_y=None)
        layout_principal.bind(minimum_height=layout_principal.setter('height'))
        
        self.lbl_resumen = MDLabel(text="", halign="center", font_style="Subtitle2", theme_text_color="Secondary", size_hint_y=None, height=dp(25))
        layout_principal.add_widget(self.lbl_resumen)
        
        self.lbl_titulo = MDLabel(text="", halign="center", font_style="H6", bold=True, size_hint_y=None, height=dp(30))
        layout_principal.add_widget(self.lbl_titulo)
        
        # Grid de selección de ejercicios usando imágenes seguras
        self.container_botones = GridLayout(cols=3, spacing=dp(10), size_hint_y=None, height=dp(140))
        
        def crear_tarjeta_ejercicio(titulo, img_source, callback):
            card = MDCard(orientation="vertical", padding=dp(5), spacing=dp(5), size_hint_y=None, height=dp(130), md_bg_color=(0.15, 0.15, 0.15, 1), radius=[15])
            img = Image(source=img_source, fit_mode="contain", size_hint_y=0.7)
            card.add_widget(img)
            card.add_widget(MDLabel(text=titulo, font_style="Caption", bold=True, halign="center", size_hint_y=0.3))
            card.bind(on_release=lambda x: callback(titulo, card))
            return card

        self.btn_dominadas = crear_tarjeta_ejercicio("Dominadas", "img_dominadas.png", self.seleccionar_ejercicio)
        self.btn_flexiones = crear_tarjeta_ejercicio("Flexiones", "img_flexiones.png", self.seleccionar_ejercicio)
        self.btn_sentadillas = crear_tarjeta_ejercicio("Sentadillas", "img_sentadillas.png", self.seleccionar_ejercicio)
        
        self.container_botones.add_widget(self.btn_dominadas)
        self.container_botones.add_widget(self.btn_flexiones)
        self.container_botones.add_widget(self.btn_sentadillas)
        layout_principal.add_widget(self.container_botones)
        
        # Bloque dinámico donde se simula el Video/Instrucciones de entrenamiento
        self.container_video = BoxLayout(orientation='vertical', size_hint_y=None, height=0, opacity=0)
        layout_principal.add_widget(self.container_video)
        
        self.btn_entrenar = MDFillRoundFlatButton(
            text="Iniciar Entrenamiento Móvil", size_hint=(0.9, None), height=dp(50), 
            pos_hint={"center_x": 0.5}, md_bg_color=(0.1, 0.6, 0.1, 1),
            on_release=lambda x: self.comenzar_entrenamiento_camara()
        )
        layout_principal.add_widget(self.btn_entrenar)
        
        scroll.add_widget(layout_principal)
        layout_pantalla.add_widget(scroll)
        
        self.btn_regresar_flotante = MDIconButton(
            icon="arrow-left", md_bg_color=(0.25, 0.25, 0.25, 1),
            pos_hint={"x": 0.04, "top": 0.98}, on_release=lambda x: self.regresar_pantalla()
        )
        layout_pantalla.add_widget(self.btn_regresar_flotante)
        self.add_widget(layout_pantalla)

    def actualizar_resumen(self):
        ej = DATOS_USUARIO['ejercicio'] or "Ninguno"
        self.lbl_resumen.text = f"Atleta: {DATOS_USUARIO['nombre']} | Ejercicio: {ej}"

    def regresar_pantalla(self):
        self.manager.transition.direction = "right"
        if DATOS_USUARIO["plan_sugerido"]:
            self.manager.current = "sugerencia"
        else:
            self.manager.current = "registro"

    def seleccionar_ejercicio(self, ejercicio, boton_pulsado):
        DATOS_USUARIO["ejercicio"] = ejercicio
        self.actualizar_resumen()
        for btn in [self.btn_dominadas, self.btn_flexiones, self.btn_sentadillas]:
            btn.md_bg_color = (0.15, 0.15, 0.15, 1)
        boton_pulsado.md_bg_color = (0.4, 0.15, 0.15, 1) 
        self.mostrar_video_tutorial(ejercicio)

    def mostrar_video_tutorial(self, ejercicio):
        self.container_video.clear_widgets()
        self.container_video.height = dp(240)
        self.container_video.opacity = 1
        
        instrucciones = {
            "Dominadas": ["1. Palmas hacia afuera.", "2. Brazos extendidos al colgar.", "3. Pasa la barbilla sobre la barra."],
            "Flexiones": ["1. Manos al ancho de hombros.", "2. Cuerpo recto como tabla.", "3. Baja el pecho controlado."],
            "Sentadillas": ["1. Pies al ancho de hombros.", "2. Baja la cadera hacia atrás.", "3. Rodillas sin pasar la punta."]
        }
        
        card_vid = MDCard(orientation='vertical', padding=dp(12), spacing=dp(8), radius=[15], md_bg_color=(0.1, 0.1, 0.12, 1), size_hint_y=None, height=dp(230))
        card_vid.add_widget(MDLabel(text=f"Guía Técnica: {ejercicio}", font_style="Subtitle1", bold=True, text_color=(1, 0.4, 0.4, 1), theme_text_color="Custom", size_hint_y=None, height=dp(25)))
        
        bloque_guia = BoxLayout(orientation='vertical', spacing=dp(4))
        pasos = instrucciones.get(ejercicio, ["Selecciona un ejercicio."])
        for paso in pasos:
            bloque_guia.add_widget(MDLabel(text=paso, font_style="Body2", theme_text_color="Primary"))
        
        bloque_guia.add_widget(MDLabel(text="* Simulación de video optimizada para ahorrar batería en Android.", font_style="Caption", theme_text_color="Secondary"))
        card_vid.add_widget(bloque_guia)
        self.container_video.add_widget(card_vid)

    def comenzar_entrenamiento_camara(self):
        if not DATOS_USUARIO["ejercicio"]:
            dialog = MDDialog(title="⚠️ Selección vacía", text="Elige un ejercicio antes de empezar.", buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())])
            dialog.open()
            return
        self.manager.transition.direction = "left"
        self.manager.current = "entrenamiento_activo"


# PANTALLA 5: MONITOR DE ENTRENAMIENTO (Distribución 55% Escáner, 45% Panel)
class PantallaEntrenamiento(Screen):
    UMBRALES = {
        "Flexiones":   {"pico": 12.2, "valle": 8.8},
        "Dominadas":   {"pico": 12.8, "valle": 8.2},
        "Sentadillas": {"pico": 13.2, "valle": 8.8},
    }

    def on_enter(self, *args):
        ejercicio = DATOS_USUARIO["ejercicio"] or "Sentadillas"
        self.lbl_ejercicio.text = f"ÁREA DE ENTRENAMIENTO: {str(ejercicio).upper()}"
        self.contador_reps = 0
        self.lbl_contador.text = "0"
        self.estado_fase = "arriba"
        self.umbral = self.UMBRALES.get(ejercicio, self.UMBRALES["Sentadillas"])
        self.scanner_line_y = 0

        self.scanner_event = Clock.schedule_interval(self.actualizar_escaneo, 1 / 30.0)
        self.text_event = Clock.schedule_interval(self.actualizar_texto_ia, 2.5)

        if accelerometer:
            try:
                accelerometer.enable()
                self.sensor_disponible = True
            except Exception:
                self.sensor_disponible = False
                self.lbl_ejercicio.text = "Modo: Botones Manuales Activos"
        else:
            self.sensor_disponible = False
            self.lbl_ejercicio.text = "Modo: Botones Manuales Activos"

        Clock.schedule_interval(self.leer_sensor, 1.0 / 20.0)

    def on_leave(self, *args):
        Clock.unschedule(self.leer_sensor)
        if self.scanner_event: self.scanner_event.cancel()
        if self.text_event: self.text_event.cancel()
        if accelerometer and self.sensor_disponible:
            try: accelerometer.disable()
            except Exception: pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sensor_disponible = False
        self.scanner_event = None
        self.text_event = None
        self.text_index = 0
        layout = FloatLayout()

        # El cuadro de simulación IA ocupa el 55% superior
        scanner_container = FloatLayout(size_hint=(1, 0.55), pos_hint={"center_x": 0.5, "top": 0.98})
        self.scanner_widget = Widget(size_hint=(0.95, 0.95), pos_hint={"center_x": 0.5, "center_y": 0.5})
        with self.scanner_widget.canvas:
            Color(0.06, 0.06, 0.1, 1)
            self.scanner_bg = Rectangle(pos=self.scanner_widget.pos, size=self.scanner_widget.size)
            Color(0, 0.6, 1, 0.3)
            self.scanner_line = Rectangle(pos=(self.scanner_widget.x, self.scanner_widget.y), size=(self.scanner_widget.width, dp(5)))
            Color(0.4, 0.7, 1, 0.2)
            self.scanner_outline = Line(rectangle=(self.scanner_widget.x, self.scanner_widget.y, self.scanner_widget.width, self.scanner_widget.height), width=1.5)
        self.scanner_widget.bind(pos=self._update_scanner_canvas, size=self._update_scanner_canvas)
        scanner_container.add_widget(self.scanner_widget)

        self.scanner_text = MDLabel(
            text="Inicializando Escáner Inteligente...", halign="center",
            theme_text_color="Custom", text_color=(0.4, 0.8, 1, 1),
            size_hint=(1, None), height=dp(30), pos_hint={"center_x": 0.5, "y": 0.06}
        )
        scanner_container.add_widget(self.scanner_text)
        layout.add_widget(scanner_container)

        # Panel de métricas ocupa el 43% inferior (Diseño modular que impide amontonamiento)
        panel_inferior = BoxLayout(orientation='vertical', size_hint=(1, 0.43), pos_hint={"x": 0, "y": 0}, padding=dp(12))
        fondo_panel = MDCard(orientation='vertical', padding=dp(12), spacing=dp(8), md_bg_color=(0.12, 0.12, 0.14, 0.98), radius=[20, 20, 0, 0])

        self.lbl_ejercicio = MDLabel(text="-", halign="center", font_style="Caption", bold=True, theme_text_color="Custom", text_color=(0, 0.8, 1, 1), size_hint_y=None, height=dp(20))
        fondo_panel.add_widget(self.lbl_ejercicio)

        layout_numeros = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(45))
        layout_numeros.add_widget(MDLabel(text="REPETICIONES:", font_style="Subtitle1", theme_text_color="Secondary", halign="left"))
        self.lbl_contador = MDLabel(text="0", font_style="H3", bold=True, halign="right", theme_text_color="Custom", text_color=(0, 0.9, 0.4, 1))
        layout_numeros.add_widget(self.lbl_contador)
        fondo_panel.add_widget(layout_numeros)

        # Botón Pro para simular con un toque
        btn_simular = MDFillRoundFlatButton(text="Simular Repetición Pasiva", md_bg_color=(0, 0.4, 0.7, 1), size_hint=(1, None), height=dp(45), on_release=lambda x: self.simular_repeticion())
        fondo_panel.add_widget(btn_simular)

        layout_ajuste = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(40))
        btn_menos = MDFillRoundFlatButton(text="-1 Corrección", md_bg_color=(0.25, 0.25, 0.25, 1), size_hint=(0.5, 1), on_release=lambda x: self.ajustar_manual(-1))
        btn_mas = MDFillRoundFlatButton(text="+1 Fuerza", md_bg_color=(0.15, 0.45, 0.2, 1), size_hint=(0.5, 1), on_release=lambda x: self.ajustar_manual(1))
        layout_ajuste.add_widget(btn_menos)
        layout_ajuste.add_widget(btn_mas)
        fondo_panel.add_widget(layout_ajuste)

        btn_terminar = MDFillRoundFlatButton(text="Finalizar y Guardar Sesión", md_bg_color=(0.8, 0.15, 0.15, 1), size_hint=(1, None), height=dp(45), on_release=lambda x: self.terminar())
        fondo_panel.add_widget(btn_terminar)

        panel_inferior.add_widget(fondo_panel)
        layout.add_widget(panel_inferior)
        self.add_widget(layout)

    def _update_scanner_canvas(self, *args):
        self.scanner_bg.pos = self.scanner_widget.pos
        self.scanner_bg.size = self.scanner_widget.size
        self.scanner_line.size = (self.scanner_widget.width, dp(5))
        self.scanner_line.pos = (self.scanner_widget.x, self.scanner_widget.y + self.scanner_line_y)
        self.scanner_outline.rectangle = (self.scanner_widget.x, self.scanner_widget.y, self.scanner_widget.width, self.scanner_widget.height)

    def actualizar_escaneo(self, dt):
        if not self.scanner_widget: return
        self.scanner_line_y += self.scanner_widget.height * dt * 0.45
        if self.scanner_line_y > self.scanner_widget.height:
            self.scanner_line_y = 0
        self.scanner_line.pos = (self.scanner_widget.x, self.scanner_widget.y + self.scanner_line_y)

    def actualizar_texto_ia(self, dt):
        textos = ["Escaneando alineación corporal...", "Ángulo articular en rango óptimo...", "Procesando repeticiones nativas...", "Postura Excelente. ¡Continúa!"]
        self.text_index = (self.text_index + 1) % len(textos)
        self.scanner_text.text = textos[self.text_index]

    def simular_repeticion(self):
        self.contador_reps += 1
        self.lbl_contador.text = str(self.contador_reps)

    def ajustar_manual(self, delta):
        self.contador_reps = max(0, self.contador_reps + delta)
        self.lbl_contador.text = str(self.contador_reps)

    def leer_sensor(self, dt):
        if not self.sensor_disponible or not accelerometer: return
        try:
            valores = accelerometer.acceleration
            if not valores or valores[0] is None: return
            x, y, z = valores[0], valores[1], valores[2]
            magnitud = math.sqrt(x*x + y*y + z*z)
            if magnitud > self.umbral["pico"] and self.estado_fase == "abajo":
                self.contador_reps += 1
                self.lbl_contador.text = str(self.contador_reps)
                self.estado_fase = "arriba"
            elif magnitud < self.umbral["valle"]:
                self.estado_fase = "abajo"
        except Exception: pass

    def terminar(self):
        dialog = MDDialog(title="¡Entrenamiento Completado!", text=f"Registraste con éxito {self.contador_reps} repeticiones en tu historial.", buttons=[MDFlatButton(text="Regresar al Menú", on_release=lambda x: self.salir_limpio(dialog))])
        dialog.open()
        save_user_data()

    def salir_limpio(self, dialogo):
        dialogo.dismiss()
        self.manager.transition.direction = "right"
        self.manager.current = "bienvenida"


# PANTALLAS COMPLEMENTARIAS: PERFIL, PROGRESO, MEMBRESÍAS, PAGO Y CONFIRMACIÓN
class PantallaPerfil(Screen):
    def on_enter(self, *args):
        self.lbl_nombre.text = DATOS_USUARIO["nombre"] if DATOS_USUARIO["nombre"] else "Atleta FlexRex"
        self.lbl_detalles.text = f"{DATOS_USUARIO['edad']} años | {DATOS_USUARIO['peso']} kg | {DATOS_USUARIO['altura']} cm"
        self.lbl_membresia.text = f"Suscripción Activa: {DATOS_USUARIO['membresia']}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        box = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        header.add_widget(MDIconButton(icon="arrow-left", on_release=lambda x: self.volver()))
        header.add_widget(MDLabel(text="Mi Perfil Deportivo", font_style="H6", bold=True))
        box.add_widget(header)

        avatar_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(140), spacing=dp(5))
        avatar_box.add_widget(MDIconButton(icon="account-circle", icon_size="64sp", pos_hint={"center_x": 0.5}, theme_text_color="Custom", text_color=(1, 0.2, 0.2, 1)))
        self.lbl_nombre = MDLabel(text="Cargando...", halign="center", font_style="H6", bold=True)
        self.lbl_detalles = MDLabel(text="-", halign="center", font_style="Body2", theme_text_color="Secondary")
        self.lbl_membresia = MDLabel(text="-", halign="center", font_style="Caption", theme_text_color="Custom", text_color=COLOR_AMARILLO)
        avatar_box.add_widget(self.lbl_nombre)
        avatar_box.add_widget(self.lbl_detalles)
        avatar_box.add_widget(self.lbl_membresia)
        box.add_widget(avatar_box)

        stats_card = MDCard(orientation='horizontal', padding=dp(12), size_hint_y=None, height=dp(70), md_bg_color=(0.15, 0.15, 0.18, 1), radius=[15])
        s1 = BoxLayout(orientation='vertical'); s1.add_widget(MDLabel(text="14", halign="center", font_style="Subtitle1", bold=True, text_color=(0, 0.8, 1, 1), theme_text_color="Custom")); s1.add_widget(MDLabel(text="Sesiones", halign="center", font_style="Caption"))
        s2 = BoxLayout(orientation='vertical'); s2.add_widget(MDLabel(text="6", halign="center", font_style="Subtitle1", bold=True, text_color=(1, 0.5, 0, 1), theme_text_color="Custom")); s2.add_widget(MDLabel(text="Racha Días", halign="center", font_style="Caption"))
        stats_card.add_widget(s1); stats_card.add_widget(s2)
        box.add_widget(stats_card)

        box.add_widget(MDFillRoundFlatButton(text="Análisis de Progreso", size_hint=(1, None), height=dp(48), md_bg_color=(0.2, 0.2, 0.22, 1), on_release=lambda x: self.ir_a_progreso()))
        box.add_widget(MDFillRoundFlatButton(text="Cambiar mi Membresía", size_hint=(1, None), height=dp(48), md_bg_color=COLOR_AMARILLO, text_color=(0,0,0,1), on_release=lambda x: self.ir_a_membresias()))
        
        box.add_widget(Widget(size_hint_y=1))
        layout.add_widget(box)
        self.add_widget(layout)

    def volver(self):
        self.manager.transition.direction = "right"; self.manager.current = "bienvenida"
    def ir_a_progreso(self):
        self.manager.transition.direction = "left"; self.manager.current = "progreso"
    def ir_a_membresias(self):
        self.manager.transition.direction = "left"; self.manager.current = "membresias"

class PantallaProgreso(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        box = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        header.add_widget(MDIconButton(icon="arrow-left", on_release=lambda x: self.volver()))
        header.add_widget(MDLabel(text="Rendimiento Semanal", font_style="H6", bold=True))
        box.add_widget(header)

        grid = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(90), spacing=dp(12))
        c1 = MDCard(orientation='vertical', padding=dp(8), md_bg_color=(0.14, 0.14, 0.16, 1), radius=[12])
        c1.add_widget(MDLabel(text="410", halign="center", font_style="H6", bold=True, text_color=(0, 0.8, 0.4, 1), theme_text_color="Custom"))
        c1.add_widget(MDLabel(text="Total Reps", halign="center", font_style="Caption"))
        c2 = MDCard(orientation='vertical', padding=dp(8), md_bg_color=(0.14, 0.14, 0.16, 1), radius=[12])
        c2.add_widget(MDLabel(text="Martes", halign="center", font_style="H6", bold=True, text_color=(1, 0.4, 0.1, 1), theme_text_color="Custom"))
        c2.add_widget(MDLabel(text="Mayor Carga", halign="center", font_style="Caption"))
        grid.add_widget(c1); grid.add_widget(c2)
        box.add_widget(grid)

        box.add_widget(MDLabel(text="Registro de Actividad Reciente", font_style="Subtitle2", bold=True, size_hint_y=None, height=dp(20)))
        historial = MDCard(orientation='vertical', padding=dp(12), spacing=dp(6), md_bg_color=(0.08, 0.08, 0.1, 1), radius=[10], size_hint_y=None, height=dp(100))
        historial.add_widget(MDLabel(text="• Hoy: Flexiones Intensas — 50 reps", font_style="Caption", theme_text_color="Secondary"))
        historial.add_widget(MDLabel(text="• Ayer: Sentadillas Libres — 70 reps", font_style="Caption", theme_text_color="Secondary"))
        historial.add_widget(MDLabel(text="• Lun: Dominadas Estrictas — 25 reps", font_style="Caption", theme_text_color="Secondary"))
        box.add_widget(historial)

        box.add_widget(Widget(size_hint_y=1))
        layout.add_widget(box)
        self.add_widget(layout)

    def volver(self):
        self.manager.transition.direction = "right"; self.manager.current = "perfil"

class PantallaMembresias(Screen):
    def on_enter(self, *args): self.actualizar_ui()
    def actualizar_ui(self):
        self.card_gratis.md_bg_color = (0.14, 0.14, 0.16, 1)
        self.card_mensual.md_bg_color = (0.13, 0.13, 0.22, 1)
        self.card_anual.md_bg_color = (0.22, 0.18, 0.1, 1)
        self.btn_gratis.text = "Seleccionar Plan"
        self.btn_mensual.text = "Adquirir Plan"
        self.btn_anual.text = "Adquirir Plan"
        if DATOS_USUARIO["membresia"] == "Gratis":
            self.card_gratis.md_bg_color = (0.25, 0.25, 0.25, 1); self.btn_gratis.text = "Plan Activo"
        elif DATOS_USUARIO["membresia"] == "Premium Mensual":
            self.card_mensual.md_bg_color = (0.18, 0.28, 0.45, 1); self.btn_mensual.text = "Plan Activo"
        elif DATOS_USUARIO["membresia"] == "Premium Anual":
            self.card_anual.md_bg_color = (0.45, 0.38, 0.1, 1); self.btn_anual.text = "Plan Activo"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        scroll = ScrollView(size_hint=(1, 0.9), pos_hint={"x": 0, "y": 0})
        box = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15), size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        header.add_widget(MDIconButton(icon="arrow-left", on_release=lambda x: self.volver()))
        header.add_widget(MDLabel(text="Suscripciones FlexRex", font_style="H6", bold=True))
        box.add_widget(header)

        # Tarjetas optimizadas en espacio horizontal y vertical para pantallas móviles pequeñas
        def build_plan_card(titulo, precio, desc, img_src, cb, is_premium=False):
            card = MDCard(orientation='horizontal', padding=dp(10), spacing=dp(10), size_hint_y=None, height=dp(160), radius=[15])
            card.add_widget(Image(source=img_src, size_hint=(0.4, 1), fit_mode="contain"))
            info = BoxLayout(orientation='vertical', spacing=dp(4), size_hint_x=0.6)
            info.add_widget(MDLabel(text=titulo, font_style="Subtitle1", bold=True, text_color=((0,0.8,1,1) if is_premium else (1,1,1,1)), theme_text_color="Custom"))
            info.add_widget(MDLabel(text=precio, font_style="Subtitle2", bold=True))
            info.add_widget(MDLabel(text=desc, font_style="Caption", theme_text_color="Secondary"))
            btn = MDFillRoundFlatButton(text="Elegir", size_hint=(1, None), height=dp(36), on_release=cb)
            info.add_widget(btn)
            card.add_widget(info)
            return card, btn

        self.card_gratis, self.btn_gratis = build_plan_card("Acceso Básico", "$0.00 / permanente", "3 Ejercicios\nHistorial local estándar", "img_plan_gratis.png", lambda x: self.seleccionar_plan("Gratis", 0))
        self.card_mensual, self.btn_mensual = build_plan_card("Premium Mensual", "$9.99 / mes", "Rutinas IA Completas\nHistorial ilimitado en nube", "img_plan_mensual.png", lambda x: self.seleccionar_plan("Premium Mensual", 9.99), True)
        self.card_anual, self.btn_anual = build_plan_card("Premium Anual", "$79.99 / año", "Beneficios completos\nAhorro neto del 33%", "img_plan_anual.png", lambda x: self.seleccionar_plan("Premium Anual", 79.99), True)
        
        box.add_widget(self.card_gratis); box.add_widget(self.card_mensual); box.add_widget(self.card_anual)
        scroll.add_widget(box); layout.add_widget(scroll)
        self.add_widget(layout)

    def volver(self):
        self.manager.transition.direction = "right"; self.manager.current = "bienvenida"
    def seleccionar_plan(self, plan, precio):
        if plan == "Gratis":
            DATOS_USUARIO["membresia"] = "Gratis"; DATOS_USUARIO["membresia_activa"] = False; self.actualizar_ui()
        else:
            DATOS_USUARIO["plan_temp"] = plan; DATOS_USUARIO["precio_temp"] = precio
            self.manager.transition.direction = "left"; self.manager.current = "pago"

class PantallaPago(Screen):
    def on_enter(self, *args):
        plan = DATOS_USUARIO.get("plan_temp", "Premium")
        precio = DATOS_USUARIO.get("precio_temp", "0.00")
        self.lbl_resumen.text = f"Suscripción: {plan} (${precio})"
        self.lbl_contenido_plan.text = CONTENIDO_PLANES.get(plan, "Acceso total.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        scroll = ScrollView(size_hint=(1, 1))
        box = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(12), size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(45))
        header.add_widget(MDIconButton(icon="arrow-left", on_release=lambda x: self.volver()))
        header.add_widget(MDLabel(text="Pasarela de Pago", font_style="H6", bold=True))
        box.add_widget(header)

        self.lbl_resumen = MDLabel(text="-", font_style="Subtitle1", text_color=(0, 0.8, 0.4, 1), theme_text_color="Custom", size_hint_y=None, height=dp(25))
        box.add_widget(self.lbl_resumen)

        card_c = MDCard(orientation="vertical", padding=dp(10), md_bg_color=(0.12, 0.12, 0.15, 1), radius=[12], size_hint_y=None, height=dp(70))
        self.lbl_contenido_plan = MDLabel(text="", font_style="Caption", theme_text_color="Primary")
        card_c.add_widget(self.lbl_contenido_plan); box.add_widget(card_c)

        self.txt_nombre = MDTextField(hint_text="Nombre del Tarjetahabiente", mode="rectangle", icon_left="account", size_hint_y=None, height=dp(45))
        self.txt_tarjeta = MDTextField(hint_text="Número de Tarjeta (16 dígitos)", mode="rectangle", icon_left="credit-card", size_hint_y=None, height=dp(45), max_text_length=16)
        
        row_fechas = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(45))
        self.txt_fecha = MDTextField(hint_text="MM/AA", mode="rectangle")
        self.txt_cvv = MDTextField(hint_text="CVV", mode="rectangle", max_text_length=3, password=True)
        row_fechas.add_widget(self.txt_fecha); row_fechas.add_widget(self.txt_cvv)

        box.add_widget(self.txt_nombre); box.add_widget(self.txt_tarjeta); box.add_widget(row_fechas)

        btn_pagar = MDFillRoundFlatButton(text="Confirmar Transacción", icon="lock", size_hint=(1, None), height=dp(48), md_bg_color=(0, 0.6, 0.3, 1), on_release=lambda x: self.procesar_pago())
        box.add_widget(btn_pagar)

        scroll.add_widget(box); layout.add_widget(scroll)
        self.add_widget(layout)

    def volver(self):
        self.manager.transition.direction = "right"; self.manager.current = "membresias"
    def procesar_pago(self):
        if not self.txt_nombre.text or len(self.txt_tarjeta.text) < 15 or not self.txt_fecha.text or not self.txt_cvv.text:
            d = MDDialog(title="Campos incompletos", text="Verifica los datos bancarios ingresados.", buttons=[MDFlatButton(text="Cerrar", on_release=lambda x: d.dismiss())])
            d.open()
            return
        DATOS_USUARIO["membresia"] = DATOS_USUARIO.get("plan_temp", "Premium")
        DATOS_USUARIO["membresia_activa"] = True
        self.manager.transition.direction = "left"; self.manager.current = "confirmacion"

class PantallaConfirmacion(Screen):
    def on_enter(self, *args):
        self.lbl_plan.text = f"Suscripción Activa: {DATOS_USUARIO['membresia']}"
        self.lbl_beneficios.text = CONTENIDO_PLANES.get(DATOS_USUARIO["membresia"], "Activado.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        box = BoxLayout(orientation='vertical', padding=dp(25), spacing=dp(15), size_hint=(1, 0.9), pos_hint={"center_x":0.5, "center_y":0.5})
        
        box.add_widget(MDIconButton(icon="check-circle", icon_size="72sp", theme_text_color="Custom", text_color=(0, 0.8, 0.3, 1), pos_hint={"center_x": 0.5}))
        box.add_widget(MDLabel(text="¡Alta Exitosa!", halign="center", font_style="H5", bold=True))
        
        self.lbl_plan = MDLabel(text="-", halign="center", font_style="Subtitle2", theme_text_color="Secondary")
        box.add_widget(self.lbl_plan)

        card_b = MDCard(orientation="vertical", padding=dp(12), md_bg_color=(0.1, 0.1, 0.14, 1), radius=[12], size_hint_y=None, height=dp(95))
        self.lbl_beneficios = MDLabel(text="", halign="center", font_style="Caption")
        card_b.add_widget(self.lbl_beneficios); box.add_widget(card_b)

        btn_comenzar = MDFillRoundFlatButton(text="Ir a Entrenamientos", size_hint=(1, None), height=dp(48), md_bg_color=(1, 0.2, 0.2, 1), on_release=lambda x: self.ir_inicio())
        box.add_widget(btn_comenzar)

        layout.add_widget(box); self.add_widget(layout)

    def ir_inicio(self):
        self.manager.transition.direction = "right"; self.manager.current = "bienvenida"


# CONTROLADOR CENTRAL NATIVO
class FlexRexApp(MDApp):
    def build(self):
        load_user_data()
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Red'
        
        sm = ScreenManager()
        sm.add_widget(PantallaBienvenida(name='bienvenida'))
        sm.add_widget(PantallaRegistro(name='registro'))
        sm.add_widget(PantallaSugerenciaPlan(name='sugerencia'))
        sm.add_widget(PantallaEjercicios(name='ejercicios'))
        sm.add_widget(PantallaEntrenamiento(name='entrenamiento_activo'))
        sm.add_widget(PantallaPerfil(name='perfil'))
        sm.add_widget(PantallaProgreso(name='progreso'))
        sm.add_widget(PantallaMembresias(name='membresias'))
        sm.add_widget(PantallaPago(name='pago'))
        sm.add_widget(PantallaConfirmacion(name='confirmacion'))
        return sm

if __name__ == "__main__":
    FlexRexApp().run()
