import flet as ft
from state import AppState
from ui import ui

class logic:
    def __init__(self, state: AppState, ui: ui):
        self.state = state
        self.ui = ui