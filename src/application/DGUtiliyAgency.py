from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Button, Footer, Header, Input, RadioSet

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

    #content {
        width: 70;
        padding: 1 2;
    }

    #life-areas-header {
        margin: 1 0 2 0;
        padding: 1 2;
        text-align: center;
    }

    #life-areas-checkboxes {
        margin: 1 2;
        padding: 1;
    }

    #necessity {
        margin: 1 2;
        padding: 1;
    }

    #button-group {
        margin: 2 2 1 2;
        height: auto;
        align: center middle;
    }

    #button-group Button {
        margin: 0 1;
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

    Checkbox {
        margin: 0 0 1 0;
    }

    RadioButton {
        margin: 0 0 1 0;
    }
    """
    purchase_data = {}

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),  # Press 'q' to quit
        Binding("ctrl+c", "quit", "Quit", priority=True),  # Ctrl+C also quits
    ]

    MODES = {}

    def compose(self) -> ComposeResult:
        yield Header()
        yield WelcomeScreen()
        yield Footer()

    def on_mount(self) -> None:
        self.push_screen(WelcomeScreen())


def main():
    app = DGUtilityAgency()
    app.run()


if __name__ == "__main__":
    main()
