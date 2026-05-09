import typer

from cli import interactive_menu
from cli.commands import buy, sell

app = typer.Typer(invoke_without_command=True)

app.command()(buy)
app.command()(sell)


@app.callback()
def main(ctx: typer.Context):

    if ctx.invoked_subcommand:
        return

    interactive_menu()


if __name__ == "__main__":
    app()
