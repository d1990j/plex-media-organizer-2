import flet as ft
from state import AppState
from ui import UI

class Logic:
    def __init__(self, state: AppState, ui: UI):
        self.state = state
        self.ui = ui