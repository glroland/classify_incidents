import logging
import click
from from_dir_command import FromDirectoryCommand
from from_file_command import FromFileCommand
from from_snow_command import FromServiceNowCommand

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@click.group()
def cli():
    """ CLI for reviewing IT incident data and grouping into related contexts for further action. """
    pass

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
@click.argument('input')
@click.argument('output')
def from_file(input : str, output : str):
    """ Loads incidents from a file. """
    click.echo("Classifying Incidents from file.  Input=" + input + " Output=" + output)
    command = FromFileCommand()
    command.filename_w_path = input
    command.output_filename = output
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
