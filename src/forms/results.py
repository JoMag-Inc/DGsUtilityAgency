from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Input, Static

from src.calculator import (
    calculate_breakeven_probability,
    calculate_expected_utility_buy,
    calculate_expected_utility_not_buy,
    calculate_utilities,
)


class ResultsScreen(Screen):
    """Screen displaying the utility calculation results."""

    # Reactive probabilities that update the UI when changed
    p_useful_if_buy = reactive(0.5)
    p_useful_if_not_buy = reactive(0.1)

    def __init__(self, purchase_data: dict):
        super().__init__()
        self.results = calculate_utilities(purchase_data)

    def compose(self) -> ComposeResult:

        with Vertical(id="content"):
            with Container(classes="panel", id="results-panel"):
                yield Static(
                    "Adjust the probabilities below to see how the recommendation changes.\n",
                    classes="hint",
                )

                with Vertical(classes="section", id="scenarios"):
                    yield Static(
                        f"Buy+Useful: {self.results['u_buy_useful']:.2f}  "
                        f"Buy+Not: {self.results['u_buy_not_useful']:.2f}  "
                        f"NoBuy+Need: {self.results['u_not_buy_useful']:.2f}  "
                        f"NoBuy+NoNeed: {self.results['u_not_buy_not_useful']:.2f}",
                        id="scenario-values",
                    )

                yield Input(
                    placeholder="0.0-1.0",
                    value="0.5",
                    id="p_useful_buy",
                    type="number",
                )

                yield Input(
                    placeholder="0.0-1.0",
                    value="0.5",
                    id="p_useful_not_buy",
                    type="number",
                )

                with Vertical(classes="section", id="analysis"):
                    yield Static("", id="expected_utility_buy")
                    yield Static("", id="expected_utility_not_buy")
                    yield Static("", id="breakeven_analysis")
                    yield Static(self._get_recommendation(), id="recommendation")

                with Horizontal(id="button-group"):
                    yield Button("← Start Over", variant="default", id="start_over")

    def on_mount(self) -> None:
        """Initialize the expected utility display when screen loads."""
        item_name = self.app.purchase_data.get("item_name", "Unknown Item")
        self.query_one("#results-panel", Container).border_title = (
            f"Analysis: {item_name}"
        )
        self.query_one("#scenarios", Vertical).border_title = "Scenario Values"
        self.query_one("#p_useful_buy", Input).border_title = "P(useful|buy)"
        self.query_one("#p_useful_not_buy", Input).border_title = "P(useful|not buy)"
        self.query_one("#analysis", Vertical).border_title = "Expected Utilities"
        self._update_expected_utilities()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle changes to probability inputs."""
        if event.input.id == "p_useful_buy":
            if not event.value or len(event.value.strip()) == 0:
                return
            try:
                value = float(event.value)
                if 0 <= value <= 1:
                    self.p_useful_if_buy = value
                    self._update_expected_utilities()
                else:
                    self.app.notify("Probability must be between 0 and 1", severity="warning")
            except ValueError:
                self.app.notify("Probability must be a valid number", severity="warning")
        elif event.input.id == "p_useful_not_buy":
            if not event.value or len(event.value.strip()) == 0:
                return
            try:
                value = float(event.value)
                if 0 <= value <= 1:
                    self.p_useful_if_not_buy = value
                    self._update_expected_utilities()
                else:
                    self.app.notify("Probability must be between 0 and 1", severity="warning")
            except ValueError:
                self.app.notify("Probability must be a valid number", severity="warning")

    def _update_expected_utilities(self) -> None:
        """Update the expected utility displays."""
        eu_buy = calculate_expected_utility_buy(self.p_useful_if_buy, self.results)
        eu_not_buy = calculate_expected_utility_not_buy(
            self.p_useful_if_not_buy, self.results
        )
        breakeven = calculate_breakeven_probability(
            self.results, self.p_useful_if_not_buy
        )

        eu_buy_widget = self.query_one("#expected_utility_buy", Static)
        if eu_buy > eu_not_buy:
            eu_buy_widget.update(f"E[U(Buy)]: {eu_buy:.2f} ✓")
        else:
            eu_buy_widget.update(f"E[U(Buy)]: {eu_buy:.2f}")

        eu_not_buy_widget = self.query_one("#expected_utility_not_buy", Static)
        if eu_not_buy > eu_buy:
            eu_not_buy_widget.update(f"E[U(Don't Buy)]: {eu_not_buy:.2f} ✓")
        else:
            eu_not_buy_widget.update(f"E[U(Don't Buy)]: {eu_not_buy:.2f}")

        breakeven_widget = self.query_one("#breakeven_analysis", Static)
        breakeven_widget.update(f"Breakeven: {breakeven:.1%}")

        recommendation_widget = self.query_one("#recommendation", Static)
        recommendation_widget.update(self._get_recommendation())

    def _get_recommendation(self) -> str:
        """Generate a recommendation based on the current expected utilities."""
        eu_buy = calculate_expected_utility_buy(self.p_useful_if_buy, self.results)
        eu_not_buy = calculate_expected_utility_not_buy(
            self.p_useful_if_not_buy, self.results
        )
        breakeven = calculate_breakeven_probability(
            self.results, self.p_useful_if_not_buy
        )

        if eu_buy > eu_not_buy:
            confidence = eu_buy - eu_not_buy
            return f"Recommendation: BUY (gain: {confidence:.2f})"
        else:
            deficit = eu_not_buy - eu_buy
            return f"Recommendation: DON'T BUY (need {breakeven:.1%}, have {self.p_useful_if_buy:.1%})"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start_over":
            # Clear all screens and go back to welcome
            self.app.pop_screen()  # Pop results
            self.app.pop_screen()  # Pop time_and_category
            self.app.pop_screen()  # Pop life_areas
            self.app.pop_screen()  # Pop welcome
            from .welcome import WelcomeScreen

            self.app.push_screen(WelcomeScreen())
