from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.animation import Animation 
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton, MDFloatingActionButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.scrollview import ScrollView

# Datos del usuario
DATOS_USUARIO = {
    "nombre": "",
    "edad": "",
    "sexo": "Seleccionar...",
    "altura": "",
    "peso": "",
    "ejercicio": None,
    "plan_sugerido": None
}

# PANTALLA 1: BIENVENIDA
class PantallaBienvenida(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout_pantalla = FloatLayout()
        layout_principal = BoxLayout(orientation='vertical', padding=[20, 35, 20, 25], spacing=12)
        
        layout_principal.add_widget(MDLabel(
            text="FLEX-REX", halign="center", font_style="H4", 
            theme_text_color="Primary", size_hint_y=None, height=40
        ))
        layout_principal.add_widget(MDLabel(
            text="Tu entrenador personal dinámico", halign="center", font_style="Subtitle1",
            theme_text_color="Secondary", size_hint_y=None, height=30
        ))
        
        self.logo = AsyncImage(
            source="https://cdn-icons-png.flaticon.com/512/2936/2936886.png", 
            size_hint=(0.6, 0.35), allow_stretch=True,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        layout_principal.add_widget(self.logo)
        self.animar_logo_flotante()
        
        datos_tarjetas = [
            {"titulo": "Múltiples Ejercicios", "sub": "Elige entre flexiones, dominadas o sentadillas", "icono": "weight-lifter", "color": (1, 0.3, 0.3, 1)},
            {"titulo": "Sistema de Rachas", "sub": "Mantén tu motivación día a día", "icono": "fire", "color": (1, 0.6, 0.2, 1)},
            {"titulo": "Estadísticas Detalladas", "sub": "Observa tu progreso y evolución", "icono": "trophy-outline", "color": (0.2, 0.6, 1, 1)}
        ]
        
        for dt in datos_tarjetas:
            card = MDCard(
                orientation='horizontal', padding=[15, 10, 15, 10],
                size_hint=(1, None), height=70, radius=[12, 12, 12, 12],
                md_bg_color=(0.15, 0.15, 0.15, 1), elevation=1
            )
            icon_container = FloatLayout(size_hint=(0.18, 1))
            icon_container.add_widget(MDIconButton(icon=dt["icono"], pos_hint={"center_x": 0.5, "center_y": 0.5}, theme_icon_color="Custom", icon_color=dt["color"]))
            card.add_widget(icon_container)
            
            text_container = BoxLayout(orientation='vertical', spacing=2)
            text_container.add_widget(MDLabel(text=dt["titulo"], font_style="Subtitle2", bold=True, theme_text_color="Primary"))
            text_container.add_widget(MDLabel(text=dt["sub"], font_style="Caption", theme_text_color="Secondary"))
            card.add_widget(text_container)
            layout_principal.add_widget(card)
            
        layout_principal.add_widget(BoxLayout(size_hint_y=None, height=5))
        
        btn_comenzar = MDRaisedButton(
            text="Comenzar Ahora", pos_hint={"center_x": 0.5},
            size_hint=(0.85, None), height=48,
            on_release=lambda x: self.ir_a_registro()
        )
        layout_principal.add_widget(btn_comenzar)
        layout_pantalla.add_widget(layout_principal)
        
        btn_flotante_info = MDFloatingActionButton(
            icon="information-variant",
            pos_hint={"right": 0.95, "y": 0.03},
            md_bg_color=MDApp.get_running_app().theme_cls.primary_color,
            on_release=lambda x: print("[INFO] Desarrollado para FLEX-REX v1.0")
        )
        layout_pantalla.add_widget(btn_flotante_info)
        
        self.add_widget(layout_pantalla)

    def animar_logo_flotante(self):
        anim = Animation(pos_hint={"center_x": 0.5, "center_y": 0.55}, duration=1.0, t='in_out_quad') + \
               Animation(pos_hint={"center_x": 0.5, "center_y": 0.45}, duration=1.0, t='in_out_quad')
        anim.repeat = True
        anim.start(self.logo)

    def ir_a_registro(self):
        self.manager.transition.direction = "left"
        self.manager.current = "registro"

# PANTALLA 2: REGISTRO
class PantallaRegistro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout_pantalla = FloatLayout()
        
        scroll = ScrollView(size_hint=(1, 1))
        layout_principal = BoxLayout(orientation='vertical', padding=25, spacing=15, size_hint_y=None)
        layout_principal.bind(minimum_height=layout_principal.setter('height'))
        
        layout_principal.add_widget(MDLabel(
            text="¡Bienvenido!\nCuéntanos un poco sobre ti", 
            halign="center", font_style="H5", size_hint_y=None, height=70
        ))
        
        self.txt_nombre = MDTextField(hint_text="¿Cómo te llamas?", text="", size_hint_y=None, height=50)
        self.txt_edad = MDTextField(hint_text="¿Qué edad tienes?", text="", size_hint_y=None, height=50)
        self.txt_altura = MDTextField(hint_text="Altura (cm)", text="", size_hint_y=None, height=50)
        self.txt_peso = MDTextField(hint_text="Peso (kg)", text="", size_hint_y=None, height=50)
        
        layout_principal.add_widget(self.txt_nombre)
        layout_principal.add_widget(self.txt_edad)
        layout_principal.add_widget(self.txt_altura)
        layout_principal.add_widget(self.txt_peso)
        
        layout_sexo = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=75)
        layout_sexo.add_widget(MDLabel(text="Sexo:", font_style="Caption", theme_text_color="Secondary", size_hint_y=None, height=20))
        
        self.btn_sexo_dropdown = MDRaisedButton(
            text=DATOS_USUARIO["sexo"], 
            size_hint=(1, None), height=45, 
            md_bg_color=(0.2, 0.2, 0.2, 1),
            on_release=self.abrir_menu_sexo
        )
        layout_sexo.add_widget(self.btn_sexo_dropdown)
        layout_principal.add_widget(layout_sexo)
        
        opciones = ["Masculino", "Femenino", "Prefiero no decirlo"]
        self.menu_sexo = MDDropdownMenu(
            caller=self.btn_sexo_dropdown,
            items=[{"text": op, "viewclass": "OneLineListItem", "on_release": lambda x=op: self.cambiar_sexo(x)} for op in opciones],
            width_mult=4,
        )
        
        layout_principal.add_widget(MDLabel(
            text="Consejo rápido:\nComienza con una meta alcanzable. Es mejor hacer ejercicio constante que agotarse el primer día.",
            halign="center", font_style="Caption", theme_text_color="Secondary",
            size_hint_y=None, height=60
        ))
        
        btn_siguiente = MDRaisedButton(
            text="Continuar",
            size_hint=(0.85, None), height=50,
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.ir_a_sugerencia()
        )
        layout_principal.add_widget(btn_siguiente)
        
        btn_limpiar = MDFlatButton(
            text="Limpiar campos",
            size_hint=(0.85, None), height=40,
            pos_hint={"center_x": 0.5},
            theme_text_color="Custom",
            text_color=(0.8, 0.8, 0.8, 1),
            on_release=lambda x: self.limpiar_campos()
        )
        layout_principal.add_widget(btn_limpiar)
        
        scroll.add_widget(layout_principal)
        layout_pantalla.add_widget(scroll)
        
        self.btn_regresar_flotante = MDIconButton(
            icon="arrow-left", theme_icon_color="Custom", 
            icon_color=(1, 1, 1, 1), md_bg_color=(0.25, 0.25, 0.25, 1),     
            pos_hint={"x": 0.04, "top": 0.96}, size_hint=(None, None), size=(42, 42),
            on_release=lambda x: self.regresar_pantalla()
        )
        layout_pantalla.add_widget(self.btn_regresar_flotante)
        
        btn_flotante_ayuda = MDFloatingActionButton(
            icon="help",
            pos_hint={"right": 0.95, "y": 0.03},
            md_bg_color=(0.2, 0.5, 0.8, 1),
            on_release=lambda x: self.mostrar_ayuda()
        )
        layout_pantalla.add_widget(btn_flotante_ayuda)
        
        self.add_widget(layout_pantalla)
    
    def limpiar_campos(self):
        self.txt_nombre.text = ""
        self.txt_edad.text = ""
        self.txt_altura.text = ""
        self.txt_peso.text = ""
        self.btn_sexo_dropdown.text = "Seleccionar..."
        DATOS_USUARIO["sexo"] = "Seleccionar..."
        
        anim = Animation(opacity=0.5, duration=0.1) + Animation(opacity=1.0, duration=0.15)
        for campo in [self.txt_nombre, self.txt_edad, self.txt_altura, self.txt_peso]:
            anim.start(campo)
    
    def mostrar_ayuda(self):
        dialog = MDDialog(
            title="Información requerida",
            text="Completa tus datos para personalizar tu experiencia de entrenamiento.\n\n"
                 "- Nombre: Como quieras que te llamemos\n"
                 "- Edad: Para recomendaciones según tu rango etario\n"
                 "- Altura: En centímetros (ej: 175)\n"
                 "- Peso: En kilogramos (ej: 70)\n"
                 "- Sexo: Para ajustes específicos",
            buttons=[
                MDFlatButton(
                    text="Entendido",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def abrir_menu_sexo(self, boton):
        self.menu_sexo.open()

    def cambiar_sexo(self, sexo_elegido):
        self.btn_sexo_dropdown.text = sexo_elegido
        DATOS_USUARIO["sexo"] = sexo_elegido
        self.menu_sexo.dismiss()
        
        anim = Animation(opacity=0.4, duration=0.1) + Animation(opacity=1.0, duration=0.15)
        anim.start(self.btn_sexo_dropdown)

    def regresar_pantalla(self):
        self.manager.transition.direction = "right"
        self.manager.current = "bienvenida"

    def ir_a_sugerencia(self):
        DATOS_USUARIO["nombre"] = self.txt_nombre.text if self.txt_nombre.text else "Anónimo"
        DATOS_USUARIO["edad"] = self.txt_edad.text if self.txt_edad.text else "No provista"
        DATOS_USUARIO["altura"] = self.txt_altura.text if self.txt_altura.text else "No provista"
        DATOS_USUARIO["peso"] = self.txt_peso.text if self.txt_peso.text else "No provista"
        
        self.manager.transition.direction = "left"
        self.manager.current = "sugerencia_plan"

# PANTALLA 3: SUGERENCIA DE PLAN
class PantallaSugerenciaPlan(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plan_generado = None
        self.card_plan = None
        
    def on_enter(self, *args):
        self.generar_plan_personalizado()
    
    def generar_plan_personalizado(self):
        altura = DATOS_USUARIO["altura"]
        peso = DATOS_USUARIO["peso"]
        
        imc = None
        if altura != "No provista" and peso != "No provista":
            try:
                altura_metros = float(altura) / 100
                peso_kg = float(peso)
                imc = peso_kg / (altura_metros ** 2)
            except:
                pass
        
        if imc:
            if imc < 18.5:
                self.plan_generado = {
                    "nivel": "Principiante - Bajo peso",
                    "objetivo": "Ganar masa muscular y peso saludable",
                    "ejercicio_recomendado": "Sentadillas",
                    "ejercicios": ["Sentadillas", "Flexiones asistidas", "Dominadas con banda elástica"],
                    "repeticiones": "10-12 repeticiones x 3 series",
                    "frecuencia": "3-4 veces por semana",
                    "duracion": "30-40 minutos por sesión",
                    "consejo": "Complementa con una dieta rica en proteínas y carbohidratos"
                }
            elif imc < 25:
                self.plan_generado = {
                    "nivel": "Intermedio - Peso normal",
                    "objetivo": "Mantener y tonificar",
                    "ejercicio_recomendado": "Flexiones",
                    "ejercicios": ["Flexiones", "Sentadillas con salto", "Dominadas"],
                    "repeticiones": "15-20 repeticiones x 4 series",
                    "frecuencia": "4-5 veces por semana",
                    "duracion": "45 minutos por sesión",
                    "consejo": "Varía la intensidad para evitar estancamiento"
                }
            elif imc < 30:
                self.plan_generado = {
                    "nivel": "Intermedio - Sobrepeso",
                    "objetivo": "Reducción de grasa y ganancia muscular",
                    "ejercicio_recomendado": "Sentadillas",
                    "ejercicios": ["Sentadillas", "Flexiones", "Cardio ligero"],
                    "repeticiones": "12-15 repeticiones x 3 series",
                    "frecuencia": "4-5 veces por semana",
                    "duracion": "45-50 minutos por sesión",
                    "consejo": "Incluye 15 minutos de cardio antes de cada sesión"
                }
            else:
                self.plan_generado = {
                    "nivel": "Principiante - Obesidad",
                    "objetivo": "Pérdida de peso progresiva",
                    "ejercicio_recomendado": "Sentadillas asistidas",
                    "ejercicios": ["Sentadillas asistidas", "Flexiones de pared", "Caminata"],
                    "repeticiones": "8-10 repeticiones x 2 series",
                    "frecuencia": "3 veces por semana",
                    "duracion": "30 minutos por sesión",
                    "consejo": "Consulta a un profesional antes de comenzar"
                }
        else:
            self.plan_generado = {
                "nivel": "Principiante",
                "objetivo": "Mejorar condición física general",
                "ejercicio_recomendado": "Flexiones",
                "ejercicios": ["Flexiones", "Sentadillas", "Dominadas"],
                "repeticiones": "10-15 repeticiones x 3 series",
                "frecuencia": "3 veces por semana",
                "duracion": "30-40 minutos por sesión",
                "consejo": "Comienza con pocas repeticiones y aumenta gradualmente"
            }
        
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        layout_pantalla = FloatLayout()
        layout_principal = BoxLayout(orientation='vertical', padding=25, spacing=15, size_hint=(1, 1))
        
        layout_principal.add_widget(MDLabel(
            text=f"✨ Plan Personalizado para {DATOS_USUARIO['nombre']} ✨",
            halign="center", font_style="H5", bold=True,
            theme_text_color="Primary", size_hint_y=None, height=50
        ))
        
        self.card_plan = MDCard(
            orientation='vertical', padding=20, spacing=12,
            size_hint=(0.95, None), height=480,
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.15, 0.15, 0.15, 1),
            radius=[15, 15, 15, 15], elevation=4
        )
        
        icono_plan = "🏆" if self.plan_generado["nivel"] == "Intermedio - Peso normal" else "📈"
        self.card_plan.add_widget(MDLabel(
            text=f"{icono_plan} {self.plan_generado['nivel']}",
            halign="center", font_style="H6", bold=True,
            theme_text_color="Primary", size_hint_y=None, height=35
        ))
        
        self.card_plan.add_widget(MDLabel(
            text=f"🎯 Objetivo: {self.plan_generado['objetivo']}",
            halign="left", font_style="Subtitle1",
            size_hint_y=None, height=35
        ))
        
        self.card_plan.add_widget(MDLabel(
            text=f"⭐ EJERCICIO PRINCIPAL: {self.plan_generado['ejercicio_recomendado']}",
            halign="center", font_style="Subtitle1", bold=True,
            theme_text_color="Custom", text_color=(1, 0.5, 0.2, 1),
            size_hint_y=None, height=40
        ))
        
        self.card_plan.add_widget(MDLabel(
            text=f"📊 {self.plan_generado['repeticiones']}",
            halign="center", font_style="Body1", bold=True,
            theme_text_color="Primary", size_hint_y=None, height=35
        ))
        
        ejercicios_texto = "💪 Plan completo:\n"
        for ejercicio in self.plan_generado['ejercicios']:
            ejercicios_texto += f"  • {ejercicio}\n"
        
        self.card_plan.add_widget(MDLabel(
            text=ejercicios_texto,
            halign="left", font_style="Body1",
            size_hint_y=None, height=100
        ))
        
        self.card_plan.add_widget(MDLabel(
            text=f"📅 {self.plan_generado['frecuencia']}",
            halign="left", font_style="Body1",
            size_hint_y=None, height=35
        ))
        
        self.card_plan.add_widget(MDLabel(
            text=f"⏱️ {self.plan_generado['duracion']}",
            halign="left", font_style="Body1",
            size_hint_y=None, height=35
        ))
        
        self.card_plan.add_widget(MDLabel(
            text=f"💡 {self.plan_generado['consejo']}",
            halign="left", font_style="Body1",
            theme_text_color="Secondary", size_hint_y=None, height=60
        ))
        
        layout_principal.add_widget(self.card_plan)
        
        layout_botones = BoxLayout(orientation='horizontal', spacing=15, size_hint=(1, None), height=50, padding=[20, 0, 20, 0])
        
        btn_aceptar = MDRaisedButton(
            text="✓ Aceptar y Comenzar",
            size_hint=(0.48, 1),
            md_bg_color=(0.1, 0.7, 0.1, 1),
            on_release=lambda x: self.aceptar_plan()
        )
        
        btn_omitir = MDFlatButton(
            text="Omitir y Elegir Yo",
            size_hint=(0.48, 1),
            theme_text_color="Custom",
            text_color=(0.8, 0.8, 0.8, 1),
            on_release=lambda x: self.omitir_plan()
        )
        
        layout_botones.add_widget(btn_aceptar)
        layout_botones.add_widget(btn_omitir)
        layout_principal.add_widget(layout_botones)
        
        layout_pantalla.add_widget(layout_principal)
        
        self.btn_regresar_flotante = MDIconButton(
            icon="arrow-left", theme_icon_color="Custom", 
            icon_color=(1, 1, 1, 1), md_bg_color=(0.25, 0.25, 0.25, 1),     
            pos_hint={"x": 0.04, "top": 0.96}, size_hint=(None, None), size=(42, 42),
            on_release=lambda x: self.regresar_pantalla()
        )
        layout_pantalla.add_widget(self.btn_regresar_flotante)
        
        self.add_widget(layout_pantalla)
    
    def aceptar_plan(self):
        DATOS_USUARIO["plan_sugerido"] = self.plan_generado
        DATOS_USUARIO["ejercicio"] = self.plan_generado['ejercicio_recomendado']
        
        dialog = MDDialog(
            title="🎉 Plan Aceptado",
            text=f"¡Excelente {DATOS_USUARIO['nombre']}!\n\n"
                 f"Comenzarás con: {self.plan_generado['ejercicio_recomendado']}\n"
                 f"{self.plan_generado['repeticiones']}\n\n"
                 f"¡Prepárate para tu entrenamiento!",
            buttons=[
                MDFlatButton(
                    text="Comenzar Ahora",
                    on_release=lambda x: [dialog.dismiss(), self.ir_a_ejercicios()]
                )
            ]
        )
        dialog.open()
    
    def omitir_plan(self):
        DATOS_USUARIO["plan_sugerido"] = None
        DATOS_USUARIO["ejercicio"] = None
        
        dialog = MDDialog(
            title="Selección Manual",
            text="Puedes elegir tus propios ejercicios.\n\n"
                 "Selecciona el que prefieras en la siguiente pantalla.",
            buttons=[
                MDFlatButton(
                    text="Continuar",
                    on_release=lambda x: [dialog.dismiss(), self.ir_a_ejercicios()]
                )
            ]
        )
        dialog.open()
    
    def regresar_pantalla(self):
        self.manager.transition.direction = "right"
        self.manager.current = "registro"
    
    def ir_a_ejercicios(self):
        self.manager.transition.direction = "left"
        self.manager.current = "ejercicios"

# PANTALLA 4: EJERCICIOS
class PantallaEjercicios(Screen):
    def on_enter(self, *args):
        animacion_entrada = Animation(pos_hint={"center_x": 0.5, "center_y": 0.45}, duration=0.8, t='out_cubic')
        animacion_entrada.start(self.layout_principal)
        self.actualizar_resumen()
        
        if DATOS_USUARIO["plan_sugerido"]:
            self.mostrar_plan_aceptado()
            self.ocultar_botones_seleccion()
        else:
            self.mostrar_botones_seleccion()
            self.ocultar_plan()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout_pantalla = FloatLayout()
        
        self.layout_principal = BoxLayout(
            orientation='vertical', padding=25, spacing=24, 
            size_hint=(1, 0.85), pos_hint={"center_x": 0.5, "center_y": 0.45}
        )
        
        self.lbl_resumen = MDLabel(
            text="", halign="center", font_style="Subtitle1", bold=True,
            theme_text_color="Secondary", size_hint_y=None, height=30
        )
        self.layout_principal.add_widget(self.lbl_resumen)
        
        self.lbl_titulo = MDLabel(
            text="", halign="center", font_style="H5", bold=True, 
            theme_text_color="Primary", size_hint_y=None, height=40
        )
        self.layout_principal.add_widget(self.lbl_titulo)
        
        self.container_plan = BoxLayout(orientation='vertical', size_hint_y=None, height=0)
        self.layout_principal.add_widget(self.container_plan)
        
        self.container_botones = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None, height=250)
        
        self.btn_dominadas = MDRaisedButton(
            text="Dominadas", size_hint=(0.85, None), height=50, 
            pos_hint={"center_x": 0.5}, md_bg_color=(0.2, 0.2, 0.2, 1), 
            on_release=lambda x: self.seleccionar_ejercicio("Dominadas", self.btn_dominadas)
        )
        self.btn_flexiones = MDRaisedButton(
            text="Flexiones", size_hint=(0.85, None), height=50, 
            pos_hint={"center_x": 0.5}, md_bg_color=(0.2, 0.2, 0.2, 1), 
            on_release=lambda x: self.seleccionar_ejercicio("Flexiones", self.btn_flexiones)
        )
        self.btn_sentadillas = MDRaisedButton(
            text="Sentadillas", size_hint=(0.85, None), height=50, 
            pos_hint={"center_x": 0.5}, md_bg_color=(0.2, 0.2, 0.2, 1), 
            on_release=lambda x: self.seleccionar_ejercicio("Sentadillas", self.btn_sentadillas)
        )
        
        self.container_botones.add_widget(self.btn_dominadas)
        self.container_botones.add_widget(self.btn_flexiones)
        self.container_botones.add_widget(self.btn_sentadillas)
        self.layout_principal.add_widget(self.container_botones)
        
        btn_entrenar = MDRaisedButton(
            text="Empezar a Entrenar", 
            size_hint=(0.85, None), height=55, 
            md_bg_color=(0.1, 0.6, 0.1, 1),
            on_release=lambda x: self.finalizar_todo()
        )
        self.layout_principal.add_widget(btn_entrenar)
        layout_pantalla.add_widget(self.layout_principal)
        
        self.btn_regresar_flotante = MDIconButton(
            icon="arrow-left", theme_icon_color="Custom", 
            icon_color=(1, 1, 1, 1), md_bg_color=(0.25, 0.25, 0.25, 1),     
            pos_hint={"x": 0.04, "top": 0.96}, size_hint=(None, None), size=(42, 42),
            on_release=lambda x: self.regresar_pantalla()
        )
        layout_pantalla.add_widget(self.btn_regresar_flotante)
        
        self.btn_salir_flotante = MDIconButton(
            icon="close", theme_icon_color="Custom", 
            icon_color=(1, 1, 1, 1), md_bg_color=(0.25, 0.25, 0.25, 1),     
            pos_hint={"right": 0.96, "top": 0.96}, size_hint=(None, None), size=(42, 42),
            on_release=lambda x: self.alerta_usuario_salir()
        )
        layout_pantalla.add_widget(self.btn_salir_flotante)
        
        btn_flotante_logros = MDFloatingActionButton(
            icon="trophy",
            pos_hint={"right": 0.95, "y": 0.03},
            md_bg_color=(0.9, 0.6, 0.1, 1),
            on_release=lambda x: print("[LOGROS] ¡Próximamente podrás ver tus medallas aquí!")
        )
        layout_pantalla.add_widget(btn_flotante_logros)
        
        self.add_widget(layout_pantalla)
    
    def actualizar_resumen(self):
        resumen_texto = f"⚡ {DATOS_USUARIO['nombre']}"
        if DATOS_USUARIO['altura'] and DATOS_USUARIO['altura'] != "No provista":
            resumen_texto += f" | {DATOS_USUARIO['altura']}cm"
        if DATOS_USUARIO['peso'] and DATOS_USUARIO['peso'] != "No provista":
            resumen_texto += f" • {DATOS_USUARIO['peso']}kg"
        self.lbl_resumen.text = resumen_texto
    
    def mostrar_plan_aceptado(self):
        plan = DATOS_USUARIO["plan_sugerido"]
        self.lbl_titulo.text = "📋 SIGUIENDO TU PLAN PERSONALIZADO"
        
        self.container_plan.clear_widgets()
        
        card_plan = MDCard(
            orientation='vertical', padding=[20, 15, 20, 15],
            size_hint=(0.95, None), height=300,
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.1, 0.2, 0.15, 1), 
            radius=[15, 15, 15, 15],
            elevation=3
        )
        
        card_plan.add_widget(MDLabel(
            text=f"🎯 {plan['objetivo']}",
            halign="center", font_style="Subtitle1", bold=True,
            theme_text_color="Primary", size_hint_y=None, height=40
        ))
        
        card_plan.add_widget(MDLabel(
            text=f"⭐ EJERCICIO DE HOY",
            halign="center", font_style="Caption", bold=True,
            theme_text_color="Secondary", size_hint_y=None, height=25
        ))
        
        lbl_ejercicio = MDLabel(
            text=f"{plan['ejercicio_recomendado'].upper()}",
            halign="center", font_style="H5", bold=True,
            theme_text_color="Custom", text_color=(1, 0.6, 0.2, 1),
            size_hint_y=None, height=45
        )
        card_plan.add_widget(lbl_ejercicio)
        
        card_plan.add_widget(MDLabel(
            text=f"📊 {plan['repeticiones']}",
            halign="center", font_style="Body1", bold=True,
            theme_text_color="Primary", size_hint_y=None, height=35
        ))
        
        card_plan.add_widget(MDLabel(
            text=f"💡 {plan['consejo']}",
            halign="center", font_style="Caption",
            theme_text_color="Secondary", size_hint_y=None, height=50
        ))
        
        self.container_plan.add_widget(card_plan)
        self.container_plan.height = 320
    
    def ocultar_botones_seleccion(self):
        self.container_botones.height = 0
        self.container_botones.opacity = 0
    
    def mostrar_botones_seleccion(self):
        self.container_botones.height = 250
        self.container_botones.opacity = 1
    
    def ocultar_plan(self):
        self.container_plan.height = 0
        self.container_plan.opacity = 0
        self.lbl_titulo.text = "¿Qué quieres contar hoy?"
    
    def seleccionar_ejercicio(self, ejercicio, boton_pulsado):
        DATOS_USUARIO["ejercicio"] = ejercicio
        for btn in [self.btn_dominadas, self.btn_flexiones, self.btn_sentadillas]:
            btn.md_bg_color = (0.2, 0.2, 0.2, 1)
        boton_pulsado.md_bg_color = (1, 0.25, 0.25, 1)

    def regresar_pantalla(self):
        self.manager.transition.direction = "right"
        self.manager.current = "sugerencia_plan"

    def alerta_usuario_salir(self):
        dialog = MDDialog(
            title="¿Cerrar FLEX-REX?",
            text="¿Estás seguro de que quieres salir de la aplicación?",
            buttons=[
                MDFlatButton(text="No", on_release=lambda x: dialog.dismiss()),
                MDFlatButton(text="Sí", on_release=lambda x: self.exit_app())
            ]
        )
        dialog.open()
    
    def exit_app(self):
        MDApp.get_running_app().stop()

    def finalizar_todo(self):
        if not DATOS_USUARIO["ejercicio"]:
            from kivymd.uix.dialog import MDDialog
            dialog = MDDialog(
                title="⚠️ Selecciona un ejercicio",
                text="Por favor, selecciona un ejercicio antes de comenzar.",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
            )
            dialog.open()
            return
            
        print(f"\n==========================================")
        print(f"[ENTRENAMIENTO INICIADO]")
        print(f"Atleta: {DATOS_USUARIO['nombre']} | Edad: {DATOS_USUARIO['edad']} | Sexo: {DATOS_USUARIO['sexo']}")
        print(f"Altura: {DATOS_USUARIO['altura']} cm | Peso: {DATOS_USUARIO['peso']} kg")
        print(f"Contador activo para: {DATOS_USUARIO['ejercicio']}")
        if DATOS_USUARIO["plan_sugerido"]:
            print(f"Plan activo: {DATOS_USUARIO['plan_sugerido']['nivel']}")
            print(f"Ejercicio del plan: {DATOS_USUARIO['plan_sugerido']['ejercicio_recomendado']}")
        print(f"==========================================\n")
        
        # Mostrar diálogo de éxito
        dialog = MDDialog(
            title="🎉 Entrenamiento Iniciado",
            text=f"¡Buena suerte con tus {DATOS_USUARIO['ejercicio']}!\n\n"
                 f"El contador está listo para registrar tus repeticiones.",
            buttons=[MDFlatButton(text="Comenzar", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

# CLASE PRINCIPAL
class FlexRexApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Red'
        
        sm = ScreenManager()
        sm.add_widget(PantallaBienvenida(name='bienvenida'))
        sm.add_widget(PantallaRegistro(name='registro'))
        sm.add_widget(PantallaSugerenciaPlan(name='sugerencia_plan'))
        sm.add_widget(PantallaEjercicios(name='ejercicios'))
        return sm

if __name__ == "__main__":
    FlexRexApp().run()