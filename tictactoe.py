#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tictactoe.game as game

import click
import numpy as np


@click.command()
@click.option('--name', prompt=True, default='Human Player',
              help='Player name.')
@click.option('--level', prompt=True, default='medium', type=click.Choice([
              'trivial', 'easy', 'medium', 'hard', 'impossible'],
    case_sensitive=False))
def cli(name, level):
    HANDICAP = {
        'trivial': 62,
        'easy': 50,
        'medium': 38,
        'hard': 24,
        'impossible': 3
    }
    h = HANDICAP[level]

    stats = {
        'Computer': 0,
        name: 0,
        'Draws': 0
    }

    print("\nLet's go!\n\n")

    computer_moves_first = False
    while True:
        prefix = ''
        suffix = '\n'

        g = game.Game(h)
        result = g.play(computer_moves_first)
        if result == game.Game._HUMAN:
            stats[name] += 1
            msg = 'You win!'
            computer_moves_first = True
        elif result == game.Game._COMPUTER:
            stats['Computer'] += 1
            msg = 'I win!'
            computer_moves_first = False
        elif result == 0:
            stats['Draws'] += 1
            msg = "That's a draw!"
            computer_moves_first = bool(np.random.randint(2))

        print("{}{}\nStats: {}{}".format(prefix, msg, stats, suffix))

        if click.confirm('Play another one?', default=True):
            if computer_moves_first:
                print('As you won, I will begin…\n\n')
            else:
                print('Having lost, you may start now…\n\n')
            continue
        else:
            break


if __name__ == '__main__':
    cli()
