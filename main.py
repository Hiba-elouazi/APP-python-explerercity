import sys
import requests
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QHBoxLayout, QLineEdit, QApplication, QScrollArea, QFrame
from PySide6.QtGui import QPixmap, QFont, QPalette, QBrush
from PySide6.QtCore import Qt, QTimer
from modules import *
from widgets import *
from io import BytesIO
import datetime
from amadeus import Client, ResponseError
from PySide6.QtWidgets import (
    QListWidget, QMessageBox
)
widgets = None
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI if different
db = client["user_db"]  # Database name
users_collection = db["users"]  # Collection name for storing user data

from PySide6.QtWidgets import QSizePolicy

import bcrypt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QStackedWidget,
    QPushButton, QHBoxLayout, QGraphicsOpacityEffect
)
from PySide6.QtGui import QPixmap, QFont, QPalette, QBrush
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QHBoxLayout, QSizePolicy)
from PySide6.QtGui import QPixmap, QFont, QPalette, QBrush
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, QEvent
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QStackedWidget, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QFont, QPixmap, QPalette, QColor, QLinearGradient
from PySide6.QtCore import Qt

class OnboardingScreen(QWidget):
    def __init__(self):
     super().__init__()
     self.setWindowTitle("Welcome to CityExplorer")
     self.resize(360, 640)
     self.setMinimumSize(320, 480)

     self.setAutoFillBackground(True)

     self.layout = QVBoxLayout(self)
     self.layout.setContentsMargins(0, 0, 0, 0)
     self.layout.setAlignment(Qt.AlignCenter)

    # Stacked widget to hold pages
     self.stacked_widget = QStackedWidget()
     self.layout.addWidget(self.stacked_widget)

    # Create pages
     self.page1 = self.create_page("slide1.png", "🌍 Discover New Places", "Uncover hidden gems & must-see locations")
     self.page2 = self.create_page("slide.png", "🎭 Find Exciting Events", "Stay updated with concerts, festivals & activities")
     self.page3 = self.create_page("slide2.png", "🗺️ Plan Your Journey", "Your city, your adventure – plan your perfect trip")

     self.pages = [self.page1, self.page2, self.page3]  # Save pages in a list

    # Add pages to the stacked widget
     for page in self.pages:
        self.stacked_widget.addWidget(page)

     self.current_index = 0
     self.update_pagination()

    # Fade Animation Setup
     self.opacity_effect = QGraphicsOpacityEffect()
     self.stacked_widget.setGraphicsEffect(self.opacity_effect)
     self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
     self.animation.setDuration(500)

    # Timer for auto-switching pages
     self.timer = QTimer(self)
     self.timer.timeout.connect(self.next_page)
     self.timer.start(2000)

    def create_page(self, image_path, title_text, description_text):
     page = QWidget()
     page.setObjectName("page")

    # Background label
     background = QLabel(page)
     background.setPixmap(QPixmap(image_path))
     background.setScaledContents(True)

     background.setGeometry(0, 0, page.width(), page.height())  
     background.setGeometry(0, 0, self.width(), self.height())
     background.lower()  # Send background behind

    # Create a transparent container
     container = QWidget(page)
     container.setStyleSheet("background: transparent;")
     container_layout = QVBoxLayout(container)
     container_layout.setContentsMargins(30, 80, 30, 40)
     container_layout.setAlignment(Qt.AlignTop)
# Title
     title = QLabel(title_text)
     title.setFont(QFont("Segoe UI", 12, QFont.Bold))
     title.setAlignment(Qt.AlignCenter)
     title.setStyleSheet("""
     QLabel {
        color: #ffffff;
        background: rgba(0, 0, 0, 0.3);
        padding: 12px 20px;
        border-radius: 20px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
     }
     """)

