from textual.app import ComposeResult
from textual.widgets import Button, Input, Static


class WelcomeScreen(Static):
    def compose(self) -> ComposeResult:

        yield Static("[bold cyan]Welcome to Purchase Utility Calculator[/bold cyan]\n\n"
            "This tool helps you make optimal decisions about purchases.\n"
            "Fill in the information below to get started.\n",
            id="welcome-text")

        yield Static("\n[bold]What item are you considering?[/bold]")
        yield Input(placeholder="e.g., Laptop", id="item_name")
        
        yield Static("\n[bold]What is the price?[/bold]")
        yield Input(placeholder="e.g., 1200", id="price")
        
        yield Static("\n[bold]What is your income level?[/bold]")
        yield Static("[dim]Press 1=low, 2=medium, 3=high[/dim]")
        yield Input(placeholder="low/medium/high", id="income_level")
        
        yield Static("")  # Spacing
        yield Button("Continue →", variant="primary", id="continue")
