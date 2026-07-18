import flet as ft
import os
from state import AppState
import subprocess

def main(page: ft.Page):

    state = AppState()

    ##################### LOGIC ############################
    async def browse_source_directory(e: ft.Event[ft.Button]):
        """Open a dialog to select a directory"""
        print("Browse source directory selected") # Testing
        state.source_directory_path.value = await ft.FilePicker().get_directory_path() or state.source_directory_path.value
        print(f"Source directory set to {state.source_directory_path.value}")
        state.source_directory_path.update()
        load_media_files()
        # toggle the commit button if a directory is chosen for source and destination
        toggle_commit_button()

    async def browse_destination_directory():
        """Open a dialog to select a directory"""
        print("Browse destination directory selected") # testing
        state.destination_directory_path.value = await ft.FilePicker().get_directory_path() or state.destination_directory_path.value
        print(f"Destination directory set to {state.destination_directory_path.value}")
        state.destination_directory_path.update()
        # toggle the commit button if a directory is chosen for source and destination
        toggle_commit_button()

    def stage_file():
        """Stage selected file for naming."""
        print("Stage file selected")

    def commit_files():
        """Commit the staged files, completing change"""
        print("Commit files selected")

    def source_file_clicked(e: ft.Event[ft.ListTile]):
        index = e.control.data
        print(f"source file clicked at index {index}")
        # update the selected file index
        state.selected_file_index = index

        # reload the files to update highlights
        load_media_files()

        # Fill the text fields in selected file info
        fill_selected_file_fields(
            state.media_files[index]["name"],
            state.media_files[index]["year"],
            state.media_files[index]["tv_movie"],
            state.media_files[index]["season"],
            state.media_files[index]["episode"]
        )

    def fill_selected_file_fields(title: str, year: str, tv_movie: bool, season: str, episode: str):
        title_textfield.value = title
        year_textfield.value = year
        tv_movie_switch.value = tv_movie
        season_textfield.value = season
        episode_textfield.value = episode
        selected_info_container.update()

    def toggle_commit_button():
          if state.source_directory_path.value != "No path selected" and state.destination_directory_path.value != "No path selected":
                print("Commit button activated")
                commit_button.disabled = False
                commit_button.update()

    def load_media_files():
        """Attempt to load the media files from directory"""
        # If a directory is chosen
        if state.source_directory_path.value != "No path selected":
            # Reset media files
            state.media_files.clear()
            file_list.controls.clear()

            # Find each file in the chosen directory that has the correct filetype and add to media files 
            for file in os.listdir(state.source_directory_path.value):
                    if file.lower().endswith((".mp4", ".mkv", ".avi", ".mov", ".mp3", ".flac")):
                        state.media_files.append({"name": file, "tv_movie": False, "new_name": "", "year": "", "season": "", "episode": ""})

            # Cycle through each item in the files and add the name to the list
            for index, item in enumerate(state.media_files):
                tile = ft.ListTile(
                        title=ft.Text(item["name"]),
                        on_click=source_file_clicked,
                        data=index,
                        selected_color=ft.Colors.BLUE_500
                )
                if index == state.selected_file_index:
                    tile.selected = True
                else:
                    tile.selected = False
                file_list.controls.append(tile)
                
                #Update the file list
                file_list.update()

    def play_media_file():
        """Attempt to play the media file"""
        try:
            index = state.selected_file_index
            file = state.media_files[index]["name"]
            filepath = os.path.join(state.source_directory_path.value, file)
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

    def update_on_tv_movie_switch():
        """Update the text boxes upon switch change"""
        season_textfield.disabled = tv_movie_switch.value
        episode_textfield.disabled = tv_movie_switch.value
        print(f"Season textfield disabled set to: {season_textfield.disabled}")
        print(f"Episode textfield disabled set to: {episode_textfield.disabled}")
        season_textfield.update()
        episode_textfield.update()
    
            


    ########################## Buttons ############################
    source_button = ft.Button(
        content="Browse",
        on_click=browse_source_directory
    )
    destination_button = ft.Button(
        content="Browse",
        on_click=browse_destination_directory
    )
    play_button = ft.Button(
        content="Play",
        on_click=play_media_file
    )
    stage_button = ft.Button(
        content="Stage",
        on_click=stage_file
    )
    commit_button = ft.Button(
        content="Commit",
        on_click=commit_files,
        disabled=True
    )

    ######################## Lists #############################
    file_list = ft.ListView(
        controls=[
            #ft.Text(f"Item {i}") for i in range(1, 100) # For testing
        ],
        expand=True
    )
    stage_list = ft.ListView(
        controls=[
            ft.Text(f"Item {i}") for i in range(1, 100) # For testing
        ],
        expand=True
    )

    ######################### Switches ##########################
    tv_movie_switch = ft.Switch(
        label="TV/Movie", 
        value=False,
        on_change=update_on_tv_movie_switch
    )

    ##################### Text Fields ###########################
    title_textfield = ft.TextField(
        label="Title"
    )
    year_textfield = ft.TextField(
        label="Year"
    )
    season_textfield = ft.TextField(
        label="Season",
        col=6,
        disabled=tv_movie_switch.value
    )
    episode_textfield = ft.TextField(
        label="Episode",
        col=6,
        disabled=tv_movie_switch.value
    )

    ########################## Top row container ########################
    top_container = ft.Container(
        content=ft.Row(
            [
                source_button,
                state.source_directory_path
            ]
        ),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        padding=20,
        border_radius=10,
        col=12
    )

    ######################## Middle row containers #########################
    file_list_container = ft.Container(
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        padding=20,
        border_radius=10,
        col=4,
        content=ft.Column(
            [
                file_list
            ]
        )
    )
    selected_info_container = ft.Container(
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        padding=20,
        border_radius=10,
        col=4,
        content=ft.Column(
            [
                ft.Text("Media Info"),
                title_textfield,
                year_textfield,
                tv_movie_switch,
                ft.ResponsiveRow(
                    [
                        season_textfield,
                        episode_textfield
                    ]
                ),
                ft.Container(expand=True), # Push buttons to bottom
                ft.Row(
                    [
                        play_button,
                        stage_button
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ]
        )
    )
    stage_list_container = ft.Container(
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        padding=20,
        border_radius=10,
        col=4,
        content=ft.Column(
            [
                stage_list
            ]
        )
    )

    ######################### Bottom row container #########################
    bottom_container = ft.Container(
        content=ft.Row(
            [
                destination_button,
                state.destination_directory_path,
                ft.Container(expand=True), # Add space between
                commit_button
            ]
        ),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        padding=20,
        border_radius=10,
        col=12
    )

    
    
    ########################### Add items to page #############################
    page.add(
        ft.Column(
            [
                # Top Row
                ft.ResponsiveRow(
                    [
                        top_container
                    ]
                ),

                # Middle Row
                ft.ResponsiveRow(
                    [
                        file_list_container,
                        selected_info_container,
                        stage_list_container
                    ],
                    expand=True
                ),

                # Bottom Row     
                ft.ResponsiveRow(
                    [
                        bottom_container
                    ]
                )   
            ],
            spacing=10,
            expand=True
        )
        
    )

    
##################### Run file ######################
if __name__ == "__main__":
    ft.run(main)