# Description
     description = QLabel(description_text)
     description.setFont(QFont("Segoe UI", 10))
     description.setWordWrap(True)
     description.setAlignment(Qt.AlignCenter)
     description.setStyleSheet("""
     QLabel {
        color: #f0f0f0;
        background: rgba(0, 0, 0, 0.25);
        padding: 10px 16px;
        border-radius: 16px;
        font-weight: 500;
        letter-spacing: 0.5px;
     }
     """)

    # Pagination Dots
     pagination_layout = QHBoxLayout()
     pagination_layout.setAlignment(Qt.AlignCenter)
     dots = []
     for _ in range(3):
        dot = QLabel("•")
        dot.setFont(QFont("Arial", 20))
        dot.setStyleSheet("color: #A0A0A0;")
        dot.setAlignment(Qt.AlignCenter)
        pagination_layout.addWidget(dot)
        dots.append(dot)

    # Next Button
     next_button = QPushButton("Get Started")
     next_button.setStyleSheet(""" 
     QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6a11cb, stop:1 #2575fc);
        border: none;
        border-radius: 28px;
        color: white;
        font-family: "Segoe UI", sans-serif;
        font-size: 18px;
        font-weight: bold;
        padding: 14px 30px;
        margin-top: 20px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
     }
     QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8e2de2, stop:1 #4a00e0);
        transform: scale(1.05);
     }
     QPushButton:pressed {
        background-color: #5e35b1;
        transform: scale(0.98);
     }
     """)
     next_button.clicked.connect(self.next_page)
     next_button.hide()  # Hide initially


     container_layout.addWidget(title)
     container_layout.addSpacing(10)
     container_layout.addWidget(description)
     container_layout.addStretch()
     container_layout.addLayout(pagination_layout)
     container_layout.addWidget(next_button, alignment=Qt.AlignCenter)

    # Save references
     page.background = background
     page.dots = dots
     page.next_button = next_button
     page.container = container

     return page


    def next_page(self):
     if self.animation.state() == QPropertyAnimation.Running:
        return

     if self.current_index < len(self.pages) - 1:
        self.current_index += 1
        self.fade_to_page(self.current_index)

        if self.current_index == len(self.pages) - 1:
            page = self.pages[self.current_index]
            page.next_button.show()
            self.timer.stop()
        else:
            page = self.pages[self.current_index]
            page.next_button.hide()
     else:
        self.close()
        self.show_authentication_screen()

    def fade_to_page(self, index):
        self.animation.stop()
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(lambda: self.show_new_page(index))
        self.animation.start()

    def show_new_page(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.update_pagination()
        self.animation.finished.disconnect()
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()

    def update_pagination(self):
     page = self.pages[self.current_index]
     for i, dot in enumerate(page.dots):
        if i == self.current_index:
            dot.setStyleSheet("color: #FF4081;")
        else:
            dot.setStyleSheet("color: #A0A0A0;")
  
    def show_authentication_screen(self):
      """Show the authentication screen after onboarding is complete."""
      self.auth_screen = AuthScreen()
      self.auth_screen.show()
      self.close()

class AuthScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authentification")
        self.resize(360, 640)
        self.setMinimumSize(320, 480)
        # 📸 Background
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap("assets/bg.jpg"))
        self.background.setScaledContents(True)
        self.background.setGeometry(0, 0, self.width(), self.height())

        # 🔮 Main layout with blur panel
        self.overlay = QWidget(self)
        self.overlay.setGeometry(0, 0, 360, 640)

        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(20)

        opacity = QGraphicsOpacityEffect()
        opacity.setOpacity(0.4)  # Feel free to tweak

        self.overlay.setGraphicsEffect(blur)
        self.overlay.setGraphicsEffect(opacity)

        # 🧊 Foreground glassy form container
        self.container = QWidget(self)
        self.container.setGeometry(20, 60, 320, 520)
        self.container.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.12);
            border-radius: 20px;
        """)

        # Optional: Extra blur on container
        container_blur = QGraphicsBlurEffect()
        container_blur.setBlurRadius(10)
        self.container.setGraphicsEffect(container_blur)

        # 🌟 Add stacked login/signup to container
        self.stack = QStackedWidget(self.container)
        self.stack.setGeometry(10, 10, 300, 500)
        self.stack.addWidget(self.login_ui())
        self.stack.addWidget(self.signup_ui())

    def resizeEvent(self, event):
     if self.background.pixmap():
        self.background.setPixmap(
            QPixmap("assets/bg.jpg").scaled(
                self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
        )
     self.background.setGeometry(0, 0, self.width(), self.height())
     self.overlay.setGeometry(0, 0, self.width(), self.height())
     super().resizeEvent(event)

    def login_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Login")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)

        self.email_login = QLineEdit()
        self.password_login = QLineEdit()

        self.email_login.setPlaceholderText("Email Address")
        self.password_login.setPlaceholderText("Password")
        self.password_login.setEchoMode(QLineEdit.Password)

        for field in (self.email_login, self.password_login):
            field.setStyleSheet("""
                QLineEdit {
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    background-color: #f5f5f5;
                }
            """)

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #00C853;
                color: white;
                font-size: 16px;
                padding: 12px;
                border-radius: 8px;
            }
        """)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.email_login)
        layout.addWidget(self.password_login)
        layout.addWidget(login_btn)

        or_label = QLabel("Or login with")
        or_label.setAlignment(Qt.AlignCenter)
        or_label.setStyleSheet("color: #aaa; margin: 15px 0;")

        icons_layout = QHBoxLayout()
        for icon in ["G", "f"]:
            btn = QPushButton(icon)
            btn.setFixedSize(40, 40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #333;
                    color: white;
                    border-radius: 20px;
                    font-weight: bold;
                    font-size: 18px;
                }
            """)
            icons_layout.addWidget(btn)

        layout.addWidget(or_label)
        layout.addLayout(icons_layout)

        switch_label = QLabel("Don’t have an account? <a href='#'>Signup</a>")
        switch_label.setStyleSheet("color: white;")
        switch_label.setAlignment(Qt.AlignCenter)
        switch_label.setOpenExternalLinks(False)
        switch_label.linkActivated.connect(lambda: self.stack.setCurrentIndex(1))

        layout.addSpacing(15)
        layout.addWidget(switch_label)

        login_btn.clicked.connect(self.login_user)


        return widget

    def signup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Signup")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)

        self.username = QLineEdit()
        self.email_signup = QLineEdit()
        self.password_signup = QLineEdit()
        self.confirm = QLineEdit()
  
        self.username.setPlaceholderText("User name")
        self.email_signup.setPlaceholderText("Email address")
        self.password_signup.setPlaceholderText("Password")
        self.password_signup.setEchoMode(QLineEdit.Password)
        self.confirm.setPlaceholderText("Confirm password")
        self.confirm.setEchoMode(QLineEdit.Password)

        for field in (self.username, self.email_signup, self.password_signup, self.confirm):
            field.setStyleSheet("""
                QLineEdit {
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    background-color: #f5f5f5;
                }
            """)

        signup_btn = QPushButton("Signup")
        signup_btn.setStyleSheet("""
            QPushButton {
                background-color: #00C853;
                color: white;
                font-size: 16px;
                padding: 12px;
                border-radius: 8px;
            }
        """)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.username)
        layout.addWidget(self.email_signup)
        layout.addWidget(self.password_signup)
        layout.addWidget(self.confirm)
        layout.addWidget(signup_btn)

        or_label = QLabel("Or signup with")
        or_label.setAlignment(Qt.AlignCenter)
        or_label.setStyleSheet("color: #aaa; margin: 15px 0;")

        icons_layout = QHBoxLayout()
        for icon in ["G", "f"]:
            btn = QPushButton(icon)
            btn.setFixedSize(40, 40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #333;
                    color: white;
                    border-radius: 20px;
                    font-weight: bold;
                    font-size: 18px;
                }
            """)
            icons_layout.addWidget(btn)

        layout.addWidget(or_label)
        layout.addLayout(icons_layout)

        switch_label = QLabel("Already have an account? <a href='#'>Login</a>")
        switch_label.setStyleSheet("color: white;")
        switch_label.setAlignment(Qt.AlignCenter)
        switch_label.setOpenExternalLinks(False)
        switch_label.linkActivated.connect(lambda: self.stack.setCurrentIndex(0))

        layout.addSpacing(15)
        layout.addWidget(switch_label)
         
        signup_btn.clicked.connect(self.signup_user)
 
        return widget
    def signup_user(self):
      username = self.username.text()
      email = self.email_signup.text()
      password = self.password_signup.text()
      confirm = self.confirm.text()

      if password != confirm:
        QMessageBox.warning(self, "Error", "Passwords do not match!")
        return

      if users_collection.find_one({"email": email}):
        QMessageBox.warning(self, "Error", "Email already registered!")
        return

      hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
      users_collection.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password
      })

      QMessageBox.information(self, "Success", "Account created! Please log in.")
      self.stack.setCurrentIndex(0)  # Go to login page


    def login_user(self):
      email = self.email_login.text()
      password = self.password_login.text()

      user = users_collection.find_one({"email": email})
      if not user or not bcrypt.checkpw(password.encode(), user["password"]):
        QMessageBox.warning(self, "Error", "Invalid email or password")
        return

    # Login successful
      self.main_window = MainWindow()
      self.main_window.show()
      self.close()  # Close the login/signup window


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("ExplorCity")
        self.setFixedSize(360, 640)  # Mobile size

        # Main widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignTop)
    
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Add a QLabel for the weather icon
        self.ui.weather_icon = QLabel()
        self.ui.weather_icon.setFixedSize(60, 50)  # Set icon size
        self.ui.weather_label_layout = QHBoxLayout()  # Create horizontal layout
        self.ui.weather_label_layout.addWidget(self.ui.weather_label)
        self.ui.weather_label_layout.addWidget(self.ui.weather_icon)
        self.ui.weather_label_layout.addWidget(self.ui.weather_display)
        self.ui.weather_label_layout.setAlignment(Qt.AlignLeft)

        # Replace the single weather label with the new layout
        self.ui.weather_section = QWidget()
        self.ui.weather_section.setLayout(self.ui.weather_label_layout)
        self.ui.home_layout.addWidget(self.ui.weather_section)

        self.ui.events_layout = QVBoxLayout()

        self.ui.events_scroll_area = QScrollArea(self)  
        self.ui.events_scroll_area.setWidgetResizable(True)  # Make the scroll area resizable
        self.ui.events_scroll_area.setStyleSheet("border-radius: 15px; border: 2px solid #FFB6C1;")  # Rounded corners for the scroll area

        self.ui.events_container = QWidget(self)
        self.ui.events_container.setLayout(self.ui.events_layout)  # Set the layout for the events container

        self.ui.events_scroll_area.setWidget(self.ui.events_container)

        self.ui.events_display.setLayout(QVBoxLayout())  # Clear previous layout
        self.ui.events_display.layout().addWidget(self.ui.events_scroll_area)  # Add scroll area

        # Attractions Layout Setup (New part)
        self.ui.attractions_layout = QVBoxLayout()
        self.ui.attractions_scroll_area = QScrollArea(self)
        self.ui.attractions_scroll_area.setWidgetResizable(True)
        self.ui.attractions_scroll_area.setStyleSheet("border-radius: 15px; border: 2px solid #FFB6C1;") 
        self.ui.attractions_container = QWidget(self)
        self.ui.attractions_container.setLayout(self.ui.attractions_layout)
        self.ui.attractions_scroll_area.setWidget(self.ui.attractions_container)
        self.ui.attractions_display.setLayout(QVBoxLayout())
        self.ui.attractions_display.layout().addWidget(self.ui.attractions_scroll_area)


        # Connect the Search button to the update function
        self.ui.search_button.clicked.connect(self.update_dashboard)

        # Initialize the Explore Page
        self.explore_page = ExplorePage()
        
        global widgets
        widgets = self.ui
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        title = "ExplorCity"
        description = "ExploreCity App"
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_show_map.clicked.connect(self.buttonClick)
        widgets.btn_explore.clicked.connect(self.buttonClick)
        widgets.btn_meteo.clicked.connect(self.buttonClick)
        widgets.btn_AI.clicked.connect(self.buttonClick)

        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        self.show()

        # SET CUSTOM THEME
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))




    def update_dashboard(self):
        city = self.ui.location_input.text()
        if city:
            self.get_weather(city)  
            self.get_events(city)  
            self.get_attractions(city) 

    def get_weather(self, city):
      """Fetch weather data from WeatherStack API and update the UI with an icon."""
      api_key = "a8a167c4ee2f0d7f7796cc7bbf6274ad"  
      url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"

      try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and "current" in data:
            temp = data["current"]["temperature"]  
            weather_desc = data["current"]["weather_descriptions"][0]
            icon_url = data["current"]["weather_icons"][0] 
            # Update weather text
            self.ui.weather_display.setText(f"{city}: {weather_desc}, {temp}°C")

            # Fetch and display weather icon
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(icon_url).content)
            self.ui.weather_icon.setPixmap(pixmap)

        else:
            self.ui.weather_display.setText("City not found or API error.")
            self.ui.weather_icon.clear()

      except Exception as e:
        self.ui.weather_display.setText("Error fetching weather data.")
        self.ui.weather_icon.clear()
        print(f"Weather API Error: {e}")


    def get_events(self, city):
      api_key = "1mkxTalQ0Ub70YsyAfH3GoEGXhwzuUxk"  
      url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={api_key}&city={city}"

      try:
        response = requests.get(url)
        print("API Response Status Code:", response.status_code)  
        print("API Response Content:", response.text) 

        data = response.json()

        if response.status_code == 200 and "_embedded" in data:
            events = data["_embedded"]["events"]

            # Clear previous events
            for i in reversed(range(self.ui.events_layout.count())):
                widget = self.ui.events_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

            if not events:
                self.ui.events_display.setText("Aucun événement trouvé.")
            else:
                self.ui.events_display.setText("")  # Clear previous message
                for event in events:  # Display first 5 events
                    event_name = event["name"]
                    event_date = event["dates"]["start"]["localDate"] if "dates" in event else "Date inconnue"
                    image_url = event["images"][0]["url"] if "images" in event else None  # Get image

                    event_frame = QFrame()
                    event_frame.setStyleSheet("""
                        border: 1px solid #FFB6C1; 
                        border-radius: 15px; 
                        padding: 15px; 
                        background-color: #FFF0F5; 
                        margin-bottom: 20px;
                        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                    """) 
                    event_layout = QHBoxLayout(event_frame)

                    if image_url:
                        pixmap = QPixmap()
                        pixmap.loadFromData(requests.get(image_url).content)
                        image_label = QLabel()
                        image_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                        image_label.setFixedSize(150, 150)
                        image_label.setStyleSheet("border-radius: 10px;")  
                        event_layout.addWidget(image_label)

                    event_name_label = QLabel(f"<b>{event_name}</b>")
                    event_name_label.setStyleSheet("color: #FF6F61; font-size: 16px; font-family: 'Arial'; padding-left: 10px;")
                    event_name_label.setAlignment(Qt.AlignLeft)

                    event_date_label = QLabel(f"📅 {event_date}")
                    event_date_label.setStyleSheet("color: #4A4A4A; font-size: 12px; font-family: 'Arial'; padding-left: 10px;")
                    event_date_label.setAlignment(Qt.AlignLeft)

                    text_layout = QVBoxLayout()
                    text_layout.addWidget(event_name_label)
                    text_layout.addWidget(event_date_label)

                    # Add the name, date, and image to the event layout
                    event_layout.addLayout(text_layout)

                    self.ui.events_layout.addWidget(event_frame)

        else:
            self.ui.events_display.setText("Aucun événement trouvé ou erreur API.")

      except Exception as e:
        self.ui.events_display.setText("Erreur de récupération des événements.")
        print(f"Ticketmaster API Error: {e}")
    def get_attractions(self, city):
      api_key = "fsq3bWhASwNmkqILh358fBbTglc16fotf5aZ/tuCV1Uav+k="  
      url = "https://api.foursquare.com/v3/places/search"
      headers = {
        "Accept": "application/json",
        "Authorization": api_key
      }
      params = {
        "near": city,
        "categories": "16000",  
        "limit": 5  
      }

      try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if response.status_code == 200 and "results" in data:
            attractions = data["results"]

            # Remove previous displayed attractions
            for i in reversed(range(self.ui.attractions_layout.count())):
                widget = self.ui.attractions_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

            if not attractions:
                self.ui.attractions_display.setText("No attractions found.")
            else:
                self.ui.attractions_display.setText("")  # Clear previous message
                for attraction in attractions:
                    name = attraction.get("name", "Unknown name")
                    address = attraction.get("location", {}).get("formatted_address", "Address unavailable")
                    fsq_id = attraction.get("fsq_id")  

                    attraction_frame = QFrame()
                    attraction_frame.setStyleSheet("""
                        border: 2px solid #FFB6C1; 
                        border-radius: 15px; 
                        padding: 15px; 
                        background-color: #FFF0F5; 
                        margin-bottom: 20px;
                        box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.1);
                    """)  

                    attraction_layout = QHBoxLayout(attraction_frame)

                    text_label = QLabel(f"<b>{name}</b><br>{address}")
                    text_label.setWordWrap(True)
                    text_label.setAlignment(Qt.AlignVCenter)
                    text_label.setStyleSheet("""
                        font-size: 16px; 
                        color: #FF6F61; 
                        font-family: 'Arial'; 
                        padding-left: 15px;
                    """)
                    attraction_layout.addWidget(text_label)

                    image_label = QLabel()
                    image_label.setFixedSize(120, 120)
                    pixmap = self.get_attraction_image(fsq_id, api_key)
                    if pixmap:
                        image_label.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    image_label.setStyleSheet("border-radius: 10px; border: 2px solid #FFB6C1;")  
                    attraction_layout.addWidget(image_label)

                    self.ui.attractions_layout.addWidget(attraction_frame)

        else:
            self.ui.attractions_display.setText("Error: Could not retrieve attractions.")

      except Exception as e:
        self.ui.attractions_display.setText("Error retrieving attractions.")
        print(f"Foursquare API Error: {e}")

