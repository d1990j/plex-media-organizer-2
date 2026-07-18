import flet as ft
from state import AppState
from logic import Logic
from ui import UI

def main(page: ft.Page):
    state = AppState()
    logic_ref = Logic(state)
    ui = UI(page, logic_ref)

    # Build the page
    ui.build_page()

    
##################### Run file ######################
if __name__ == "__main__":
    ft.run(main)