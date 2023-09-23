import flet as ft
from screen.user_control.app_bar import NavBar
from screen.router_manager import Router

__version__ = '0.8b'

def main(page: ft.Page) -> ft.FletApp:
    # Page settings
    page.title = f'MangaYouKnow {__version__}'
    page.theme_mode = 'dark'
    page.window_min_width = 770
    page.window_min_height = 600
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER

    # Router setup
    router = Router(page)
    page.on_route_change = router.route_change

    # NavBar setup
    page.banner = NavBar(page)

    # Scroll mode
    page.scroll = ft.ScrollMode.ADAPTIVE

    # Layout setup
    page.add(ft.Stack([
        ft.Column([router.body], left=90, top=0),
        router.reader
    ]))

    # Data initialization
    page.data = {'reader_container': router.reader}

    # Initial route
    page.go('/')

    # Update the page
    page.update()

if __name__ == '__main__':
    ft.app(target=main)
