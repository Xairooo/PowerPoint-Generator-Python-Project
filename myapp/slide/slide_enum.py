from enum import IntEnum

class SlideLayout(IntEnum):
    TITLE = 0                 # Title Slide
    TITLE_AND_CONTENT = 1     # Title and Content
    SECTION_HEADER = 2        # Section Header
    TWO_CONTENT = 3           # Two Content
    COMPARISON = 4            # Comparison
    TITLE_ONLY = 5            # Title Only
    BLANK = 6                 # Blank
    CONTENT_WITH_CAPTION = 7  # Content with Caption
    PICTURE_WITH_CAPTION = 8  # Picture with Caption
    TITLE_AND_VERTICAL_TEXT = 9
    VERTICAL_TITLE_AND_TEXT = 10