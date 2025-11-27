from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Input, RadioButton, RadioSet, Static

from src.forms.results import ResultsScreen


class TimeAndCategoryScreen(Screen):
    def on_mount(self) -> None:
        """Set border title when screen is mounted"""
        self.query_one("#time-category-panel", Container).border_title = (
            "Step 3: Time & Category"
        )
        self.query_one("#time_and_usage", Vertical).border_title = "Time and Usage"
        self.query_one("#hours_pr_week", Input).border_title = (
            "Estiamted hours per week of use"
        )
        self.query_one("#use_probability", RadioSet).border_title = (
            "How probable is it to meet the hours per week estimate?"
        )
        self.query_one("#life_span", Input).border_title = "Life span (months)"
        self.query_one("#category", RadioSet).border_title = "Benefit Category"

    def compose(self) -> ComposeResult:

        with Vertical(id="content"):
            with Container(classes="panel", id="time-category-panel"):
                yield Static(
                    "Tell us about usage patterns and expected lifespan.",
                    classes="hint",
                )

                with Vertical(classes="section", id="time_and_usage"):
                    yield Input(
                        placeholder="e.g., 2", id="hours_pr_week", type="number"
                    )
                    with RadioSet(id="use_probability"):
                        yield RadioButton("Low", id="low")
                        yield RadioButton("Medium", id="medium", value=True)
                        yield RadioButton("High", id="high")

                    yield Input(placeholder="e.g., 14", id="life_span", type="number")

                with RadioSet(id="category"):
                    yield RadioButton("Entertainment", id="entertainment")
                    yield RadioButton("Efficiency", id="efficiency", value=True)
                    yield RadioButton("Quality of Life", id="qol")

                with Horizontal(id="button-group"):
                    yield Button("← Back", variant="default", id="back")
                    yield Button("Continue →", variant="primary", id="continue")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "continue":
            time_use = self.query_one("#hours_pr_week", Input).value
            use_probability_radio = self.query_one("#use_probability", RadioSet)
            use_probability = use_probability_radio.pressed_button.id
            life_span = self.query_one("#life_span", Input).value

            category_radio = self.query_one("#category", RadioSet)
            category = category_radio.pressed_button.id

            self.app.purchase_data["time_use"] = float(time_use)
            self.app.purchase_data["use_probability"] = use_probability
            self.app.purchase_data["life_span"] = int(life_span)
            self.app.purchase_data["category"] = category

            # Navigate to results screen
            self.app.push_screen(ResultsScreen(self.app.purchase_data))

        elif event.button.id == "back":
            self.app.pop_screen()
