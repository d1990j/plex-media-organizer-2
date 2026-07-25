from enum import Enum

class Keys(Enum):
    NAME = "name"
    YEAR = "year"
    SEASON = "season"
    EPISODE = "episode"
    STAGED = "staged"
    INDEX = "index"
    TYPE = "type"
    NEW_NAME = "new_name"

class MediaType(Enum):
    MOVIE = "movie"
    TV = "tv"