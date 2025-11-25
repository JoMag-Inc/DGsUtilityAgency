from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, RadioButton, RadioSet, Static


class TimeAndCategoryScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="content"):
            yield Static(
                "[bold cyan]Step 3: Time & Category[/bold cyan]\n\n"
                "Tell us how much time you will spend with this, how long it will last and in which category of benefit the item lands in.",
                id="time-and-category-header",
            )

            yield Static("\n[bold]How many hours per week will you use this?[/bold]")
            yield Static("[dim]Enter the number of hours[/dim]")
            yield Input(placeholder="e.g., 2", id="hours_pr_week", type="number")

            yield Static("\n[bold]What is the life span of the item in months?[/bold]")
            yield Static("[dim]Enter the expected duration[/dim]")
            yield Input(placeholder="e.g., 14", id="life_span", type="number")

            yield Static("[bold]What category does this belong to?[/bold]")
            yield Static("[dim]Select one[/dim]")

            with RadioSet(id="category"):
                yield RadioButton("Entertainment", id="entertainment")
                yield RadioButton("Efficiency", id="efficiency", value=True)
                yield RadioButton("Quality of Life", id="qol")

            with Horizontal(id="button-group"):
                yield Button("← Back", variant="default", id="back")
                yield Button("Continue →", variant="primary", id="continue")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "continue":
            time_use = self.query_one("#hours_pr_week", Input).value
            life_span = self.query_one("#life_span", Input).value
            category_radio = self.query_one("#category", RadioSet)
            category = category_radio.pressed_button.id

            self.app.purchase_data["time_use"] = time_use
            self.app.purchase_data["life_span"] = life_span
            self.app.purchase_data["category"] = category
            self.app.notify(f"All data: {self.app.purchase_data}")

        elif event.button.id == "back":
            self.app.pop_screen()
