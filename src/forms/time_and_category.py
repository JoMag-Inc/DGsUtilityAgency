from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, RadioButton, RadioSet, Static


class TimeAndCategoryScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="content"):
            with Container(classes="panel"):
                yield Static(
                    "[bold cyan]╔═══════════════════════════════════════════════════╗[/bold cyan]\n"
                    "[bold cyan]║[/bold cyan]  Step 3: Time & Category                         [bold cyan]║[/bold cyan]\n"
                    "[bold cyan]╚═══════════════════════════════════════════════════╝[/bold cyan]",
                    classes="panel-title",
                )

                yield Static(
                    "Tell us about usage patterns and expected lifespan.",
                    classes="hint",
                )

                with Vertical(classes="section"):
                    yield Static("[bold]Usage Time[/bold]", classes="section-header")
                    yield Static(
                        "How many hours per week will you use this?", classes="label"
                    )
                    yield Input(
                        placeholder="e.g., 2", id="hours_pr_week", type="number"
                    )
                    yield Static(
                        "[bold]How probable do you think it is that you will get to use it as much as you say?[/bold]"
                    )
                    with RadioSet(id="use_probability"):
                        yield RadioButton("Low", id="low")
                        yield RadioButton("Medium", id="meduim")
                        yield RadioButton("High", id="high")

                    yield Static(
                        "What is the life span of the item in months?", classes="label"
                    )
                    yield Input(placeholder="e.g., 14", id="life_span", type="number")

                with Vertical(classes="section"):
                    yield Static(
                        "[bold]Benefit Category[/bold]", classes="section-header"
                    )
                    yield Static("What category does this belong to?", classes="hint")

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
            use_probability_radio = self.query_one("#use_probability", RadioSet)
            use_probability = use_probability_radio.pressed_button.id
            life_span = self.query_one("#life_span", Input).value

            category_radio = self.query_one("#category", RadioSet)
            category = category_radio.pressed_button.id

            self.app.purchase_data["time_use"] = time_use
            self.app.purchase_data["use_probability"] = use_probability
            self.app.purchase_data["life_span"] = life_span
            self.app.purchase_data["category"] = category
            self.app.notify(f"All data: {self.app.purchase_data}")

        elif event.button.id == "back":
            self.app.pop_screen()
