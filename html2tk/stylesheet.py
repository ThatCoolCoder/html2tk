import tinycss2

from .style import Style

class Stylesheet:
    BASE_STYLE_LOOKUP = {
        'paragraph' : 'TLabel',
        'heading1' : 'TLabel',
        'heading2' : 'TLabel',
        'button' : 'TButton',
        'input' : 'TEntry',
        'checkbox_input' : 'TCheckbutton',
        'div' : 'TFrame'
    }

    DEFAULT_STYLES = {
        'paragraph' : Style(BASE_STYLE_LOOKUP['paragraph'],
            font='helvetica',
            font_size=12,
            color='black',
            background_color='grey90'),
        'heading1' : Style(BASE_STYLE_LOOKUP['heading1'],
            font='helvetica',
            font_size=24,
            color='black',
            background_color='grey90'),
        'heading2' : Style(BASE_STYLE_LOOKUP['heading2'],
            font='helvetica',
            font_size=18,
            color='black',
            background_color='grey90'),
        'button' : Style(BASE_STYLE_LOOKUP['button'],
            font='helvetica',
            font_size=12,
            color='black'),
        'input' : Style(BASE_STYLE_LOOKUP['input'],
            font='helvetica',
            font_size=12,
            color='black',
            background_color='white'),
        'checkbox_input' : Style(BASE_STYLE_LOOKUP['checkbox_input'],
            color='black',
            background_color='grey90'),
        'div' : Style(BASE_STYLE_LOOKUP['div'],
            background_color='grey90')
    }

    CSS_ATTRIBUTE_TO_PYTHON = {
        'color' : 'color',
        'background-color' : 'background_color',
        'font-size' : 'font_size',
        'font' : 'font'
    }

    def __init__(self, css_file_name: str = '', css: str = '',
        style_dict: dict = {}):
        
        self.clear_styles()

        if css_file_name != '':
            self.load_css_file(css_file_name)
        elif css != '':
            self.load_css(css)
        elif len(style_dict) > 0:
            self.load_style_dict(style_dict)
        
        self.init_default_styles()
    
    def clear_styles(self):
        '''Remove all styles allocated using __init__,
        load_css_file, load_css and load_style_dict.
        Does not delete styles - only removes them from this sheet.
        Does not remove default styles.
        '''
        self.styles = {} # remove everything
        self.init_default_styles() # restore defaults

    def init_default_styles(self):
        '''Set styles for the basic elements
        if the user hasn't specified them.
        '''
        for style_name in self.DEFAULT_STYLES:
            if style_name not in self.styles:
                self.styles[style_name] = self.DEFAULT_STYLES[style_name]
    
    def load_css_file(self, css_file_name: str):
        '''Read css from a file and parse it,
        then use the css to create styles for this sheet
        '''
        file = None
        try:
            file = open(css_file_name, 'r', encoding='utf-8')
            css = file.read()
            self.load_css(css)
        finally:
            file.close()

    def load_css(self, css: str):
        '''Parse css and use it to create styles for this sheet'''
        css_rules = tinycss2.parse_stylesheet(css, skip_comments=True,
            skip_whitespace=True)
        for rule in css_rules:
            class_name = rule.prelude[0].value
            declaration_list = tinycss2.parse_declaration_list(rule.content)
            print(declaration_list)
            # I don't know how to do dict comprehension so use a loop
            attributes = {}
            for declaration in declaration_list:
                if type(declaration) != tinycss2.ast.Declaration:
                    continue
                attribute_name = self.CSS_ATTRIBUTE_TO_PYTHON[
                    declaration.lower_name]

                value = None
                for token in declaration.value:
                    if type(token) != tinycss2.ast.WhitespaceToken:
                        value = token.value

                if value is not None:
                    attributes[attribute_name] = value

            base_style_name = self.BASE_STYLE_LOOKUP[class_name] 
            self.styles[class_name] = Style(base_style_name, **attributes)

    def load_style_dict(self, style_dict: dict):
        '''Load a dict of styles where the key is the element type
        and the value is the style.
        Note that this copies the styles from the dict
        and does not create pointers
        '''
        for style_name in style_dict:
            self.styles[style_name] = style_dict[style_name].copy()

    def __getitem__(self, item):
        '''Get the style named item.
        If the style doesn't exist, return a fallback style.
        Warning: do not call this before instantiating a Tk window,
        or an extra one will be made due to Tk weirdness.
        '''
        style = self.styles.get(item, self.styles['paragraph'])
        if not style.fully_initiated:
            style.init()
        return style