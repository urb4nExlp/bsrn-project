from textual.app import App
from textual.widgets import Header, Footer, Static


class HelloWorldApp(App):
    async def on_mount(self):
        header = Header()
        footer = Footer()
        message = Static("Hallo, dies ist eine einfache Textual-Anwendung!", id="message")

        await self.view.dock(header, edge="top")
        await self.view.dock(footer, edge="bottom")
        await self.view.dock(message, edge="center")


if __name__ == "__main__":
    HelloWorldApp.run(log="textual.log")
