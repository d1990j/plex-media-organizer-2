import flet as ft
from state import AppState
import os
import ui

class Logic:
    def __init__(self, state: AppState):
        self.state = state

    ##################### LOGIC ############################
    async def browse_source_directory(self, ui: ui.UI):
        """Open a dialog to select a directory"""
        print("Browse source directory selected") # Testing
        self.state.source_directory_path = await ft.FilePicker().get_directory_path() or self.state.source_directory_path
        print(f"Source directory set to {self.state.source_directory_path}")
        # Update the source directory text
        ui.source_directory_path.value = self.state.source_directory_path
        ui.source_directory_path.update()
        self.load_media_files(ui)
        # toggle the commit button if a directory is chosen for source and destination
        self.toggle_commit_button()

    async def browse_destination_directory(self, ui: ui.UI):
        """Open a dialog to select a directory"""
        print("Browse destination directory selected") # testing
        self.state.destination_directory_path = await ft.FilePicker().get_directory_path() or self.state.destination_directory_path
        print(f"Destination directory set to {self.state.destination_directory_path}")
        # Update the destination directory text in UI
        ui.destination_directory_path.value = self.state.destination_directory_path
        ui.destination_directory_path.update()
        # toggle the commit button if a directory is chosen for source and destination
        self.toggle_commit_button()

    # def stage_file():
    #     """Stage selected file for naming."""
    #     if tv_movie_switch.value: # If True, is Movie, otherwise is TV
    #         print("Stage start for Movie file")
    #     else:
    #         print("Stage start for TV file")

    # def commit_files():
    #     """Commit the staged files, completing change"""
    #     print("Commit files selected")

    def select_source_file(self, index: int, ui: ui.UI):
        # update the selected file index
        self.state.selected_file_index = index

        # reload the files to update highlights
        self.load_media_files(ui)

        # Fill the text fields in selected file info
        ui.fill_selected_file_fields(
            self.state.media_files[index]["name"],
            self.state.media_files[index]["year"],
            self.state.media_files[index]["tv_movie"],
            self.state.media_files[index]["season"],
            self.state.media_files[index]["episode"]
        )

    def toggle_commit_button(self):
          print("Commit button pressed")

    def load_media_files(self, ui: ui.UI):
        """Attempt to load the media files from directory"""
        # If a directory is chosen
        if self.state.source_directory_path != "No path selected":
            # Reset media files
            self.state.media_files.clear()
            ui.file_list.controls.clear()

            # Find each file in the chosen directory that has the correct filetype and add to media files 
            for file in os.listdir(self.state.source_directory_path):
                    if file.lower().endswith((".mp4", ".mkv", ".avi", ".mov", ".mp3", ".flac")):
                        self.state.media_files.append({"name": file, "tv_movie": False, "new_name": "", "year": "", "season": "", "episode": ""})

            # Cycle through each item in the files and add the name to the list
            for index, item in enumerate(self.state.media_files):
                tile = ft.ListTile(
                        title=ft.Text(item["name"]),
                        on_click=ui.on_source_file_clicked,
                        data=index,
                        selected_color=ft.Colors.BLUE_500
                )
                if index == self.state.selected_file_index:
                    tile.selected = True
                else:
                    tile.selected = False
                ui.file_list.controls.append(tile)
                
                #Update the file list
                ui.file_list.update()

    # def play_media_file():
    #     """Attempt to play the media file"""
    #     try:
    #         index = state.selected_file_index
    #         file = state.media_files[index]["name"]
    #         filepath = os.path.join(state.source_directory_path.value, file)
    #         print(f"Filepath created: {filepath}")
    #         # Determine OS, nt for windows, posix for mac/linux
    #         if os.name == "nt":
    #             print("OS set to nt")
    #             os.startfile(filepath)
    #         elif os.name == "posix":
    #             print("OS set to posix")
    #             subprocess.run(["open", filepath])
    #     except:
    #         print("Unable to play media")

    # def update_on_tv_movie_switch():
    #     """Update the text boxes upon switch change"""
    #     season_textfield.disabled = tv_movie_switch.value
    #     episode_textfield.disabled = tv_movie_switch.value
    #     print(f"Season textfield disabled set to: {season_textfield.disabled}")
    #     print(f"Episode textfield disabled set to: {episode_textfield.disabled}")
    #     season_textfield.update()
    #     episode_textfield.update()