from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Input, RadioButton, RadioSet, Static

from src.forms.life_areas import LifeAreasScreen


class WelcomeScreen(Screen):
    def on_mount(self) -> None:
        """Set border title when screen is mounted"""
        self.query_one("#welcome-panel", Container).border_title = (
            "Welcome to DGs Utility Agency"
        )
        self.query_one("#item_name", Input).border_title = "Item name"
        self.query_one("#price", Input).border_title = "Price (dollars)"
        self.query_one("#income_level", RadioSet).border_title = "Income Level"

    def compose(self) -> ComposeResult:
        with Container(classes="panel", id="welcome-panel"):
            yield Static(
                "This tool helps you make optimal decisions about purchases.\n"
                "Fill in the information below to get started.",
                id="welcome-text",
            )

            yield Input(placeholder="e.g., Laptop", id="item_name")
            yield Input(placeholder="e.g., 1200", id="price", type="number")

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

            # Validate item name
            if not item_name or len(item_name.strip()) == 0:
                self.app.notify("Item name is required", severity="error")
                return
            if len(item_name) > 100:
                self.app.notify("Item name must be 100 characters or less", severity="error")
                return

            # Validate price
            if not price or len(price.strip()) == 0:
                self.app.notify("Price is required", severity="error")
                return
            try:
                price_value = float(price)
                if price_value <= 0:
                    self.app.notify("Price must be greater than 0", severity="error")
                    return
            except ValueError:
                self.app.notify("Price must be a valid number", severity="error")
                return

            # Store in app's data
            self.app.purchase_data = {
                "item_name": item_name.strip(),
                "price": price_value,
                "income_level": income_level,
            }

            # Go to next screen
            self.app.push_screen(LifeAreasScreen())
