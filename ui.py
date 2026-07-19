import flet as ft
import logic

class UI:
    def __init__(self, page: ft.Page, logic: logic.Logic):
        self.page = page
        self.logic = logic
    
        ########################## Buttons ############################
        self.source_button = ft.Button(
            content="Browse",
            on_click=self.browse_source_directory_clicked
        )
        self.destination_button = ft.Button(
            content="Browse",
            on_click=self.browse_destination_directory_clicked
        )
        self.play_button = ft.Button(
            content="Play",
            #on_click=play_media_file
        )
        self.stage_button = ft.Button(
            content="Stage",
            #on_click=stage_file
        )
        self.commit_button = ft.Button(
            content="Commit",
            #on_click=commit_files,
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
                ft.Text(f"Item {i}") for i in range(1, 100) # For testing
            ],
            expand=True
        )

        ######################### Switches ##########################
        self.tv_movie_switch = ft.Switch(
            label="TV/Movie", 
            value=False,
            #on_change=update_on_tv_movie_switch
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

    async def browse_source_directory_clicked(self, e):
        print("Browse source directory clicked")
        await self.logic.browse_source_directory(self)

    async def browse_destination_directory_clicked(self):
        print("Browse destination directory clicked")
        await self.logic.browse_destination_directory(self)

    def on_source_file_clicked(self, e: ft.Event[ft.ListTile]):
        print("Source file clicked at index:", e.control.data)
        self.logic.select_source_file(e.control.data, self)

    def fill_selected_file_fields(self, title: str, year: str, tv_movie: bool, season: str, episode: str):
        self.title_textfield.value = title
        self.year_textfield.value = year
        self.tv_movie_switch.value = tv_movie
        self.season_textfield.value = season
        self.episode_textfield.value = episode
        self.selected_info_container.update()
    
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