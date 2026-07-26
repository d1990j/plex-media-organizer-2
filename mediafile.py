from constants import MediaType

class MediaFile:
    def __init__(self, file_name: str, new_name: str | None = None, year: str | None = None, season: str | None = None, episode: str | None = None, type: MediaType = MediaType.MOVIE):
        self.new_name = new_name
        self.year = year
        self.season = season
        self.episode = episode
        self.file_name = file_name
        self.type = type
        self.staged = False

    def get_plex_folder_series_name(self) -> str:
        """Return the name of the file folder for the series using the Plex naming convention."""
        plex_name = f"{self.new_name} ({self.year})" if self.year else f"{self.new_name}"
        return plex_name

    def get_plex_folder_season_name(self) -> str:
        """Return the name of the file folder for the season using the Plex naming convention."""
        if self.season:
            plex_name = f"Season {self.season.zfill(2)}"
        else:
            print(f"ERROR: No season selected for {self.file_name}, using 0.")
            plex_name = "0"
        return plex_name

    def get_plex_name(self) -> str:
        """Return the name of the file using the Plex naming convention."""
        if self.type == MediaType.TV:
            if self.season and self.episode and self.year:
                plex_name = f"{self.new_name} ({self.year}) - S{self.season.zfill(2)}E{self.episode.zfill(2)}"
            else:
                plex_name = f"{self.new_name}"
            return plex_name
        else:
            if self.year:
                plex_name = f"{self.new_name} ({self.year})"
            else:
                plex_name = f"{self.new_name}"
            return plex_name