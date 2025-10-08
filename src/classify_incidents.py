import click

@click.group()
def cli():
    """ CLI for reviewing IT incident data and grouping into related contexts for further action. """
    pass

@cli.command()
@click.argument('path')
@click.option('--openai_baseurl', default=None, help='OpenAI Compatible Inferencing Endpoint')
def from_dir(path : str, openai_baseurl : str):
    """ Loads incidents from a directory. """
    click.echo("from_dir: " + path)

@cli.command()
def from_snow():
    """ Loads incidents directly from ServiceNow. """
    click.echo("from_snow" )

if __name__ == '__main__':
    cli()
