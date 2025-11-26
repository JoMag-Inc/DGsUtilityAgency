from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Input, RadioButton, RadioSet, Static

from src.forms.life_areas import LifeAreasScreen


class WelcomeScreen(Screen):
    def compose(self) -> ComposeResult:
        with Container(classes="panel", id="welcome-panel"):
            yield Static(
                "[bold cyan]╔═══════════════════════════════════════════════════╗[/bold cyan]\n"
                "[bold cyan]║[/bold cyan]           Welcome to DGs Utility Agency[bold cyan]           ║[/bold cyan]\n"
                "[bold cyan]╚═══════════════════════════════════════════════════╝[/bold cyan]\n",
                classes="panel-title",
            )

            yield Static(
                "This tool helps you make optimal decisions about purchases.\n"
                "Fill in the information below to get started.",
                id="welcome-text",
            )

            with Vertical(classes="section"):
                yield Static("[bold]Item Information[/bold]", classes="section-header")
                yield Static("What item are you considering?", classes="label")
                yield Input(placeholder="e.g., Laptop", id="item_name")

                yield Static("What is the price (dollars)?", classes="label")
                yield Input(placeholder="e.g., 1200", id="price")

            with Vertical(classes="section"):
                yield Static("[bold]Income Level[/bold]", classes="section-header")
                yield Static("Select your income level:", classes="hint")
                with RadioSet(id="income_level"):
                    yield RadioButton("Low", id="low")
                    yield RadioButton("Medium", id="medium", value=True)  # Default
                    yield RadioButton("High", id="high")

            with Horizontal(id="button-group"):
                yield Button("Continue →", variant="primary", id="continue")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle continue button"""
        if event.button.id == "continue":
            # Collect data from this screen
            item_name = self.query_one("#item_name", Input).value
            price = self.query_one("#price", Input).value
            income_radio = self.query_one("#income_level", RadioSet)
            income_level = income_radio.pressed_button.id

            # Store in app's data
            self.app.purchase_data = {
                "item_name": item_name,
                "price": price,
                "income_level": income_level,
            }

            # Go to next screen
            self.app.push_screen(LifeAreasScreen())
