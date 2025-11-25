from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (
    Button,
    Checkbox,
    Footer,
    Header,
    RadioButton,
    RadioSet,
    Static,
)

from src.forms.time_and_category import TimeAndCategoryScreen


class LifeAreasScreen(Screen):

    def compose(self):
        yield Header()

        with Vertical(id="content"):
            yield Static(
                "[bold cyan]Step 2: Life Areas & Necessity[/bold cyan]\n\n"
                "Tell us more about this purchase.",
                id="life-areas-header",
            )

            yield Static("[bold]What areas of life does this affect?[/bold]")
            yield Static("[dim]Select all that apply[/dim]")

            with Vertical(id="life-areas-checkboxes"):
                yield Checkbox("Career & Professional", id="career")
                yield Checkbox("Personal & Social", id="personal")
                yield Checkbox("Health & Wellness", id="health")

            yield Static("[bold]How necessary is this item?[/bold]")
            yield Static("[dim]Select one[/dim]")

            with RadioSet(id="necessity"):
                yield RadioButton("Essential - Must have", id="essential", value=True)
                yield RadioButton(
                    "Nice to have - Want but not critical", id="nice_to_have"
                )

            with Horizontal(id="button-group"):
                yield Button("← Back", variant="default", id="back")
                yield Button("Continue →", variant="primary", id="continue")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "continue":

            life_areas = []
            career_checkbox = self.query_one("#career", Checkbox)
            personal_checkbox = self.query_one("#personal", Checkbox)
            health_checkbox = self.query_one("#health", Checkbox)

            if career_checkbox.value:
                life_areas.append("career")
            if personal_checkbox.value:
                life_areas.append("personal")
            if health_checkbox.value:
                life_areas.append("health")

            necessity_radio = self.query_one("#necessity", RadioSet)
            necessity = necessity_radio.pressed_button.id

            self.app.purchase_data["life_areas"] = life_areas
            self.app.purchase_data["necessity"] = necessity

            self.app.push_screen(TimeAndCategoryScreen())

        elif event.button.id == "back":
            self.app.pop_screen()
