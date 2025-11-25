from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Button, Footer, Header, Input

from ..forms.welcome import WelcomeScreen


class DGUtilityAgency(App):
    CSS = """
    Screen {
        align: center middle;
    }
    
    #welcome-text {
        margin: 1 2;
        padding: 1 2;
    }
    
    Input {
        margin: 0 2;
        width: 60;
    }
    
    Button {
        margin: 1 2;
    }
    
    Static {
        margin: 0 2;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),  # Press 'q' to quit
        Binding("ctrl+c", "quit", "Quit", priority=True),  # Ctrl+C also quits
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield WelcomeScreen()
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "continue":
            # Get the values from inputs
            item_name = self.query_one("#item_name", Input).value
            price = self.query_one("#price", Input).value
            income_level = self.query_one("#income_level", Input).value

            # For now, just show what we collected
            self.notify(f"Collected: {item_name}, ${price}, {income_level}")


def main():
    app = DGUtilityAgency()
    app.run()


if __name__ == "__main__":
    main()
