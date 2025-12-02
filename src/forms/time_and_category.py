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
            "Estimated hours per week of use"
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

            # Validate hours per week
            if not time_use or len(time_use.strip()) == 0:
                self.app.notify("Hours per week is required", severity="error")
                return
            try:
                time_use_value = float(time_use)
                if time_use_value < 0:
                    self.app.notify("Hours per week cannot be negative", severity="error")
                    return
                if time_use_value > 168:
                    self.app.notify("Hours per week cannot exceed 168 (hours in a week)", severity="error")
                    return
            except ValueError:
                self.app.notify("Hours per week must be a valid number", severity="error")
                return

            # Validate life span
            if not life_span or len(life_span.strip()) == 0:
                self.app.notify("Life span is required", severity="error")
                return
            try:
                life_span_value = int(life_span)
                if life_span_value <= 0:
                    self.app.notify("Life span must be greater than 0", severity="error")
                    return
                if life_span_value > 600:
                    self.app.notify("Life span cannot exceed 600 months (50 years)", severity="error")
                    return
            except ValueError:
                self.app.notify("Life span must be a valid whole number", severity="error")
                return

            self.app.purchase_data["time_use"] = time_use_value
            self.app.purchase_data["use_probability"] = use_probability
            self.app.purchase_data["life_span"] = life_span_value
            self.app.purchase_data["category"] = category

            # Navigate to results screen
            self.app.push_screen(ResultsScreen(self.app.purchase_data))

        elif event.button.id == "back":
            self.app.pop_screen()
