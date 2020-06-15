#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tictactoe.game as game

import click

HANDICAP = {
    'trivial': 62,
    'easy': 50,
    'medium': 38,
    'hard': 24,
    'impossible': 3
}


@click.command()
@click.option('--name', prompt=True, default='Human Player', help='Player name.')
@click.option('--level', prompt=True, default='medium', type=click.Choice([
              'trivial', 'easy', 'medium', 'hard', 'impossible'],
    case_sensitive=False))
def cli(name, level):
    h = HANDICAP[level]
    g = game.Game(h)
    g.play()


if __name__ == '__main__':
    cli()
