import flet as ft
from screen.user_control.app_bar import NavBar
from screen.router_manager import Router


__version__ = '0.7b'


def __main__(page: ft.Page) -> ft.FletApp:
    page.title = f'MangaYouKnow {__version__}'
    page.theme_mode = 'dark'
    page.window_min_width = 770
    page.window_min_height = 600
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    router = Router(page)
    page.on_route_change = router.route_change
    # page.appbar = NavBar(page)
    page.banner = NavBar(page)
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.add(
        ft.Stack([
            ft.Column([
                router.body
            ],
            left=90,
            top=0
            ),
            router.reader
        ])
    )
    page.data = {}
    # def on_key(e: ft.KeyboardEvent):
    #     if e.key == 'Arrow Right':
    #         print(e.key)
    #     if e.key == 'F11':
    #         if page.window_full_screen:
    #             page.window_full_screen = False
    #         else:
    #             page.window_full_screen = True
    #     page.update()
    # page.on_keyboard_event = on_key
    # page.data['key_manager'] = on_key
    page.go('/')
    # def resize(e:ft.ControlEvent):
    #     page.update()
    # page.on_resize = resize
    page.update()


if __name__ == '__main__':
    ft.app(target=__main__)
    