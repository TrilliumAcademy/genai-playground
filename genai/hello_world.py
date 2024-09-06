#!/usr/bin/env python3

# This is a simple hello world program just to make sure everything is working correctly.

from time import sleep

from rich.console import Console

console = Console()

with console.status("[magenta]Nerd detector booting up") as status:
    sleep(3)
    console.log("Importing advanced AI")
    sleep(3)
    console.log("Advanced nerd detection AI Ready")
    sleep(3)
    status.update(status="[bold blue] Scanning for nerds", spinner="earth")
    sleep(3)
    console.log("Found nerd sitting at keyboard")
    sleep(3)
    status.update(
        status="[bold red]Moving nerd.exe to Trash",
        spinner="bouncingBall",
        spinner_style="yellow",
    )
    sleep(5)
    console.print("[bold green]Nerd deleted successfully")