# Function to fetch an image for the attraction
    def get_attraction_image(self, fsq_id, api_key):
      """ Fetches an image for the attraction via Foursquare API. """
      url = f"https://api.foursquare.com/v3/places/{fsq_id}/photos"
      headers = {
        "Accept": "application/json",
        "Authorization": api_key
      }

      try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if response.status_code == 200 and isinstance(data, list) and len(data) > 0:
            photo = data[0]  
            photo_url = f"{photo['prefix']}original{photo['suffix']}"  

            # Download the image
            image_response = requests.get(photo_url)
            if image_response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(BytesIO(image_response.content).read())  # Load the image in memory
                return pixmap
      except Exception as e:
        print(f"Error fetching image: {e}")

      return None  # If no image found

    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_show_map":
            if not hasattr(self, 'show_map_page'):
               self.show_map_page = ShowMapPage()
        
            widgets.stackedWidget.addWidget(self.show_map_page)
            widgets.stackedWidget.setCurrentWidget(self.show_map_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))


        if btnName == "btn_explore":
         if not hasattr(self, 'explore_page'):
            self.explore_page = ExplorePage()
           
         widgets.stackedWidget.addWidget(self.explore_page)  
         widgets.stackedWidget.setCurrentWidget(self.explore_page)  


        if btnName == "btn_meteo":
         if not hasattr(self, 'weather_dashboard'):
            self.weather_dashboard = WeatherDashboard()

         widgets.stackedWidget.addWidget(self.weather_dashboard)
         widgets.stackedWidget.setCurrentWidget(self.weather_dashboard)  

        if btnName == "btn_AI":
         if not hasattr(self, 'ai_assistant'):
            self.ai_assistant = AIAssistant()

         widgets.stackedWidget.addWidget(self.ai_assistant)  
         widgets.stackedWidget.setCurrentWidget(self.ai_assistant)  

        if btnName == "btn_show_settings":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')


    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')



