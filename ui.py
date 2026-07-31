import flet as ft
import logic
import state
from constants import Keys, MediaType

class UI:
    def __init__(self, page: ft.Page, state: state.AppState):
        self.page = page
        self.state = state
    
        ########################## Buttons ############################
        self.source_button = ft.Button(
            content="Browse",
            on_click=self.on_click_browse_source_file
        )
        self.destination_button = ft.Button(
            content="Browse",
            on_click=self.on_click_browse_destination_file
        )
        self.play_button = ft.Button(
            content="Play",
            on_click=self.on_click_play
        )
        self.stage_button = ft.Button(
            content="Stage",
            on_click=self.on_click_stage_file
        )
        self.commit_button = ft.Button(
            content="Commit",
            on_click=self.on_click_commit,
            disabled=True
        )

        ######################## Lists #############################
        self.file_list = ft.ListView(
            controls=[
                #ft.Text(f"Item {i}") for i in range(1, 100) # For testing
            ],
            expand=True
        )
        self.stage_list = ft.ListView(
            controls=[
                #ft.Text(f"Item {i}") for i in range(1, 100) # For testing
            ],
            expand=True
        )

        ######################### Switches ##########################
        self.tv_movie_switch = ft.Switch(
            label="TV Show/Movie", 
            value=False,
            on_change=self.on_click_tv_movie_switch
        )

        ##################### Text Fields ###########################
        self.title_textfield = ft.TextField(
            label="Title"
        )
        self.year_textfield = ft.TextField(
            label="Year"
        )
        self.season_textfield = ft.TextField(
            label="Season",
            col=6,
            #disabled=tv_movie_switch.value
        )
        self.episode_textfield = ft.TextField(
            label="Episode",
            col=6,
            #disabled=tv_movie_switch.value
        )

        ########################## Texts ##############################
        self.source_directory_path = ft.Text(
            "None Selected"
        )
        self.destination_directory_path = ft.Text(
            "None Selected"
        )

        ########################## Top row container ########################
        self.top_container = ft.Container(
            content=ft.Row(
                [
                    self.source_button,
                    self.source_directory_path
                ]
            ),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            padding=20,
            border_radius=10,
            col=12
        )

        ######################## Middle row containers #########################
        self.file_list_container = ft.Container(
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            padding=20,
            border_radius=10,
            col=4,
            content=ft.Column(
                [
                    self.file_list
                ]
            )
        )
        self.selected_info_container = ft.Container(
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            padding=20,
            border_radius=10,
            col=4,
            content=ft.Column(
                [
                    ft.Text("Media Info"),
                    self.title_textfield,
                    self.year_textfield,
                    self.tv_movie_switch,
                    ft.ResponsiveRow(
                        [
                            self.season_textfield,
                            self.episode_textfield
                        ]
                    ),
                    ft.Container(expand=True), # Push buttons to bottom
                    ft.Row(
                        [
                            self.play_button,
                            self.stage_button
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ]
            )
        )
        self.stage_list_container = ft.Container(
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            padding=20,
            border_radius=10,
            col=4,
            content=ft.Column(
                [
                    self.stage_list
                ]
            )
        )

        ######################### Bottom row container #########################
        self.bottom_container = ft.Container(
            content=ft.Row(
                [
                    self.destination_button,
                    self.destination_directory_path,
                    ft.Container(expand=True), # Add space between
                    self.commit_button
                ]
            ),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            padding=20,
            border_radius=10,
            col=12
        )


    ####################### On Click Actions ###############################
    async def on_click_browse_source_file(self, e):
        print("Browse source directory clicked")
        await logic.browse_source_directory(self, self.state)

    async def on_click_browse_destination_file(self):
        print("Browse destination directory clicked")
        await logic.browse_destination_directory(self, self.state)

    def on_click_source_file_tile(self, e: ft.Event[ft.ListTile]):
        print("Source file clicked at index:", e.control.data)
        logic.select_file(e.control.data, self, self.state, staged=False)

    def on_click_staged_file_tile(self, e: ft.Event[ft.ListTile]):
        print("Staged file tile clicked at index:", e.control.data)
        logic.select_file(e.control.data, self, self.state, staged=True)

    def on_click_commit(self):
        print("commit clicked")
        logic.organize_files(self.state, self)

    def on_click_play(self):
        print("play button clicked")
        logic.play_media_file(self.state)

    def on_click_tv_movie_switch(self):
        """Update the text boxes upon switch change"""
        self.season_textfield.disabled = self.tv_movie_switch.value
        self.episode_textfield.disabled = self.tv_movie_switch.value
        print(f"Season/Episode textfields set to: {self.season_textfield.disabled}")
        self.season_textfield.update()
        self.episode_textfield.update()

    def on_click_stage_file(self):
        """Stage selected file for naming."""
        logic.stage_file(self.state, self)

    def show_popup(self, error: str):
        """Generate a popup using a text string for the message."""
        def on_click_close(e):
            popup.open = False
            self.page.update()

        popup = ft.AlertDialog(
            title="Error",
            content=ft.Text(error),
            actions=[ft.TextButton("Ok", on_click=on_click_close)]
        )

        self.page.show_dialog(popup)
    
    ########################### Add items to page #############################
    def build_page(self):
        self.page.add(
            ft.Column(
                [
                    # Top Row
                    ft.ResponsiveRow(
                        [
                            self.top_container
                        ]
                    ),

                    # Middle Row
                    ft.ResponsiveRow(
                        [
                            self.file_list_container,
                            self.selected_info_container,
                            self.stage_list_container
                        ],
                        expand=True
                    ),

                    # Bottom Row     
                    ft.ResponsiveRow(
                        [
                            self.bottom_container
                        ]
                    )   
                ],
                spacing=10,
                expand=True
            )
            
        )