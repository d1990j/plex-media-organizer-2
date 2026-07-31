import flet as ft
from constants import Keys
from mediafile import MediaFile

@ft.observable
class AppState:
    def __init__(self):
        self.selected_file_index = {Keys.STAGED: False, Keys.INDEX: 0}
        self.media_files: list[MediaFile] = []
        self.staged_list: list[MediaFile] = []
        self.source_directory_path = ""
        self.destination_directory_path = ""
        self.last_staged_was_tv = False