class WeatherDashboard(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize layout
        self.layout = QVBoxLayout()

        self.title_label = QLabel("Weather Dashboard")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 32px; 
            color: #FF5A5F; 
            font-weight: bold; 
            padding-bottom: 20px;
            font-family: 'Segoe UI', sans-serif;
        """)
        self.layout.addWidget(self.title_label)

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city name")
        self.city_input.setStyleSheet("""
            font-size: 18px; 
            padding: 10px; 
            border-radius: 25px; 
            border: 2px solid #FF5A5F; 
            background-color: #F8D7DA;
            color: #FF5A5F;
        """)
        self.layout.addWidget(self.city_input)

        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.setStyleSheet("""
            font-size: 20px; 
            background-color: #FF5A5F; 
            color: white; 
            border-radius: 25px; 
            padding: 10px;
            font-weight: bold;
        """)
        self.search_button.clicked.connect(self.search_weather)
        self.layout.addWidget(self.search_button)

        # Display for the current weather
        self.weather_details = QLabel("Temperature: --°C\nDescription: --\nHumidity: --%")
        self.weather_details.setStyleSheet("""
            font-size: 20px; 
            color: #333333; 
            font-family: 'Segoe UI', sans-serif;
            padding-top: 20px;
        """)
        self.layout.addWidget(self.weather_details)

        # Display for the forecast (next 5 days)
        self.forecast_layout = QVBoxLayout()
        self.forecast_label = QLabel("5-Day Forecast")
        self.forecast_label.setStyleSheet("""
            font-size: 24px; 
            color: #FF5A5F; 
            font-weight: bold; 
            padding-top: 30px;
            font-family: 'Segoe UI', sans-serif;
        """)
        self.forecast_layout.addWidget(self.forecast_label)

        self.forecast_container = QVBoxLayout()  
        self.forecast_layout.addLayout(self.forecast_container)

        self.layout.addLayout(self.forecast_layout)

        # Date display for the current weather
        self.date_label = QLabel("Date: --")
        self.date_label.setStyleSheet("""
            font-size: 16px; 
            color: #FF5A5F;
            font-weight: bold;
            font-family: 'Segoe UI', sans-serif;
        """)
        self.layout.addWidget(self.date_label)

        self.setLayout(self.layout)
        self.setWindowTitle("Weather Dashboard")
        self.setStyleSheet("""
            background-color: #FFF0F3;
            border-radius: 20px;
            padding: 30px;
            font-family: 'Segoe UI', sans-serif;
        """)

    def search_weather(self):
        city = self.city_input.text()
        api_key = "bac9ee899b14fc8ae5397cc635e70ceb" 
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        weather_data = response.json()

        if weather_data.get("cod") != "200":
            self.weather_details.setText("City not found!")
            return

        self.update_weather(weather_data)

    def update_weather(self, weather_data):
        # Clear previous forecast data
        for i in range(self.forecast_container.count()):
            widget = self.forecast_container.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Current weather details
        current_weather = weather_data['list'][0]
        weather_description = current_weather['weather'][0]['description']
        icon_code = current_weather['weather'][0]['icon']
        temperature = current_weather['main']['temp']
        humidity = current_weather['main']['humidity']
        city = weather_data['city']['name']

        # URL for the weather icon
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}.png"

        # Load the weather icon using QPixmap
        icon_pixmap = self.load_icon(icon_url)

        # Update current weather details
        self.weather_details.setText(f"Temperature: {temperature}°C\nDescription: {weather_description}\nHumidity: {humidity}%")
        self.date_label.setText(f"City: {city}\nDate: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Loop through the forecast and display it
        for day_data in weather_data['list'][::8]:  # Get data for every 24 hours (3-hour intervals in OpenWeatherMap)
            forecast_date = datetime.datetime.utcfromtimestamp(day_data['dt'])
            forecast_description = day_data['weather'][0]['description']
            forecast_icon_code = day_data['weather'][0]['icon']
            forecast_temperature = day_data['main']['temp']
            forecast_humidity = day_data['main']['humidity']

            # Forecast row layout
            forecast_row = QHBoxLayout()

            # Date label for the forecast day
            date_label = QLabel(forecast_date.strftime("%A, %d %b"))
            date_label.setStyleSheet("""
                font-size: 18px; 
                color: #333333; 
                font-weight: bold;
            """)
            forecast_row.addWidget(date_label)

            # Weather icon for the forecast
            forecast_icon_url = f"https://openweathermap.org/img/wn/{forecast_icon_code}.png"
            icon_pixmap = self.load_icon(forecast_icon_url)

            icon_label = QLabel()
            icon_label.setPixmap(icon_pixmap)
            icon_label.setAlignment(Qt.AlignCenter) 
            icon_label.setFixedSize(80, 80)  
            forecast_row.addWidget(icon_label)

            temp_label = QLabel(f"{forecast_temperature}°C")
            temp_label.setStyleSheet("""
                font-size: 18px; 
                color: #333333;
            """)
            forecast_row.addWidget(temp_label)

            description_label = QLabel(f"{forecast_description.capitalize()}")
            description_label.setStyleSheet("""
                font-size: 18px; 
                color: #333333;
            """)
            forecast_row.addWidget(description_label)

            self.forecast_container.addLayout(forecast_row)

    def load_icon(self, icon_url):
        """ Fetch and load the icon using QPixmap """
        try:
            response = requests.get(icon_url)
            if response.status_code == 200:
                icon_pixmap = QPixmap()
                icon_pixmap.loadFromData(response.content)
                return icon_pixmap
            else:
                print(f"Failed to load icon: {icon_url}")
                return QPixmap()  
        except Exception as e:
            print(f"Error loading icon: {e}")
            return QPixmap() 

import requests
from PySide6.QtWidgets import QMessageBox

# Get access token
def get_access_token(client_id, client_secret):
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")

# Search hotels
def search_hotels(city_code, access_token):
    url = "https://test.api.amadeus.com/v1/shopping/hotel-offers"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "cityCode": city_code,
        "adults": 1,
        "roomQuantity": 1,
        "radius": 50,
        "radiusUnit": "KM",
        "paymentPolicy": "NONE",
        "includeClosed": False,
        "bestRateOnly": True,
        "view": "FULL",
        "sort": "PRICE"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

class ExplorePage(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)

        # --- STACKED LAYOUT TO SWITCH VIEWS ---
        self.stacked_layout = QStackedLayout()
        self.main_layout.addLayout(self.stacked_layout)

        # --- PAGE 1: Explore Buttons ---
        self.button_page = QWidget()
        button_layout = QVBoxLayout(self.button_page)
        button_layout.setAlignment(Qt.AlignCenter)

        self.hotels_button = QPushButton("Hotels")
        self.hotels_button.setFixedSize(700, 200)
        self.hotels_button.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                font-weight: bold;
                color: white;
                border: none;
                padding: 20px;
                border-radius: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #84fab0, stop:1 #8fd3f4);
                box-shadow: 0px 10px 15px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #a6c1ee, stop:1 #fbc2eb);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #6ec6ca;
            }
        """)

        self.restaurants_button = QPushButton("Restaurants")
        self.restaurants_button.setFixedSize(700, 200)
        self.restaurants_button.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                font-weight: bold;
                color: white;
                border: none;
                padding: 20px;
                border-radius: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #84fab0, stop:1 #8fd3f4);
                box-shadow: 0px 10px 15px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #a6c1ee, stop:1 #fbc2eb);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #6ec6ca;
            }
        """)

        button_layout.addWidget(self.hotels_button)
        button_layout.addWidget(self.restaurants_button)
        self.stacked_layout.addWidget(self.button_page)

        # --- PAGE 2: Hotel Search ---
        self.hotel_search_page = QWidget()
        hotel_layout = QVBoxLayout(self.hotel_search_page)
        hotel_layout.setAlignment(Qt.AlignTop)

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city name")
        self.city_input.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 10px;")

        self.search_button = QPushButton("Search Hotels")
        self.search_button.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 10px; background-color: #3498db; color: white;")

        self.hotel_list = QListWidget()

        hotel_layout.addWidget(self.city_input)
        hotel_layout.addWidget(self.search_button)
        hotel_layout.addWidget(self.hotel_list)
        self.stacked_layout.addWidget(self.hotel_search_page)

        # ADD RETURN BUTTON TO PAGE 2
        self.return_button = QPushButton("Return")
        self.return_button.setFixedSize(100, 40)
        self.return_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                padding: 10px;
                border-radius: 10px;
                background-color:#FF69B4; 
                color: white;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        hotel_layout.addWidget(self.return_button)

        # CONNECT BUTTON TO SWITCH TO HOTEL SEARCH VIEW
        self.hotels_button.clicked.connect(self.show_hotel_search)
        self.search_button.clicked.connect(self.perform_hotel_search)
        self.return_button.clicked.connect(self.show_main_page)
 
        # --- PAGE 3: Restaurant Search ---
        self.restaurant_search_page = QWidget()
        restaurant_layout = QVBoxLayout(self.restaurant_search_page)
        restaurant_layout.setAlignment(Qt.AlignTop)

        self.restaurant_input = QLineEdit()
        self.restaurant_input.setPlaceholderText("Enter city name for restaurants")
        self.restaurant_input.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 10px;")

        self.restaurant_search_button = QPushButton("Search Restaurants")
        self.restaurant_search_button.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 10px; background-color: #3498db; color: white;")

        self.restaurant_scroll_area = QScrollArea()
        self.restaurant_scroll_area.setWidgetResizable(True)
        self.restaurant_scroll_area.setStyleSheet("border-radius: 15px; border: 2px solid #FFB6C1;")

        self.restaurant_layout = QVBoxLayout()
        self.restaurant_container = QWidget()
        self.restaurant_container.setLayout(self.restaurant_layout)

        self.restaurant_scroll_area.setWidget(self.restaurant_container)

        restaurant_layout.addWidget(self.restaurant_input)
        restaurant_layout.addWidget(self.restaurant_search_button)
        restaurant_layout.addWidget(self.restaurant_scroll_area)

        self.stacked_layout.addWidget(self.restaurant_search_page)
        # ADD RETURN BUTTON TO PAGE 3
        self.return_button = QPushButton("Return")
        self.return_button.setFixedSize(100, 40)
        self.return_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                padding: 10px;
                border-radius: 10px;
                background-color:#FF69B4; 
                color: white;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        restaurant_layout.addWidget(self.return_button)

        # CONNECT BUTTONS TO SWITCH VIEWS
        self.hotels_button.clicked.connect(self.show_hotel_search)
        self.restaurants_button.clicked.connect(self.show_restaurant_search)

        self.search_button.clicked.connect(self.perform_hotel_search)
        self.restaurant_search_button.clicked.connect(self.perform_restaurant_search)
        self.return_button.clicked.connect(self.show_main_page)
 
    def show_restaurant_search(self):
        self.stacked_layout.setCurrentWidget(self.restaurant_search_page)
    def show_hotel_search(self):
        self.stacked_layout.setCurrentWidget(self.hotel_search_page)
    def show_main_page(self):
        self.stacked_layout.setCurrentWidget(self.button_page)

    def perform_restaurant_search(self):
        city_name = self.restaurant_input.text().strip()
        if not city_name:
            QMessageBox.warning(self, "Input Error", "Please enter a city name for restaurants.")
            return

        api_key = "fsq3e9BrUQUIeZxpagEB8lZxQrtdq80HrkDdFC3Llka+JQI="  
        restaurants = self.search_restaurants(city_name, api_key)

        self.clear_restaurant_layout()

    
        for restaurant in restaurants:
                name = restaurant.get("name", "No Name")
                location = restaurant.get("location", {})
                address = location.get("formatted_address", "No address available")
                rating = restaurant.get("rating", "N/A")
                photos = restaurant.get("photos", [])

                fsq_id = restaurant.get("fsq_id")
                if fsq_id:
                  details = self.get_place_details(fsq_id, api_key)
                  rating = details.get("rating", rating)  
                  photos = details.get("photos", photos) 
                photo_url = "https://via.placeholder.com/150"
                if photos:
                    photo = photos[0]
                    prefix = photo.get("prefix", "")
                    suffix = photo.get("suffix", "")
                    photo_url = f"{prefix}original{suffix}"

                # Create a frame for each restaurant with image and info
                frame = QFrame()
                frame.setStyleSheet("""
                    QFrame {
                        border: 2px solid #FFB6C1;
                        border-radius: 15px;
                        padding: 10px;
                        background-color: white;
                        colour: black;
                    }
                """)

                frame_layout = QHBoxLayout(frame)

                # Image
                try:
                    img_data = requests.get(photo_url).content
                    pixmap = QPixmap()
                    pixmap.loadFromData(img_data)
                    image_label = QLabel()
                    image_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                except:
                    image_label = QLabel("No Image")

                frame_layout.addWidget(image_label)

                # Text Info
                info_layout = QVBoxLayout()
                info_layout.addWidget(QLabel(f"<b>{name}</b>"))
                info_layout.addWidget(QLabel(f"📍 Address: {address}"))
                info_layout.addWidget(QLabel(f"⭐ Rating: {rating}"))

                frame_layout.addLayout(info_layout)

                self.restaurant_layout.addWidget(frame)

    def get_place_details(self, fsq_id, api_key):
        url = f"https://api.foursquare.com/v3/places/{fsq_id}"
        headers = {
            "Authorization": f"{api_key}",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return {}
    def clear_restaurant_layout(self):
     while self.restaurant_layout.count():
        item = self.restaurant_layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()

    def search_restaurants(self, city_name, api_key):
        search_url = f"https://api.foursquare.com/v3/places/search?query=restaurant&near={city_name}&limit=5"
        headers = {
            "Authorization": f"{api_key}",
            "Accept": "application/json"
        }

        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            results = response.json().get("results", [])
            detailed_restaurants = []
            for restaurant in results:
                fsq_id = restaurant["fsq_id"]
                
                detailed_restaurants.append(restaurant)  
            return detailed_restaurants
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            QMessageBox.warning(self, "API Error", "Failed to fetch restaurant details.")
            return []

# Inside your class
    def perform_hotel_search(self):
      client_id = 'X2cCUdPzmWTGRmjqHE76Mj8pwJ9MtF8o'
      client_secret = 'gPVsq9G9C2RmwpTG'

      city = self.city_input.text().strip()
      if not city:
        QMessageBox.warning(self, "Input Error", "Please enter a city name.")
        return

      access_token = get_access_token(client_id, client_secret)
      if not access_token:
        QMessageBox.warning(self, "Authentication Error", "Failed to get access token.")
        return

      city_code = self.get_city_code(city, access_token)
      if not city_code:
        QMessageBox.warning(self, "City Not Found", "Could not find city code.")
        return

      hotels_data = search_hotels(city_code, access_token)
      self.hotel_list.clear()

      hotels = hotels_data.get("data", [])
      if not hotels:
        self.hotel_list.addItem("No hotels found.")
        return

      for hotel in hotels:
        name = hotel["hotel"]["name"]
        address = hotel["hotel"]["address"].get("lines", [""])[0]
        self.hotel_list.addItem(f"{name}\n{address}")

    def get_city_code(self, city_name, access_token):
      try:
        url = "https://test.api.amadeus.com/v1/reference-data/locations"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        params = {
            "keyword": city_name,
            "subType": "CITY"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json().get('data', [])
            if data:
                city_code = data[0]['id']
                print(f"Found city code: {city_code}")
                return city_code
        else:
            print(f"City code fetch error: {response.text}")
            return None
      except Exception as e:
        print(f"Error fetching city code: {e}")
        return None


class AIAssistant(QWidget):
    def __init__(self):
        super().__init__()

        self.api_key = "AIzaSyA692v-PljbLWqj55kYBjel4TjjlPc1XW0"  
        self.api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

        # Main Layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        # AI Avatar
        self.ai_avatar = QLabel(self)
        pixmap = QPixmap("chibi_ai.png") 
        self.ai_avatar.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.ai_avatar.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.ai_avatar)

        self.title_label = QLabel("💖 Your AI Bestie 💖")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Poppins", 26, QFont.Bold))
        self.title_label.setStyleSheet("color: #FF69B4; text-shadow: 2px 2px 10px #FFC0CB;")
        self.layout.addWidget(self.title_label)

        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Type your question, cutie! 💕")
        self.query_input.setStyleSheet("""
            font-size: 20px;
            padding: 15px;
            border-radius: 25px;
            border: 3px solid #FFB6C1;
            background: rgba(255, 240, 245, 0.8);
            color: #6A0572;
        """)
        self.layout.addWidget(self.query_input)

        self.send_button = QPushButton("💌 Ask AI")
        self.send_button.setStyleSheet("""
            font-size: 20px;
            background: linear-gradient(to right, #FF69B4, #FFB6C1);
            color: white;
            border-radius: 30px;
            padding: 15px;
            font-weight: bold;
            border: 3px solid #FF1493;
            transition: all 0.3s ease-in-out;
        """)
        self.send_button.clicked.connect(self.get_ai_response)
        self.layout.addWidget(self.send_button)

        self.response_display = QLabel("💬 Your AI bestie is waiting for you...")
        self.response_display.setStyleSheet("""
            font-size: 20px;
            color: #6A0572;
            background: rgba(255, 240, 245, 0.9);
            border-radius: 25px;
            padding: 15px;
            border: 3px solid #FF69B4;
            box-shadow: 0px 0px 20px #FF69B4;
        """)
        self.response_display.setWordWrap(True)
        self.layout.addWidget(self.response_display)

        self.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget {
                background: url("cute_pastel_background.jpg");  /* Use a dreamy pastel background */
                background-size: cover;
                font-family: 'Poppins', sans-serif;
            }

            QPushButton:hover {
                background: linear-gradient(to right, #FF1493, #FF69B4);
                transform: scale(1.1);
                box-shadow: 0px 0px 15px #FF69B4;
            }

            QLineEdit:hover {
                background: rgba(255, 250, 250, 1);
                border: 3px solid #FF1493;
            }
        """)

    # AI Response Function
    def get_ai_response(self):
        user_query = self.query_input.text().strip()
        if user_query:
            self.response_display.setText("Typing... ⌨️💖")
            QTimer.singleShot(1000, lambda: self.fetch_ai_response(user_query))  # Typing effect delay

    def fetch_ai_response(self, query):
        response = self.query_with_gemini(query)
        try:
            if response and 'candidates' in response:
                ai_response_text = response['candidates'][0]['content']['parts'][0]['text']
                self.animate_text(ai_response_text)  
            else:
                self.response_display.setText("Oops! I couldn't find an answer. 🥺")
        except Exception as e:
            print("Error:", e)
            self.response_display.setText("Oops! Something went wrong. 😭")

    def animate_text(self, text):
        self.response_display.setText("") 
        self.index = 0
        self.text = text
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.show_next_character)
        self.typing_timer.start(50)  

    def show_next_character(self):
        if self.index < len(self.text):
            self.response_display.setText(self.response_display.text() + self.text[self.index])
            self.index += 1
        else:
            self.typing_timer.stop()

    def query_with_gemini(self, query):
        try:
            url = f"{self.api_endpoint}?key={self.api_key}"
            headers = {'Content-Type': 'application/json'}
            payload = {"contents": [{"parts": [{"text": query}]}]}

            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print("Request Error:", e)
            return None
