import enum
class ContentType(enum.Enum):
    List = "list"
    OnlyText = "text"
    HeadingDescription = "heading_description"
    Multi = "multi"
    Dictionary = "dictionary"

class MeasureUnit(enum.OrderedDict):
    Px = "px"
    Percentage = "%"
    Viewport = "v"
    Rem = "rem"
    Em = "em"
