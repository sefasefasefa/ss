from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView


class ResponsiveForm(AnchorLayout):
    def __init__(self, content, max_width=560, **kwargs):
        super().__init__(anchor_x='center', anchor_y='center', **kwargs)
        content.size_hint_x = None
        self.scroll = ScrollView(
            size_hint=(None, 0.92),
            do_scroll_x=False,
            bar_width=dp(4)
        )
        self.content = content
        self.scroll.add_widget(content)
        self.add_widget(self.scroll)
        self.max_width = dp(max_width)
        self.bind(size=self._update_width)
        self._update_width(self, self.size)

    def _update_width(self, instance, size):
        width = max(dp(1), min(self.max_width, size[0] - dp(32)))
        self.scroll.width = width
        self.content.width = width
