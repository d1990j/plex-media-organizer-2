import flet as ft
from constants import Keys

@ft.observable
class AppState:
    def __init__(self):
        self.selected_file_index = {Keys.STAGED: False, Keys.INDEX: 0}
        self.media_files = []
        self.staged_list = []
        self.source_directory_path = ""
        self.destination_directory_path = ""