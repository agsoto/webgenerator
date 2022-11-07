import enum
class ContentType(enum.Enum):
    def __str__(self):
        return str(self.value)

    List = "list"
    OnlyText = "text"
    HeadingDescription = "heading_description"
    Multi = "multi"
    Dictionary = "dictionary"

class MeasureUnit(enum.Enum):
    def __str__(self):
        return str(self.value)

    Px = "px"
    Percentage = "%"
    Viewport = "v"
    Rem = "rem"
    Em = "em"
