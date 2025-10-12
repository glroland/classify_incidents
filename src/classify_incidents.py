""" CLI entry point for Incident Analysis Application. """
import logging
import click
from commands.from_dir import FromDirectoryCommand
from commands.from_file import FromFileCommand
from commands.from_snow import FromServiceNowCommand

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.group()
def cli():
    """ CLI for reviewing IT incident data and grouping into related contexts for 
        further action. 
    """

@cli.command()
@click.argument('path')
@click.argument('output_dir')
def from_dir(path : str, output_dir : str):
    """ Loads incidents from a directory. """
    click.echo("Classifying Incidents from Root Directory: " + path)
    click.echo("Publishing Results to: " + output_dir)
    command = FromDirectoryCommand()
    command.input_path = path
    command.output_dir = output_dir
    command.go()
    click.echo("Successfully Completed!")

@cli.command()
@click.argument('input_file')
@click.argument('output_file')
def from_file(input_file : str, output_file : str):
    """ Loads incidents from a file. """
    click.echo("Classifying Incidents from file.  Input=" + input_file + " Output=" + output_file)
    command = FromFileCommand()
    command.filename_w_path = input_file
    command.output_filename = output_file
    command.go()
    click.echo("Successfully Completed!")

@cli.command()
def from_snow():
    """ Loads incidents directly from ServiceNow. """
    click.echo("Classifying Incidents from ServiceNow")
    command = FromServiceNowCommand()
    command.go()
    click.echo("Successfully Completed!")

if __name__ == '__main__':
    cli()
