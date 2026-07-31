import flet as ft
import state
import os
import ui
import subprocess
from constants import Keys, MediaType
import shutil
from mediafile import MediaFile
from enum import Enum

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
        fill_selected_file_fields(
            ui,
            state.media_files[index].file_name if staged == False else state.media_files[index].new_name or "",
            state.media_files[index].year or "",
            state.media_files[index].type or MediaType.MOVIE,
            state.media_files[index].season or "",
            state.media_files[index].episode or "",
            state
        )

        # Toggle the commit button
        toggle_commit_button(ui, state)

        # Change name of stage file
        update_stage_button(ui, state)

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
                if file.lower().endswith((".mp4", ".mkv", ".avi", ".mov", ".mp3", ".flac")) and not file.startswith('.'):
                    mediafile = MediaFile(file)
                    state.media_files.append(mediafile)

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
        if item.staged != True:
            tile = ft.ListTile(
                    title=ft.Text(item.file_name),
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
        if file.staged:
            state.staged_list.append(file)

    # Fill listview with items in stage list
    for index, item in enumerate(state.staged_list):
        # Construct a readable name to put in list. If TV include season and episode, if Movie, just the name
        new_name = item.new_name or ""
        season = item.season or ""
        episode = item.episode or ""
        new_name = f"[{item.type.value}] {new_name} S{season} E{episode}" if item.type == MediaType.TV else f"[{item.type.value}] {new_name}"
        tile = ft.ListTile(
            title=ft.Text(new_name),
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
                file = state.media_files[index].file_name
            else:
                 index = state.selected_file_index[Keys.INDEX]
                 file = state.staged_list[index].file_name
            
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

def update_stage_button(ui: ui.UI, state: state.AppState):
    """Toggle stage button to say Stage/Unstage based on the selected file."""
    if state.selected_file_index[Keys.STAGED]:
        ui.stage_button.content = "Unstage"
    else:
        ui.stage_button.content = "Stage"

    ui.stage_button.update()

def fill_selected_file_fields(ui: ui.UI, title: str, year: str, type: MediaType, season: str, episode: str, state: state.AppState):
    """Fill the input boxes with information obtained from the selected file."""
    if state.last_staged_was_tv:
        ui.episode_textfield.value = ""
        ui.selected_info_container.update()
    else:
        ui.title_textfield.value = title
        ui.year_textfield.value = year
        ui.tv_movie_switch.value = True if type == MediaType.MOVIE else False
        ui.season_textfield.value = season
        ui.episode_textfield.value = episode
        ui.selected_info_container.update()

def organize_files(state: state.AppState, ui: ui.UI):
     # Make sure there is a source and destination directory
    if not state.source_directory_path and not state.destination_directory_path:
        print("WARNING: No source and/or destination path selected")
        return

    # boolean used to track if all files are transferred for a later check
    all_files_transferred = True

    # For each media file
    # >> If has media type selected
    # >> If "Movie" organize as needed
    # >> If "TV" organize as needed
    # >> Provide message of completion
    # >> Reload the files

    for m in state.media_files:
        if m.type == MediaType.MOVIE and m.staged:
            file = m
            title = file.new_name or file.file_name
            year = file.year or ""

            # Record the old path to the file
            old_path = os.path.join(state.source_directory_path, file.file_name)

            # Create the new folder structure and make the directory
            folder_name = f"{title} ({year})" if year else title
            dest_dir = os.path.join(state.destination_directory_path, folder_name)
            os.makedirs(dest_dir, exist_ok=True)

            # Move the file
            ext = os.path.splitext(file.file_name)[1]
            new_path = os.path.join(dest_dir, f"{folder_name}{ext}")

            # Check if path exists, if it does skip moving file, if not then move file
            if os.path.exists(new_path):
                all_files_transferred = False
            else:
                shutil.move(old_path, new_path)

        elif m.type == MediaType.TV and m.staged:
            file = m
            title = file.new_name or file.file_name
            year = file.year or ""
            season = file.season or ""
            episode = file.episode or ""

            # Record the old path to the file
            old_path = os.path.join(state.source_directory_path, file.file_name)

            # Create the new folder structure and make the directory
            dest_dir = os.path.join(state.destination_directory_path, f"{title} ({year})", f"Season {season.zfill(2)}")
            os.makedirs(dest_dir, exist_ok=True)

            # Move the file
            ext = os.path.splitext(file.file_name)[1]
            new_name = f"{title} ({year}) - S{season.zfill(2)}E{episode.zfill(2)}{ext}"
            new_path = os.path.join(dest_dir, new_name)

            # Check if path exists, if it does skip moving file, if not then move file
            if os.path.exists(new_path):
                all_files_transferred = False
            else:
                shutil.move(old_path, new_path)

        else:
            pass

    # Display completion message, if all files are transferred confirm, otherwise inform some were not
    if all_files_transferred:
        ui.show_popup("All files moved to destination!")
        load_media_files(ui, state)
    else:
        ui.show_popup("Some files skipped for names already existing.")
        update_staged_files(ui, state)
        update_source_file_list(ui, state)

def stage_file(state: state.AppState, ui: ui.UI):
    # Get a ref to the selected index
    index = state.selected_file_index[Keys.INDEX]

    # Check to make sure nothing using new name already
    for file in state.media_files:
        if file.staged and file.new_name == ui.title_textfield.value:
            print(f"File already exists by that name!")
            ui.show_popup("File already exists by that name!")
            return

    # If a staged file is selected, unstage the file and reload
    if state.media_files[index].staged:
        state.media_files[index].staged = False
    # If not a staged file, then stage the file based on if movie or tv
    elif ui.tv_movie_switch.value: # If True, is Movie, otherwise is TV
        # Stage movie file
        state.media_files[index].new_name = ui.title_textfield.value
        state.media_files[index].year = ui.year_textfield.value

        # Set the media type
        state.media_files[index].type = MediaType.MOVIE

        # Set the stage value to True
        state.media_files[index].staged = True

        # Set value for last staged file is TV to False
        state.last_staged_was_tv = False

        print(f"New movie staged: {state.media_files[index]}")
    else:
        # Stage TV file
        state.media_files[index].new_name = ui.title_textfield.value
        state.media_files[index].year = ui.year_textfield.value
        state.media_files[index].season = ui.season_textfield.value
        state.media_files[index].episode = ui.season_textfield.value

        # Set the media type
        state.media_files[index].type = MediaType.TV

        # Set the stage value to true
        state.media_files[index].staged = True

        # Set value for last staged file is tv to true
        state.last_staged_was_tv = True

        print(f"New TV show staged: {state.media_files[index]}")

    # Update the stage list view
    update_staged_files(ui, state)

    # Update the source list view
    update_source_file_list(ui, state)