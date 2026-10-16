from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from ui.button_style import StyledButton as Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from kivy.graphics import Ellipse
from auth_settings import APP_LOGO, APP_LOGO_TEXT, APP_NAME, HOME_CONFIG, LOGIN_ENABLED, MENU_ITEMS, UI_COMPONENTS
from ui.responsive import ResponsiveForm


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "main"
        self.login_enabled = LOGIN_ENABLED
        self.current_user = {}
        self.account_button = None
        components = set(UI_COMPONENTS)
        root = BoxLayout(orientation='vertical', spacing=0)
        self.root_layout = root
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(72),
            padding=(dp(12), dp(8)),
            spacing=dp(6)
        )
        self.header = header
        self._add_surface(header, (0.07, 0.08, 0.10, 1), 0)

        if 'menu' in components:
            self.menu_button = Button(
                text='☰',
                size_hint=(None, None),
                size=(dp(44), dp(44)),
                background_normal='',
                background_color=(0.15, 0.17, 0.20, 1),
                color=(0.9, 0.92, 0.94, 1),
                font_size=sp(22)
            )
            self.menu_button.bind(on_release=self.show_menu)
            header.add_widget(self.menu_button)

        if 'logo' in components:
            brand = BoxLayout(orientation='horizontal', size_hint=(None, 1), width=dp(126), spacing=dp(8))
            self.brand = brand
            if APP_LOGO:
                mark = Image(
                    source=APP_LOGO,
                    size_hint=(None, None),
                    size=(dp(34), dp(34)),
                    allow_stretch=True,
                    keep_ratio=True
                )
            else:
                mark = Label(
                    text=APP_LOGO_TEXT,
                    bold=True,
                    font_size=sp(20),
                    color=(0.04, 0.08, 0.06, 1),
                    size_hint=(None, None),
                    size=(dp(34), dp(34))
                )
                self._add_surface(mark, (0, 1, 0.5, 1), 12)
            brand.add_widget(mark)
            self.brand_name = Label(
                text=APP_NAME,
                bold=True,
                halign='left',
                valign='middle',
                font_size=sp(13)
            )
            self.brand_name.bind(
                size=lambda widget, size: setattr(widget, 'text_size', size)
            )
            brand.add_widget(self.brand_name)
            header.add_widget(brand)
        else:
            header.add_widget(Label(text='[b]Welcome[/b]', markup=True, halign='left', font_size=sp(18)))

        header.add_widget(Widget())

        self.login_btn = None
        if self.login_enabled:
            self.login_btn = Button(
                text='Sign in',
                size_hint=(None, None),
                size=(dp(84), dp(36)),
                background_normal='',
                background_color=(0, 1, 0.5, 1),
                color=(0.03, 0.08, 0.05, 1),
                bold=True
            )
            self.login_btn.bind(on_press=self.go_to_login)
            header.add_widget(self.login_btn)
        root.add_widget(header)

        content = BoxLayout(
            orientation='vertical',
            padding=(dp(22), dp(24)),
            spacing=dp(18),
            size_hint=(None, None)
        )
        self.main_content = content
        content.bind(minimum_height=content.setter('height'))
        hero = BoxLayout(
            orientation='vertical',
            padding=(dp(24), dp(22)),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(190)
        )
        self._add_surface(hero, (0.12, 0.15, 0.16, 1), 22)
        hero.add_widget(Label(
            text=HOME_CONFIG.get('eyebrow', 'YOUR NEXT CHAPTER'),
            font_size=sp(12),
            halign='left',
            color=(0, 1, 0.53, 1),
            size_hint_y=None,
            height=dp(22)
        ))
        hero_title = Label(
            text=HOME_CONFIG.get('title') or APP_NAME,
            bold=True,
            font_size=sp(30),
            halign='left',
            size_hint_y=None,
            height=dp(48)
        )
        self.hero_title = hero_title
        hero_title.bind(size=lambda widget, value: setattr(widget, 'text_size', (value[0], None)))
        hero.add_widget(hero_title)
        hero_description = Label(
            text=HOME_CONFIG.get(
                'description',
                'A calmer place to explore, create, and keep everything in one place.'
            ),
            font_size=sp(15),
            color=(0.72, 0.76, 0.78, 1),
            halign='left',
            valign='top'
        )
        hero_description.bind(size=lambda widget, value: setattr(widget, 'text_size', value))
        hero.add_widget(hero_description)
        content.add_widget(hero)

        if 'cards' in components:
            cards = GridLayout(cols=1, spacing=dp(12), size_hint_y=None)
            self.cards = cards
            cards.bind(minimum_height=cards.setter('height'))
            default_cards = (
                {'title': 'Discover', 'description': 'Find ideas and explore what is new.'},
                {'title': 'Make it yours', 'description': 'Your tools and preferences, all in one place.'},
                {'title': 'Stay in sync', 'description': 'Pick up where you left off whenever you return.'},
            )
            for card_config in HOME_CONFIG.get('cards', default_cards):
                heading = card_config.get('title', '').strip()
                description = card_config.get('description', '').strip()
                if not heading and not description:
                    continue
                card = BoxLayout(
                    orientation='vertical',
                    padding=(dp(18), dp(13)),
                    spacing=dp(5),
                    size_hint_y=None,
                    height=dp(88)
                )
                self._add_surface(card, (0.10, 0.11, 0.13, 1), 16)
                card.add_widget(Label(
                    text=heading,
                    bold=True,
                    font_size=sp(17),
                    halign='left',
                    size_hint_y=None,
                    height=dp(26)
                ))
                card_description = Label(
                    text=description,
                    font_size=sp(13),
                    color=(0.65, 0.69, 0.72, 1),
                    halign='left'
                )
                card_description.bind(size=lambda widget, value: setattr(widget, 'text_size', value))
                card.add_widget(card_description)
                cards.add_widget(card)
            content.add_widget(cards)

        self.scroll = ScrollView(
            size_hint=(None, 1),
            do_scroll_x=False,
            bar_width=dp(3)
        )
        self.scroll_content = AnchorLayout(
            anchor_x='center',
            anchor_y='top',
            size_hint=(None, None)
        )
        self.scroll_content.height = content.height
        content.bind(
            height=lambda widget, value: setattr(self.scroll_content, 'height', value)
        )
        self.scroll_content.add_widget(content)
        self.scroll.add_widget(self.scroll_content)
        self.scroll_container = AnchorLayout(anchor_x='center', anchor_y='top')
        self.scroll_container.add_widget(self.scroll)
        root.add_widget(self.scroll_container)

        if 'footer' in components:
            footer = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(48),
                padding=(dp(20), dp(8))
            )
            self._add_surface(footer, (0.07, 0.08, 0.10, 1), 0)
            footer.add_widget(Label(
                text=APP_NAME,
                color=(0.62, 0.66, 0.68, 1),
                font_size=sp(12),
                halign='left'
            ))
            root.add_widget(footer)
        self.add_widget(root)
        self.bind(size=self._update_responsive_layout)
        self._update_responsive_layout(self, self.size)

    def _update_responsive_layout(self, instance, size):
        width = size[0]
        content_width = max(dp(1), min(dp(960), width - dp(32)))
        self.main_content.width = content_width
        self.scroll_content.width = content_width
        self.scroll.width = content_width
        very_compact = width < dp(300)
        compact = width < dp(380)
        self.header.padding = (dp(8 if very_compact else 12), dp(8))
        self.header.spacing = dp(4 if very_compact else 6)
        if hasattr(self, 'menu_button'):
            self.menu_button.size = (
                dp(38 if very_compact else 44),
                dp(38 if very_compact else 44)
            )
        if hasattr(self, 'brand'):
            self.brand.width = min(
                dp(126),
                max(dp(72 if very_compact else 92), width * 0.34)
            )
            if hasattr(self, 'brand_name'):
                self.brand_name.width = (
                    dp(0) if very_compact else max(dp(0), self.brand.width - dp(42))
                )
                self.brand_name.size_hint_x = None
        if hasattr(self, 'cards'):
            self.cards.cols = 1 if width < dp(700) else 2
        if hasattr(self, 'hero_title'):
            self.hero_title.font_size = sp(24 if compact else 30)
            self.hero_title.height = dp(54 if compact else 48)
        for child in self.header.children:
            if isinstance(child, Button) and child.text == 'Sign in':
                child.width = dp(60 if very_compact else 70 if compact else 84)

    @staticmethod
    def _add_surface(widget, color, radius):
        with widget.canvas.before:
            Color(*color)
            widget.surface = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[dp(radius)])
        widget.bind(
            pos=lambda instance, value: setattr(instance.surface, 'pos', value),
            size=lambda instance, value: setattr(instance.surface, 'size', value)
        )

    def go_to_login(self, instance):
        self.manager.current = 'login'

    def set_authenticated(self, response=None):
        if not self.login_enabled:
            return
        user = response.get('user', response) if isinstance(response, dict) else {}
        self.current_user = user if isinstance(user, dict) else {}
        if self.login_btn is not None and self.login_btn.parent is not None:
            self.login_btn.parent.remove_widget(self.login_btn)
        if self.account_button is None:
            name = str(self.current_user.get('name') or self.current_user.get('username') or self.current_user.get('email') or 'Account')
            self.account_button = Button(
                text=name[0].upper(),
                size_hint=(None, None),
                size=(dp(42), dp(42)),
                background_normal='',
                background_color=(0, 0, 0, 0),
                color=(0.03, 0.08, 0.05, 1),
                bold=True
            )
            with self.account_button.canvas.before:
                Color(0, 1, 0.5, 1)
                self.account_button.avatar = Ellipse(
                    pos=self.account_button.pos,
                    size=self.account_button.size
                )
            self.account_button.bind(
                pos=lambda widget, value: setattr(widget.avatar, 'pos', value),
                size=lambda widget, value: setattr(widget.avatar, 'size', value),
                on_release=self.show_account_menu
            )
        if self.account_button.parent is None:
            self.header.add_widget(self.account_button)

    def show_account_menu(self, instance):
        dropdown = DropDown(
            auto_width=False,
            width=max(dp(1), min(dp(240), Window.width - dp(24))),
            max_height=max(dp(1), min(dp(140), Window.height - dp(24)))
        )
        settings = Button(
            text='Ayarlar',
            size_hint_y=None,
            height=dp(56),
            background_normal='',
            background_color=(0.12, 0.14, 0.16, 1)
        )
        settings.bind(on_release=lambda *_: dropdown.select('settings'))
        dropdown.add_widget(settings)
        sign_out = Button(
            text='Oturumu kapat',
            size_hint_y=None,
            height=dp(56),
            background_normal='',
            background_color=(0.24, 0.12, 0.13, 1)
        )
        sign_out.bind(on_release=lambda *_: dropdown.select('sign_out'))
        dropdown.add_widget(sign_out)
        dropdown.bind(on_select=self.on_account_menu_select)
        dropdown.open(self.account_button)
        self.account_dropdown = dropdown

    def on_account_menu_select(self, dropdown, selection):
        if self.manager is None:
            raise RuntimeError("Account menu requires an attached screen manager.")
        if selection == 'settings':
            self.manager.current = 'settings'
        elif selection == 'sign_out':
            self.sign_out()

    def sign_out(self):
        if self.account_button is not None and self.account_button.parent is not None:
            self.account_button.parent.remove_widget(self.account_button)
        self.account_button = None
        self.current_user = {}
        if self.login_enabled and self.login_btn is not None and self.login_btn.parent is None:
            self.header.add_widget(self.login_btn)
        if self.manager is not None:
            self.manager.current = 'login'

    def show_menu(self, instance):
        components = set(UI_COMPONENTS)
        drawer_width = max(
            dp(1),
            min(dp(320), self.width - dp(16), self.width * 0.84)
        )
        drawer_view = ModalView(
            size_hint=(1, 1),
            background='',
            background_color=(0, 0, 0, 0),
            auto_dismiss=True
        )
        overlay = FloatLayout(size_hint=(1, 1))
        backdrop = Button(
            background_normal='',
            background_color=(0, 0, 0, 0.58),
            size_hint=(1, 1)
        )
        backdrop.bind(on_release=lambda *_: drawer_view.dismiss())
        overlay.add_widget(backdrop)

        drawer = BoxLayout(
            orientation='vertical',
            size_hint=(None, 1),
            width=drawer_width,
            padding=(dp(18), dp(16)),
            spacing=dp(10),
            x=-drawer_width
        )
        self._add_surface(drawer, (0.07, 0.08, 0.10, 1), 0)
        drawer_header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(52),
            spacing=dp(8)
        )
        drawer_header.add_widget(Label(
            text=APP_NAME,
            bold=True,
            halign='left',
            valign='middle',
            font_size=sp(15)
        ))
        close_button = Button(
            text='×',
            size_hint=(None, None),
            size=(dp(42), dp(42)),
            background_normal='',
            background_color=(0.15, 0.17, 0.20, 1),
            font_size=sp(24)
        )
        close_button.bind(on_release=lambda *_: drawer_view.dismiss())
        drawer_header.add_widget(close_button)
        drawer.add_widget(drawer_header)
        drawer.add_widget(Label(
            text='Uygulama menüsü',
            size_hint_y=None,
            height=dp(28),
            halign='left',
            color=(0.62, 0.66, 0.68, 1),
            font_size=sp(12)
        ))

        selected_items = [
            item for item in MENU_ITEMS
            if self.login_enabled or item['action'] not in ('login', 'settings', 'logout')
        ]
        if selected_items:
            row_height = dp(64)
            items_layout = FloatLayout(
                size_hint=(1, None),
                height=max(
                    (
                        (item.get('row', 1) - 1) * row_height
                        + item.get('height', 40)
                        + dp(8)
                        for item in selected_items
                    ),
                    default=0
                )
            )
            layout_columns = 12
            item_buttons = []
            for item in selected_items:
                column = item.get('column', 1) - 1
                row = item.get('row', 1) - 1
                button_width = dp(item.get('width', 120))
                button_height = dp(item.get('height', 40))
                item_button = Button(
                    text=item['label'],
                    size_hint=(None, None),
                    size=(button_width, button_height),
                    style_dimensions=False,
                    background_normal='',
                    background_color=(0.12, 0.14, 0.16, 1),
                    color=(0.92, 0.94, 0.95, 1),
                    halign='left',
                    padding=(dp(16), 0),
                    font_size=sp(15)
                )
                item_button.menu_layout = (
                    column,
                    row,
                    button_width,
                    button_height,
                    layout_columns,
                    row_height
                )
                item_button.bind(
                    on_release=lambda button, selected=item: self._select_drawer_item(
                        selected,
                        drawer_view
                    )
                )
                items_layout.add_widget(item_button)
                item_buttons.append(item_button)

            def update_menu_item_layout(layout, size):
                unit_width = size[0] / layout_columns
                for button in item_buttons:
                    column, row, button_width, button_height, _, cell_height = button.menu_layout
                    button.x = column * unit_width + dp(4)
                    button.y = (
                        layout.height
                        - row * cell_height
                        - button_height
                        + dp(4)
                    )
                    button.width = max(
                        dp(1),
                        min(button_width, layout.width - button.x - dp(4))
                    )
                    button.height = button_height

            items_layout.bind(size=update_menu_item_layout)
            update_menu_item_layout(items_layout, items_layout.size)
            items_scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
            items_scroll.add_widget(items_layout)
            drawer.add_widget(items_scroll)
        else:
            drawer.add_widget(Label(
                text='Bu menü için henüz öğe eklenmemiş.',
                color=(0.72, 0.76, 0.78, 1),
                halign='left',
                valign='top'
            ))

        if self.login_enabled:
            drawer.add_widget(Label(
                text='Giriş, ayarlar ve oturum işlemleri menü öğelerine bağlanabilir.',
                size_hint_y=None,
                height=dp(64),
                color=(0.62, 0.66, 0.68, 1),
                font_size=sp(12),
                halign='left',
                valign='middle'
            ))
        overlay.add_widget(drawer)
        drawer_view.add_widget(overlay)
        drawer_view.bind(
            size=lambda modal, size: self._resize_drawer(modal, size, drawer)
        )
        drawer_view.open()
        Animation(x=0, d=0.2, t='out_cubic').start(drawer)
        self.drawer_view = drawer_view

    @staticmethod
    def _resize_drawer(drawer_view, size, drawer):
        drawer.width = max(
            dp(1),
            min(dp(320), size[0] - dp(16), size[0] * 0.84)
        )
        if drawer.x < 0:
            drawer.x = -drawer.width

    def _select_drawer_item(self, item, drawer_view):
        drawer_view.dismiss()
        action = item['action']
        if action == 'home':
            if self.manager is not None:
                self.manager.current = 'main'
        elif action == 'cards':
            if hasattr(self, 'cards'):
                Clock.schedule_once(
                    lambda dt: self.scroll.scroll_to(self.cards, padding=dp(12)),
                    0.2
                )
        elif action in ('about', 'help', 'message'):
            title = item['label']
            default_messages = {
                'about': 'Uygulama ana ekranı ve seçtiğiniz içerik bileşenleri.',
                'help': 'Yardım için uygulama yöneticinizle iletişime geçin.',
            }
            message = item.get('message') or default_messages.get(action, '')
            label = Label(
                text=message,
                padding=(dp(20), dp(20)),
                halign='left',
                valign='middle'
            )
            label.bind(size=lambda widget, value: setattr(widget, 'text_size', value))
            Clock.schedule_once(
                lambda dt: Popup(
                    title=title,
                    content=label,
                    size_hint=(0.82, 0.3)
                ).open(),
                0.2
            )
        elif action == 'login':
            if not self.login_enabled:
                return
            self.go_to_login(None)
        elif action == 'settings':
            if self.login_enabled and self.account_button is None:
                self.go_to_login(None)
            elif self.login_enabled and self.manager is not None:
                self.manager.current = 'settings'
        elif action == 'logout':
            if self.login_enabled:
                self.sign_out()


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'settings'
        layout = BoxLayout(orientation='vertical', padding=dp(24), spacing=dp(16), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(52), spacing=dp(12))
        back = Button(
            text='‹  Ana sayfa',
            size_hint=(None, 1),
            width=dp(130),
            background_normal='',
            background_color=(0.15, 0.17, 0.20, 1)
        )
        back.bind(on_press=self.go_home)
        header.add_widget(back)
        header.add_widget(Label(text='[b]Ayarlar[/b]', markup=True, font_size=sp(22), halign='left'))
        layout.add_widget(header)
        self.account_details = Label(
            text='Hesap bilgileri giriş yapıldığında burada görünür.',
            halign='left',
            valign='middle',
            font_size=sp(14),
            color=(0.78, 0.81, 0.83, 1),
            size_hint_y=None,
            height=dp(100)
        )
        self.account_details.bind(
            size=lambda widget, value: setattr(widget, 'text_size', value)
        )
        layout.add_widget(self.account_details)
        settings_heading = Label(
            text='Hesap ve uygulama ayarları',
            font_size=sp(18),
            halign='left',
            size_hint_y=None,
            height=dp(36)
        )
        settings_heading.bind(
            size=lambda widget, value: setattr(widget, 'text_size', value)
        )
        layout.add_widget(settings_heading)
        description = Label(
            text='Bu bölüm, seçilen giriş sistemine bağlı hesap bilgilerini gösterir.',
            font_size=sp(14),
            color=(0.65, 0.69, 0.72, 1),
            halign='left',
            valign='top',
            size_hint_y=None,
            height=dp(72)
        )
        description.bind(size=lambda widget, value: setattr(widget, 'text_size', value))
        layout.add_widget(description)
        sign_out = Button(
            text='Oturumu kapat',
            size_hint_y=None,
            height=dp(48),
            background_normal='',
            background_color=(0.8, 0.18, 0.2, 1)
        )
        sign_out.bind(on_press=self.sign_out)
        layout.add_widget(sign_out)
        self.add_widget(ResponsiveForm(layout, max_width=720))

    def on_pre_enter(self, *args):
        if self.manager is not None and self.manager.has_screen('main'):
            user = self.manager.get_screen('main').current_user
            name = str(user.get('name') or user.get('username') or 'Account')
            email = str(user.get('email') or '')
            self.account_details.text = f'{name}\n{email}' if email else name

    def go_home(self, instance):
        if self.manager is not None:
            self.manager.current = 'main'

    def sign_out(self, instance):
        if self.manager is not None:
            self.manager.get_screen('main').sign_out()
