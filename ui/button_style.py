from kivy.uix.button import Button as KivyButton

from auth_settings import BUTTON_STYLE, BUTTON_STYLE_ENABLED


def _hex_color(value):
    value = value.lstrip('#')
    return tuple(int(value[index:index + 2], 16) / 255 for index in (0, 2, 4)) + (1,)


class StyledButton(KivyButton):
    def __init__(self, *args, **kwargs):
        styleable = False
        style_dimensions = kwargs.pop('style_dimensions', True)
        if BUTTON_STYLE_ENABLED:
            background = kwargs.get('background_color', (1, 1, 1, 1))
            if len(background) > 3 and background[3] >= 0.95:
                styleable = True
                kwargs['background_normal'] = ''
                kwargs['background_color'] = _hex_color(BUTTON_STYLE['color'])
                kwargs['color'] = _hex_color(BUTTON_STYLE['text_color'])
                kwargs['background_down'] = ''
            if style_dimensions:
                width_factor = BUTTON_STYLE['width'] / 120
                height_factor = BUTTON_STYLE['height'] / 40
                if 'size' in kwargs:
                    width, height = kwargs['size']
                    kwargs['size'] = (width * width_factor, height * height_factor)
                else:
                    if kwargs.get('width') is not None:
                        kwargs['width'] *= width_factor
                    if kwargs.get('height') is not None:
                        kwargs['height'] *= height_factor
        super().__init__(*args, **kwargs)
        if styleable:
            self.bind(
                state=lambda button, state: setattr(
                    button,
                    'background_color',
                    _hex_color(
                        BUTTON_STYLE['hover_color']
                        if state == 'down'
                        else BUTTON_STYLE['color']
                    )
                )
            )
