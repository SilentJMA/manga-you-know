import flet as ft
from backend.database import DataBase

class Configs:
    def __init__(self, page: ft.Page):
        self.page = page
        self.database = DataBase()
        self.keybinds = self.database.get_config()['keybinds']
        self.create_keybind_buttons()

    def create_keybind_buttons(self):
        def listen_key(button, key):
            button.text = '...'
            self.page.update()

        keybind_buttons = []
        for key, label in self.keybinds.items():
            button = ft.TextButton(label, disabled=True)
            button.on_click = lambda event, btn=button, key=key: listen_key(btn, key)
            keybind_buttons.append(button)

        change_keys_content = ft.Column([
            ft.Card(ft.Row([btn, ft.Text(label)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), margin=1)
            for btn, (key, label) in zip(keybind_buttons, self.keybinds.items())
        ])

        change_keys_dialog = ft.AlertDialog(
            title=ft.Text('EM BREVE!'),
            content=change_keys_content
        )

        self.page.dialog = change_keys_dialog
        change_keys_dialog.open = True
        self.page.update()

    def return_content(self):
        return ft.Row(
            [   
                ft.Column([
                    ft.TextButton('Mudar keybinds', on_click=self.create_keybind_buttons)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            width=1300
        )
