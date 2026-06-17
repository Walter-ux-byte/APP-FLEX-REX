from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image  
from kivy.animation import Animation 
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField  
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock  
from kivy.graphics.texture import Texture
import os
import cv2
import math

# ==========================================
# IMPORTACIÓN ESTÁNDAR DE MEDIAPIPE (LIMPIA)
# ==========================================
import mediapipe as mp
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Datos del usuario globales
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
        
        ruta_manual = os.path.join("D:\\", "Flex-Rex", "image_51a254.png")
        if not os.path.exists(ruta_manual):
            directorio_script = os.path.dirname(os.path.abspath(__file__))
            ruta_manual = os.path.join(directorio_script, "image_51a254.png")

        self.logo = Image(
            source=ruta_manual, 
            size_hint=(0.55, 0.32), allow_stretch=True,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        layout_principal.add_widget(self.logo)
        self.animar_logo_dinamico()  
        
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
            
        self.contenedor_btn = FloatLayout(size_hint_y=None, height=60)
        self.btn_comenzar = MDRaisedButton(
            text="Comenzar Ahora", 
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.85, 0.8),
            md_bg_color=(0.9, 0.1, 0.1, 1), 
            on_release=lambda x: self.ir_a_registro()
        )
        self.contenedor_btn.add_widget(self.btn_comenzar)
        layout_principal.add_widget(self.contenedor_btn)
        
        self.animar_boton_pulso()
        layout_pantalla.add_widget(layout_principal)
        self.add_widget(layout_pantalla)

    def animar_logo_dinamico(self):
        anim = (Animation(pos_hint={"center_x": 0.5, "center_y": 0.52}, size_hint=(0.58, 0.34), duration=1.5, t='in_out_quad') + 
                Animation(pos_hint={"center_x": 0.5, "center_y": 0.48}, size_hint=(0.52, 0.30), duration=1.5, t='in_out_quad'))
        anim.repeat = True
        anim.start(self.logo)

    def animar_boton_pulso(self):
        anim = Animation(size_hint=(0.92, 0.9), duration=0.9, t='in_out_sine') + \
               Animation(size_hint=(0.85, 0.8), duration=0.9, t='in_out_sine')
        anim.repeat = True
        anim.start(self.btn_comenzar)

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
        
        self.txt_nombre = MDTextField(hint_text="¿Cómo te llamas?", size_hint_y=None, height=50)
        self.txt_edad = MDTextField(hint_text="¿Qué edad tienes?", size_hint_y=None, height=50)
        self.txt_altura = MDTextField(hint_text="Altura (cm)", size_hint_y=None, height=50)
        self.txt_peso = MDTextField(hint_text="Peso (kg)", size_hint_y=None, height=50)
        
        layout_principal.add_widget(self.txt_nombre)
        layout_principal.add_widget(self.txt_edad)
        layout_principal.add_widget(self.txt_altura)
        layout_principal.add_widget(self.txt_peso)
        
        layout_sexo = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=75)
        layout_sexo.add_widget(MDLabel(text="Sexo:", font_style="Caption", theme_text_color="Secondary", size_hint_y=None, height=20))
        
        self.btn_sexo_dropdown = MDRaisedButton(
            text=DATOS_USUARIO["sexo"], size_hint=(1, None), height=45, 
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
        
        btn_siguiente = MDRaisedButton(
            text="Continuar", size_hint=(0.85, None), height=50,
            pos_hint={"center_x": 0.5}, on_release=lambda x: self.ir_a_sugerencia()
        )
        layout_principal.add_widget(btn_siguiente)
        
        scroll.add_widget(layout_principal)
        layout_pantalla.add_widget(scroll)
        
        self.btn_regresar_flotante = MDIconButton(
            icon="arrow-left", md_bg_color=(0.25, 0.25, 0.25, 1),     
            pos_hint={"x": 0.04, "top": 0.96}, on_release=lambda x: self.regresar_pantalla()
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
        self.manager.current = "sugerencia_plan"


# PANTALLA 3: SUGERENCIA DE PLAN
class PantallaSugerenciaPlan(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plan_generado = None
        
    def on_enter(self, *args):
        self.generar_plan_personalizado()
        self.animar_botones_entrada()
    
    def generar_plan_personalizado(self):
        altura = DATOS_USUARIO["altura"]
        peso = DATOS_USUARIO["peso"]
        imc = float(peso) / ((float(altura) / 100) ** 2)
        
        if imc < 18.5:
            self.plan_generado = {"objetivo": "Ganar masa muscular", "ejercicio_recomendado": "Sentadillas", "repeticiones": " Meta: 10 repeticiones", "consejo": "Enfócate en la técnica baja."}
        elif imc < 25:
            self.plan_generado = {"objetivo": "Mantener y tonificar", "ejercicio_recomendado": "Flexiones", "repeticiones": "Meta: 15 repeticiones", "consejo": "Controla el descenso suave."}
        else:
            self.plan_generado = {"objetivo": "Acondicionamiento", "ejercicio_recomendado": "Sentadillas", "repeticiones": "Meta: 12 repeticiones", "consejo": "Mantén la espalda recta."}
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        layout_pantalla = FloatLayout()
        layout_principal = BoxLayout(orientation='vertical', padding=25, spacing=15)
        
        layout_principal.add_widget(MDLabel(text=f"✨ Plan para {DATOS_USUARIO['nombre']} ✨", halign="center", font_style="H5", bold=True, size_hint_y=None, height=50))
        
        card_plan = MDCard(orientation='vertical', padding=20, spacing=12, size_hint=(0.95, None), height=320, pos_hint={"center_x": 0.5}, md_bg_color=(0.15, 0.15, 0.15, 1), radius=[15])
        card_plan.add_widget(MDLabel(text=f"🎯 Objetivo: {self.plan_generado['objetivo']}", font_style="Subtitle1"))
        card_plan.add_widget(MDLabel(text=f"⭐ SUGERIDO: {self.plan_generado['ejercicio_recomendado']}", font_style="H6", bold=True, text_color=(1,0.5,0.2,1), theme_text_color="Custom"))
        card_plan.add_widget(MDLabel(text=f"📊 {self.plan_generado['repeticiones']}", font_style="Body1"))
        card_plan.add_widget(MDLabel(text=f"💡 Consejo: {self.plan_generado['consejo']}", font_style="Caption", theme_text_color="Secondary"))
        layout_principal.add_widget(card_plan)
        
        self.contenedor_botones = FloatLayout(size_hint=(1, None), height=60)
        self.btn_aceptar = MDRaisedButton(text="✓ Aceptar Plan", size_hint=(0.45, 0.9), pos_hint={"x": -0.5, "center_y": 0.5}, md_bg_color=(0.1, 0.7, 0.1, 1), on_release=lambda x: self.aceptar_plan())
        self.btn_omitir = MDFlatButton(text="Elegir Yo", size_hint=(0.45, 0.9), pos_hint={"right": 1.5, "center_y": 0.5}, theme_text_color="Custom", text_color=(0.8, 0.8, 0.8, 1), on_release=lambda x: self.omitir_plan())
        self.contenedor_botones.add_widget(self.btn_aceptar)
        self.contenedor_botones.add_widget(self.btn_omitir)
        layout_principal.add_widget(self.contenedor_botones)
        
        layout_pantalla.add_widget(layout_principal)
        self.add_widget(layout_pantalla)
    
    def animar_botones_entrada(self):
        Animation(pos_hint={"x": 0.03, "center_y": 0.5}, duration=0.8, t='out_back').start(self.btn_aceptar)
        Animation(pos_hint={"right": 0.97, "center_y": 0.5}, duration=0.8, t='out_back').start(self.btn_omitir)

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


# PANTALLA 4: SELECCIÓN DE EJERCICIOS
class PantallaEjercicios(Screen):
    def on_enter(self, *args):
        self.actualizar_resumen()
        if DATOS_USUARIO["plan_sugerido"]:
            self.mostrar_plan_aceptado()
            self.container_botones.height = 0
            self.container_botones.opacity = 0
        else:
            self.lbl_titulo.text = "¿Qué vas a entrenar hoy?"
            self.container_plan.height = 0
            self.container_botones.height = 220
            self.container_botones.opacity = 1
            self.animar_botones_cascada()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout_pantalla = FloatLayout()
        layout_principal = BoxLayout(orientation='vertical', padding=25, spacing=15)
        
        self.lbl_resumen = MDLabel(text="", halign="center", font_style="Subtitle2", theme_text_color="Secondary", size_hint_y=None, height=25)
        layout_principal.add_widget(self.lbl_resumen)
        
        self.lbl_titulo = MDLabel(text="", halign="center", font_style="H6", bold=True, size_hint_y=None, height=35)
        layout_principal.add_widget(self.lbl_titulo)
        
        self.container_plan = BoxLayout(orientation='vertical', size_hint_y=None, height=0)
        layout_principal.add_widget(self.container_plan)
        
        self.container_botones = FloatLayout(size_hint_y=None, height=220)
        self.btn_dominadas = MDRaisedButton(text="Dominadas", size_hint=(0.85, None), height=45, pos_hint={"center_x": -0.5, "top": 0.95}, md_bg_color=(0.2, 0.2, 0.2, 1), on_release=lambda x: self.seleccionar_ejercicio("Dominadas", self.btn_dominadas))
        self.btn_flexiones = MDRaisedButton(text="Flexiones", size_hint=(0.85, None), height=45, pos_hint={"center_x": 1.5, "top": 0.65}, md_bg_color=(0.2, 0.2, 0.2, 1), on_release=lambda x: self.seleccionar_ejercicio("Flexiones", self.btn_flexiones))
        self.btn_sentadillas = MDRaisedButton(text="Sentadillas", size_hint=(0.85, None), height=45, pos_hint={"center_x": -0.5, "top": 0.35}, md_bg_color=(0.2, 0.2, 0.2, 1), on_release=lambda x: self.seleccionar_ejercicio("Sentadillas", self.btn_sentadillas))
        
        self.container_botones.add_widget(self.btn_dominadas)
        self.container_botones.add_widget(self.btn_flexiones)
        self.container_botones.add_widget(self.btn_sentadillas)
        layout_principal.add_widget(self.container_botones)
        
        self.btn_entrenar = MDRaisedButton(
            text="🚀 Iniciar Cámara de Entrenamiento", size_hint=(0.85, None), height=50, 
            pos_hint={"center_x": 0.5}, md_bg_color=(0.1, 0.6, 0.1, 1),
            on_release=lambda x: self.comenzar_entrenamiento_camara()
        )
        layout_principal.add_widget(self.btn_entrenar)
        layout_pantalla.add_widget(layout_principal)
        self.add_widget(layout_pantalla)
    
    def animar_botones_cascada(self):
        Animation(pos_hint={"center_x": 0.5, "top": 0.95}, duration=0.4).start(self.btn_dominadas)
        Clock.schedule_once(lambda dt: Animation(pos_hint={"center_x": 0.5, "top": 0.65}, duration=0.4).start(self.btn_flexiones), 0.1)
        Clock.schedule_once(lambda dt: Animation(pos_hint={"center_x": 0.5, "top": 0.35}, duration=0.4).start(self.btn_sentadillas), 0.2)

    def actualizar_resumen(self):
        self.lbl_resumen.text = f"Atleta: {DATOS_USUARIO['nombre']} | Ejercicio: {DATOS_USUARIO['ejercicio']}"

    def mostrar_plan_aceptado(self):
        self.lbl_titulo.text = "📋 PLAN SELECCIONADO"
        self.container_plan.clear_widgets()
        card = MDCard(orientation='vertical', padding=15, size_hint=(0.9, None), height=100, pos_hint={"center_x":0.5}, md_bg_color=(0.1, 0.2, 0.15, 1))
        card.add_widget(MDLabel(text=f"Rutina de: {DATOS_USUARIO['ejercicio']}", font_style="H6", halign="center"))
        self.container_plan.add_widget(card)
        self.container_plan.height = 110

    def seleccionar_ejercicio(self, ejercicio, boton_pulsado):
        DATOS_USUARIO["ejercicio"] = ejercicio
        self.actualizar_resumen()
        for btn in [self.btn_dominadas, self.btn_flexiones, self.btn_sentadillas]:
            btn.md_bg_color = (0.2, 0.2, 0.2, 1)
        boton_pulsado.md_bg_color = (0.9, 0.1, 0.1, 1) 

    def comenzar_entrenamiento_camara(self):
        if not DATOS_USUARIO["ejercicio"]:
            dialog = MDDialog(title="⚠️ Error", text="Por favor, selecciona un ejercicio antes de encender la cámara.", buttons=[MDFlatButton(text="Entendido", on_release=lambda x: dialog.dismiss())])
            dialog.open()
            return
        self.manager.transition.direction = "left"
        self.manager.current = "entrenamiento_activo"


# PANTALLA 5: DETECCIÓN EN TIEMPO REAL
class PantallaEntrenamiento(Screen):
    def on_enter(self, *args):
        self.lbl_ejercicio.text = f"Entrenando: {str(DATOS_USUARIO['ejercicio']).upper()}"
        self.contador_reps = 0
        self.lbl_contador.text = "0"
        self.estado_fase = "arriba"
        
        try:
            # Inicialización directa usando las librerías oficiales del sistema
            self.pose = mp_pose.Pose(
                static_image_mode=False,
                model_complexity=1,  
                smooth_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
        except Exception as e:
            self.lbl_ejercicio.text = "⚠️ Error al iniciar MediaPipe"
            print(f"Error detallado de MediaPipe: {e}")
            return
        
        try:
            self.captura = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
            if not self.captura.isOpened():
                self.captura = cv2.VideoCapture(0) 
            
            if not self.captura.isOpened():
                self.lbl_ejercicio.text = "⚠️ No se detecta una Webcam activa"
                return
        except Exception as e:
            self.lbl_ejercicio.text = "⚠️ Error de Hardware de Cámara"
            return
        
        Clock.schedule_interval(self.procesar_frame_universal, 1.0 / 30.0)

    def on_leave(self, *args):
        Clock.unschedule(self.procesar_frame_universal)
        try:
            if hasattr(self, 'captura') and self.captura.isOpened():
                self.captura.release()
            if hasattr(self, 'pose'):
                self.pose.close()
        except:
            pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        self.visor_camara = Image(size_hint=(1, 0.75), pos_hint={"center_x": 0.5, "top": 0.98})
        layout.add_widget(self.visor_camara)
        
        panel_inferior = BoxLayout(orientation='vertical', size_hint=(1, 0.22), pos_hint={"x": 0, "y": 0}, padding=12, spacing=5)
        self.lbl_ejercicio = MDLabel(text="Iniciando componentes...", halign="center", font_style="H6", theme_text_color="Custom", text_color=(1, 0.7, 0.2, 1))
        panel_inferior.add_widget(self.lbl_ejercicio)
        
        layout_numeros = BoxLayout(orientation='horizontal', padding=[40, 0, 40, 0])
        layout_numeros.add_widget(MDLabel(text="REPETICIONES:", font_style="Button", halign="left"))
        self.lbl_contador = MDLabel(text="0", font_style="H3", bold=True, halign="right")
        layout_numeros.add_widget(self.lbl_contador)
        panel_inferior.add_widget(layout_numeros)
        
        btn_terminar = MDRaisedButton(text="Finalizar Entrenamiento", md_bg_color=(0.9, 0.1, 0.1, 1), size_hint=(0.9, None), height=40, pos_hint={"center_x": 0.5}, on_release=lambda x: self.terminar())
        panel_inferior.add_widget(btn_terminar)
        
        layout.add_widget(panel_inferior)
        self.add_widget(layout)

    def calcular_angulo(self, p1, p2, p3):
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        x3, y3 = p3.x, p3.y
        angulo = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        angulo = abs(angulo)
        if angulo > 180.0:
            angulo = 360 - angulo
        return angulo

    def procesar_frame_universal(self, dt):
        try:
            ret, frame = self.captura.read()
            if not ret or frame is None:
                return
                
            frame = cv2.flip(frame, 1) 
            alto, ancho, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            resultados = self.pose.process(frame_rgb)
            
            if resultados.pose_landmarks:
                mp_drawing.draw_landmarks(frame, resultados.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                puntos = resultados.pose_landmarks.landmark
                ejercicio_actual = DATOS_USUARIO["ejercicio"]
                
                if ejercicio_actual in ["Flexiones", "Dominadas"]:
                    hombro = puntos[mp_pose.PoseLandmark.LEFT_SHOULDER]
                    codo = puntos[mp_pose.PoseLandmark.LEFT_ELBOW]
                    muneca = puntos[mp_pose.PoseLandmark.LEFT_WRIST]
                    angulo = self.calcular_angulo(hombro, codo, muneca)
                    
                    if angulo > 160 and self.estado_fase == "abajo":
                        self.contador_reps += 1
                        self.lbl_contador.text = str(self.contador_reps)
                        self.estado_fase = "arriba"
                    elif angulo < 90:
                        self.estado_fase = "abajo"
                            
                elif ejercicio_actual == "Sentadillas":
                    cadera = puntos[mp_pose.PoseLandmark.LEFT_HIP]
                    rodilla = puntos[mp_pose.PoseLandmark.LEFT_KNEE]
                    tobillo = puntos[mp_pose.PoseLandmark.LEFT_ANKLE]
                    angulo = self.calcular_angulo(cadera, rodilla, tobillo)
                    
                    if angulo > 160 and self.estado_fase == "abajo":
                        self.contador_reps += 1
                        self.lbl_contador.text = str(self.contador_reps)
                        self.estado_fase = "arriba"
                    elif angulo < 100:
                        self.estado_fase = "abajo"

            buffer = cv2.flip(frame, 0).tobytes()
            textura_kivy = Texture.create(size=(ancho, alto), colorfmt='bgr')
            textura_kivy.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.visor_camara.texture = textura_kivy
        except Exception as e:
            pass

    def terminar(self):
        dialog = MDDialog(
            title="🎯 ¡Buen Trabajo!",
            text=f"Completaste un total de {self.contador_reps} repeticiones.",
            buttons=[MDFlatButton(text="Volver", on_release=lambda x: self.salir_limpio(dialog))]
        )
        dialog.open()

    def salir_limpio(self, dialogo):
        dialogo.dismiss()
        self.manager.transition.direction = "right"
        self.manager.current = "bienvenida"


# ORQUESTADOR CENTRAL
class FlexRexApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Red'
        
        sm = ScreenManager()
        sm.add_widget(PantallaBienvenida(name='bienvenida'))
        sm.add_widget(PantallaRegistro(name='registro'))
        sm.add_widget(PantallaSugerenciaPlan(name='sugerencia_plan'))
        sm.add_widget(PantallaEjercicios(name='ejercicios'))
        sm.add_widget(PantallaEntrenamiento(name='entrenamiento_activo'))
        return sm

if __name__ == "__main__":
    FlexRexApp().run()