import flet as ft
from state import AppState
from ui import UI

def main(page: ft.Page):
    state = AppState()
    ui = UI(page, state)

    # Build the page
    ui.build_page()

    
##################### Run file ######################
if __name__ == "__main__":
    ft.run(main)