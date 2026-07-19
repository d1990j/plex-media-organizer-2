import flet as ft
import state
import os
import ui
import subprocess

##################### LOGIC ############################
async def browse_source_directory(ui: ui.UI, state: state.AppState):
    """Open a dialog to select a directory"""
    print("Browse source directory selected") # Testing
    state.source_directory_path = await ft.FilePicker().get_directory_path() or state.source_directory_path
    print(f"Source directory set to {state.source_directory_path}")
    # Update the source directory text
    ui.source_directory_path.value = state.source_directory_path
    ui.source_directory_path.update()
    load_media_files(ui, state)
    # toggle the commit button if a directory is chosen for source and destination
    toggle_commit_button()

async def browse_destination_directory(ui: ui.UI, state: state.AppState):
    """Open a dialog to select a directory"""
    print("Browse destination directory selected") # testing
    state.destination_directory_path = await ft.FilePicker().get_directory_path() or state.destination_directory_path
    print(f"Destination directory set to {state.destination_directory_path}")
    # Update the destination directory text in UI
    ui.destination_directory_path.value = state.destination_directory_path
    ui.destination_directory_path.update()
    # toggle the commit button if a directory is chosen for source and destination
    toggle_commit_button()

def select_source_file(index: int, ui: ui.UI, state: state.AppState):
        # update the selected file index
        state.selected_file_index = index

        # reload the files to update highlights
        load_media_files(ui, state)

        # Fill the text fields in selected file info
        ui.fill_selected_file_fields(
            state.media_files[index]["name"],
            state.media_files[index]["year"],
            state.media_files[index]["tv_movie"],
            state.media_files[index]["season"],
            state.media_files[index]["episode"]
        )

def toggle_commit_button():
        print("Commit button pressed")

def load_media_files(ui: ui.UI, state: state.AppState):
    """Attempt to load the media files from directory"""
    # If a directory is chosen
    if state.source_directory_path != "No path selected":
        # Reset media files
        state.media_files.clear()
        ui.file_list.controls.clear()

        # Find each file in the chosen directory that has the correct filetype and add to media files 
        for file in os.listdir(state.source_directory_path):
                if file.lower().endswith((".mp4", ".mkv", ".avi", ".mov", ".mp3", ".flac")):
                    state.media_files.append({"name": file, "tv_movie": False, "new_name": "", "year": "", "season": "", "episode": ""})

        # Cycle through each item in the files and add the name to the list
        for index, item in enumerate(state.media_files):
            tile = ft.ListTile(
                    title=ft.Text(item["name"]),
                    on_click=ui.on_click_source_file_tile,
                    data=index,
                    selected_color=ft.Colors.BLUE_500
            )
            if index == state.selected_file_index:
                tile.selected = True
            else:
                tile.selected = False
            ui.file_list.controls.append(tile)
            
            #Update the file list
            ui.file_list.update()

def play_media_file(state: state.AppState):
        """Attempt to play the media file"""
        try:
            index = state.selected_file_index
            file = state.media_files[index]["name"]
            filepath = os.path.join(state.source_directory_path, file)
            print(f"Filepath created: {filepath}")
            # Determine OS, nt for windows, posix for mac/linux
            if os.name == "nt":
                print("OS set to nt")
                os.startfile(filepath)
            elif os.name == "posix":
                print("OS set to posix")
                subprocess.run(["open", filepath])
        except:
            print("Unable to play media")