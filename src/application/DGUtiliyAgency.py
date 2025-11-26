from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Button, Footer, Header, Input, RadioSet

from ..forms.welcome import WelcomeScreen


class DGUtilityAgency(App):
    CSS = """
    Screen {
        align: center middle;
        background: $surface;
    }

    /* Lazy-inspired container styles */
    .panel {
        border: tall $primary;
        background: $surface;
        padding: 1;
        margin: 0;
        width: 90;
        min-width: 80;
        height: auto;
    }

    .panel-title {
        color: $accent;
        text-style: bold;
        padding: 0;
    }

    .section {
        border: round $primary-darken-2;
        background: $panel;
        padding: 1;
        margin: 0 0 1 0;
        height: auto;
        min-height: 5;
    }

    .section-header {
        color: $text;
        text-style: bold;
        padding: 0;
    }

    .section-hint {
        color: $text-muted;
        padding: 0;
    }

    /* Header and Footer */
    Header {
        background: $primary;
        color: $text;
    }

    Footer {
        background: $panel;
    }

    /* Content containers */
    #content {
        width: 100%;
        height: auto;
        align: center top;
        padding: 0;
        overflow-y: auto;
    }

    #welcome-panel {
        border: thick $accent;
        background: $surface;
        padding: 1;
        margin: 0;
        height: auto;
    }

    #welcome-text {
        color: $text;
        padding: 0 0 1 0;
    }

    /* Container sizing */
    Container {
        height: auto;
        width: 100%;
    }

    Vertical {
        height: auto;
        width: 100%;
    }

    Horizontal {
        height: auto;
        width: 100%;
    }

    /* Input fields */
    Input {
        border: tall $primary;
        background: $boost;
        color: white;
        margin: 0 0 1 0;
        width: 100%;
        min-width: 40;

        height: 3;
    }

    Input:focus {
        border: tall $accent;
        color: white;
    }

    Input > .input--cursor {
        color: white;
        background: $accent;
    }

    Input > .input--placeholder {
        color: $text-muted;
    }

    /* Radio buttons and checkboxes */
    RadioSet {
        background: $panel;
        border: round $primary-darken-2;
        padding: 0 1;
        margin: 0 0 1 0;
        height: auto;
        min-height: 4;
    }

    RadioButton {
        background: $surface;
        margin: 0 0 0 1;
        padding: 0 1;
        height: auto;
    }

    RadioButton:hover {
        background: $boost;
    }

    Checkbox {
        background: $surface;
        margin: 0 0 0 1;
        padding: 0 1;
        height: auto;
    }

    Checkbox:hover {
        background: $boost;
    }

    #life-areas-checkboxes {
        border: round $primary-darken-2;
        background: $panel;
        padding: 0 1;
        margin: 0 0 1 0;
        height: auto;
        min-height: 4;
    }

    /* Buttons */
    Button {
        margin: 0 1;
        min-width: 16;
        height: 3;
    }

    Button.-primary {
        background: $accent;
        color: $text;
        border: tall $accent-lighten-1;
    }

    Button.-primary:hover {
        background: $accent-lighten-2;
    }

    #button-group {
        margin: 1 0 0 0;
        height: auto;
        align: center middle;
        width: 100%;
    }

    /* Labels and text */
    Static {
        color: $text;
        height: auto;
    }

    .label {
        color: $text;
        text-style: bold;
        padding: 0;
        height: auto;
    }

    .hint {
        color: $text-muted;
        text-style: italic;
        height: auto;
    }
    """
    purchase_data = {}

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),  # Press 'q' to quit
        Binding("ctrl+c", "quit", "Quit", priority=True),  # Ctrl+C also quits
    ]

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
