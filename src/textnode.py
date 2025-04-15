from enum import Enum

class TextType(Enum):
    NORMAL_TEXT = "normal text"
    BOLD_TEXT = "bold text"
    ITALIC_TEXT = "italic text"
    CODE_TEXT = "code text"
    LINK_TEXT = "link text"
    IMAGE_TEXT = "image text"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        if not isinstance(text_type, TextType):
            raise TypeError(f"text_type must be an instance of {TextType.__name__}")
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(self, type(other)):
            return False
        
        dict_self = vars(self)
        dict_other = vars(other)

        if dict_self.keys() != dict_other.keys():
            return False

        for key in dict_self:
            if dict_self[key] != dict_other[key]:
                return False
        
        return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


