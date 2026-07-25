import flet as ft
import state
import os
import ui
import subprocess
from constants import Keys

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
    toggle_commit_button(ui, state)

async def browse_destination_directory(ui: ui.UI, state: state.AppState):
    """Open a dialog to select a directory"""
    print("Browse destination directory selected") # testing
    state.destination_directory_path = await ft.FilePicker().get_directory_path() or state.destination_directory_path
    print(f"Destination directory set to {state.destination_directory_path}")
    # Update the destination directory text in UI
    ui.destination_directory_path.value = state.destination_directory_path
    ui.destination_directory_path.update()
    # toggle the commit button if a directory is chosen for source and destination
    toggle_commit_button(ui, state)

def select_file(index: int, ui: ui.UI, state: state.AppState, staged: bool):
        """Sets the selected file index, updates the source file list, populates the selected file fields."""
        # update the selected file index
        state.selected_file_index[Keys.INDEX] = index
        state.selected_file_index[Keys.STAGED] = staged

        # reload the files to update highlights
        update_source_file_list(ui, state)
        update_staged_files(ui, state)

        # Fill the text fields in selected file info
        ui.fill_selected_file_fields(
            state.media_files[index][Keys.NAME] if staged == False else state.media_files[index]["new_name"],
            state.media_files[index][Keys.YEAR],
            state.media_files[index]["type"],
            state.media_files[index][Keys.SEASON],
            state.media_files[index][Keys.EPISODE]
        )

        # Toggle the commit button
        toggle_commit_button(ui, state)

        # Change name of stage file
        # if list_type == "source":
        #     ui.stage_button.content = "Stage"
        # elif list_type == "staged":
        #     ui.stage_button.content = "Unstage"

def toggle_commit_button(ui: ui.UI, state: state.AppState):
        """Enable/Disable the commit button based on if there are files ready to be commited, there is a source and a destination directory."""
        if state.source_directory_path != "" and state.destination_directory_path != "" and len(state.staged_list) > 0:
            ui.commit_button.disabled = False
        else:
            ui.commit_button.disabled = True

        ui.commit_button.update()

def load_media_files(ui: ui.UI, state: state.AppState):
    """Attempt to load the media files from directory"""
    # If a directory is chosen
    if state.source_directory_path != "No path selected":
        # Reset media files and staged files
        state.media_files.clear()
        state.staged_list.clear()
        ui.file_list.controls.clear()
        ui.stage_list.controls.clear()


        # Find each file in the chosen directory that has the correct filetype and add to media files 
        for file in os.listdir(state.source_directory_path):
                if file.lower().endswith((".mp4", ".mkv", ".avi", ".mov", ".mp3", ".flac")):
                    state.media_files.append({Keys.NAME: file, "type": "", "new_name": "", Keys.YEAR: "", Keys.SEASON: "", Keys.EPISODE: "", "staged": False})

        # Update the source file list
        update_source_file_list(ui, state)
            
        # Update the staged file list
        update_staged_files(ui, state)

def update_source_file_list(ui: ui.UI, state: state.AppState):
    """Update the source file list without loading the files from disk again and updates the file list ui element."""
     # clear the listview
    ui.file_list.controls.clear()

    #cycle through files in media files and add to list, only add files that have not been staged
    for index, item in enumerate(state.media_files):
        if item["staged"] != True:
            tile = ft.ListTile(
                    title=ft.Text(item[Keys.NAME]),
                    on_click=ui.on_click_source_file_tile,
                    data=index,
                    selected_color=ft.Colors.BLUE_500
            )
            if index == state.selected_file_index[Keys.INDEX] and state.selected_file_index[Keys.STAGED] == False:
                tile.selected = True
            else:
                tile.selected = False
            ui.file_list.controls.append(tile)

    # update the list
    ui.file_list.update()

def update_staged_files(ui: ui.UI, state: state.AppState):
    """Update the staged file list and listview UI element."""
    # Clear the list and the listview
    state.staged_list.clear()
    ui.stage_list.controls.clear()

    # Fill list with files that have been staged
    for file in state.media_files:
        if file["staged"]:
            state.staged_list.append(file)

    # Fill listview with items in stage list
    for index, item in enumerate(state.staged_list):
        tile = ft.ListTile(
            title=ft.Text(item["new_name"]),
            on_click=ui.on_click_staged_file_tile,
            data=index,
            selected_color=ft.Colors.BLUE_500
        )

        # If the current selected file is a staged file then highlight the file
        if index == state.selected_file_index[Keys.INDEX] and state.selected_file_index[Keys.STAGED] == True:
            tile.selected = True
        else:
            tile.selected = False
            
        # Add tile to the stage list
        ui.stage_list.controls.append(tile)

    # Update the stage list
    ui.stage_list.update()
     

def play_media_file(state: state.AppState):
        """Attempt to play the media file"""
        try:
            if state.selected_file_index[Keys.STAGED] == False:
                index = state.selected_file_index[Keys.INDEX]
                file = state.media_files[index][Keys.NAME]
            else:
                 index = state.selected_file_index[Keys.INDEX]
                 file = state.staged_list[index][Keys.NAME]
            
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