import folium
from folium import plugins
from PySide6.QtWebEngineWidgets import QWebEngineView

class ShowMapPage(QWidget):
    def __init__(self):
        super().__init__()

        # Set up layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

    
        # Create map (using Folium)
        self.create_map()

        # Set up WebEngineView to display the map
        self.map_view = QWebEngineView()  
        with open("map_template.html", "r", encoding="utf-8") as f:
            html = f.read()
        self.map_view.setHtml(html)
        self.layout.addWidget(self.map_view, stretch=1)
        # Move Button
        self.move_button = QPushButton("Map")
        self.move_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff416c, stop:1 #ff4b2b);
                border: none;
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 25px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff4b2b, stop:1 #ff416c);
            }
        """)
        self.move_button.clicked.connect(self.move_to_new_location)
        self.layout.addWidget(self.move_button)

        self.setLayout(self.layout)

    def move_to_new_location(self):
        # Move to New York (dynamic move)
        lat, lon = 40.7128, -74.0060
        self.map_view.page().runJavaScript(f"moveTo({lat}, {lon});")

    def create_map(self):
     """Create a beautiful map styled like Google Maps"""
     self.map = folium.Map(
        location=[48.8566, 2.3522],
        zoom_start=13,
        tiles='CartoDB positron'  # Google Maps light style
     )

     folium.Marker(
        [48.8566, 2.3522],
        popup="Paris",
        icon=folium.Icon(color="pink", icon="info-sign")
     ).add_to(self.map)
     folium.TileLayer(
       tiles='https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
       attr='OpenStreetMap HOT',
       name='Hot Style'
     ).add_to(self.map)

    # Optional: Add nice plugins
     plugins.Fullscreen(position='topright').add_to(self.map)
     plugins.MousePosition().add_to(self.map)
     plugins.LocateControl().add_to(self.map)


    def update_map_location(self, lat, lon):
        """Update the map to center on a new location"""
        self.map = folium.Map(location=[lat, lon], zoom_start=12)
        folium.Marker([lat, lon], popup="New Location").add_to(self.map)
        self.map_view.setHtml(self.map._repr_html_())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set dark theme for the whole application
    window = OnboardingScreen()
    window.show()

    sys.exit(app.exec())