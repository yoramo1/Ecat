import sys
import os
import click
import Maestro
import workspace


@click.group()
def cli():
	pass


		
@click.command()
@click.argument('path',  type=click.Path())
def show_workspace(path):
	'''
	display the workspace
	'''
	ws = workspace.workspace(path)
	print(ws.to_string())
	

		
'''
	commands
'''		
cli.add_command(show_workspace)
	
'''
	main - entry point
'''
if (__name__=='__main__'):
	cli()
