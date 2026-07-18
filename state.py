import flet as ft

@ft.observable
class AppState:
    def __init__(self):
        self.selected_file_index = 0
        self.media_files = []
        self.staged_list = []
        self.source_directory_path = ft.Text(value="Not set")
        self.destination_directory_path = ft.Text(value="Not set")