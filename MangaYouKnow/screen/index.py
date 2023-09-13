import asyncio

import flet as ft
from time import sleep
from time import time
from backend.downloader.mangalivre import MangaLivreDl
from backend.downloader.mangadex import MangaDexDl
from backend.database import DataBase
from backend.download_manager import Downloader
import flet_core.margin as margin


class Index:
    def __init__(self, page: ft.Page):

        connection_data = DataBase()
        connection_manga = MangaDexDl()
        downloader = Downloader()
        source_selector = ft.Dropdown(options=[
            ft.dropdown.Option('md', text='MangaDex'),
            ft.dropdown.Option('ml', text='MangaLivre'),
            ft.dropdown.Option('mf', text='MangaFire'),
            ft.dropdown.Option('gkk', text='Gekkou'),
            ft.dropdown.Option('tsct', text='Taosect'),
            ft.dropdown.Option('tcb', text='TCB'),
            ft.dropdown.Option('op', text='OP Scans'),
        ], value='md')

        results = ft.Column(width=470, spacing=0.7)
        card = ft.Card(ft.Container(results), color='gray', visible=False)
        search = ft.TextField(
            label='Pesquisar Mangás...',
            width=500,
            border_radius=20,
            border_color=ft.colors.GREY_700,
            focused_border_color=ft.colors.BLUE_300,
        )

        index = ft.Stack(width=1300, height=1000)
        manga = ft.Row(visible=False)
        self.is_clicked = False

        def back_index(e):
            manga.visible = False
            index.visible = True
            page.update()

        def match_source(source: str):
            match source:
                case 'md':
                    return {
                        'id': 'id',
                        'db_id': 'md_id',
                        'name': 'attributes.title.en',
                    }
                case 'ml':
                    return {
                        'id': 'id_serie',
                        'db_id': 'ml_id',
                        'name': 'name',

                    }
                case 'mf':
                    return {
                        'db_id': 'mf_id',        
                    }
                case 'gkk':
                    return {
                        'db_id': 'gkk_id',
                    }
                case 'tsct':
                    return {
                        'db_id': 'tsct_id',       
                    }
                case 'db_tcb':
                    return {
                        'id': 'tcb_id',           
                    }
                case 'db_op':
                    return {
                        'id': 'op_id',
                    }
                case _:
                    return None


        def togle_favorite(manga: dict, button: ft.IconButton, is_on_search: bool = False):
            if connection_data.is_favorite(self.src_inf['db_id'], manga[self.src_inf['id']]):
                connection_data.delete_manga_by_id_key(self.src_inf['db_id'], manga[self.src_inf['id']])
                button.icon = ft.icons.BOOKMARK_OUTLINE
            else:
                connection_data.add_manga(manga[self.src_inf['name']], manga['link'].split('/')[-2], manga['cover'], ml_id=manga[self.src_inf['id']])
                button.icon = ft.icons.BOOKMARK_ROUNDED
            page.update()
            if is_on_search:
                self.is_clicked = True
                sleep(1)
                self.is_clicked = False
                search.focus()

        def manga_page(info_manga):
            button_favorite = ft.IconButton(
                ft.icons.BOOKMARK_ROUNDED if connection_data.is_favorite(self.src_inf['db_id'], info_manga[self.src_inf['id']]) else ft.icons.BOOKMARK_OUTLINE,
                height=30)
            button_favorite.on_click = lambda e, info=info_manga, button=button_favorite: togle_favorite(info, button)
            manga_dialog = ft.AlertDialog(
                title=ft.Text(info_manga[self.src_inf['name']][0:30], tooltip=info_manga[self.src_inf['name']]),
                content=ft.Row([
                    ft.Image(src=info_manga['cover'], height=400, width=ft.ImageFit.FIT_HEIGHT, animate_size=300,
                             border_radius=ft.border_radius.all(30)),
                ]),
                actions=[button_favorite]
            )
            manga_dialog.open = True
            page.dialog = manga_dialog

        def search_mangas(e: ft.ControlEvent = None):
            if len(e.control.value) == 0:
                results.controls.clear()
                card.visible = False
                page.update()
                return False
            results.controls.clear()
            results.controls.append(
                ft.ListTile(
                    key='noresult',
                    title=ft.Row([ft.Text('Procurando...'), ft.ProgressRing()],
                                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    disabled=True,
                    height=55
                )
            )
            card.visible = True
            page.update()
            self.src_inf = match_source(source_selector.value)
            response = downloader.search(source_selector.value, e.control.value)
            favorites = connection_data.get_database()
            list_favorites_id = [i[self.src_inf['id']] for i in favorites]
            card.visible = True
            results.controls.clear()
            if e.control.value != search.value:
                return False
            if not response:
                results.controls.append(
                    ft.ListTile(
                        key='noresult',
                        title=ft.Text('Nenhum mangá encontrado!'),
                        disabled=True,
                        height=55
                    )
                )
            else:
                for manga in response:
                    button_favorite = ft.IconButton(ft.icons.BOOKMARK_ROUNDED if manga[self.src_inf['id']] in list_favorites_id else ft.icons.BOOKMARK_OUTLINE, height=30)
                    button_favorite.on_click = lambda e, manga=manga, button=button_favorite: togle_favorite(manga, button, True)
                    results.controls.append(
                        ft.ListTile(
                            key='manga',
                            title=ft.Text(f'{manga[self.src_inf["name"]][0:42]}...' if len(manga[self.src_inf['name']]) > 45 else manga[self.src_inf['name']][0:50], tooltip=manga[self.src_inf['name']]),
                            height=45,
                            trailing=button_favorite,
                            on_click=lambda e, info=manga: manga_page(info)
                        )
                    )
                if len(search.value) == 0:
                    results.controls.clear()
                    card.visible = False
            page.update()

        def out_search(e):
            sleep(0.1)
            if self.is_clicked:
                return
            card.visible = False
            page.update()

        def focus_search(e):
            if len(results.controls) != 0:
                if results.controls[0].key == 'manga':
                    card.visible = True
                    page.update()

        search.on_change = search_mangas
        search.on_blur = out_search
        search.on_focus = focus_search

        index.controls.append(
            ft.ResponsiveRow([
                ft.Column([ft.Container(bgcolor='white', width=300)], col=3),
                ft.Column([ft.Container(search, padding=10)], col=6),
                ft.Column([ft.Container(source_selector, width=200, padding=10)], col=3),
            ], alignment=ft.MainAxisAlignment.CENTER, columns=12
            )
        )
        index.controls.append(
            ft.Row([], top=100)
        )
        index.controls.append(
            ft.Row([card], top=70, left=260)
        )

        self.content = ft.Column(
            [
                ft.Stack([
                    index,
                    manga
                ], width=1000, height=1000)
            ],
        )

    def return_content(self) -> ft.Row:
        return self.content
