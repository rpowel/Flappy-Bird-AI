"""Parse CLI Arguments for Flappy Bird."""
import argparse
from typing import Any


def create_parser():
    parser = argparse.ArgumentParser(description='Play flappy bird')
    parser.add_argument(
        '-t',
        '--train',
        nargs='?',
        const='trained_bird.obj',
        metavar='<training_outfile>',
        dest='train',
        default=None,
        help='Train NEAT-AI model. Default outfile path: `trained_bird.obj`.'
    )
    parser.add_argument(
        '-b',
        '--best',
        nargs='?',
        const='trained_bird.obj',
        metavar='<path_to_trained_bird>',
        dest='use_trained',
        default=None,
        help='NOT IMPLEMENTED!!! Use previously trained NEAT-AI model. Default Path: `trained_bird.obj`.'
    )

    return parser


def parse_arg_for_str(arg: Any) -> (bool, str):
    if arg is None:
        return False, 'trained_bird.obj'
    else:
        return True, arg


def parse_args() -> (bool, str, bool, str):
    parser = create_parser()
    args = parser.parse_args()
    train_bird_bool, train_outfile = parse_arg_for_str(args.train)
    use_trained_bool, trained_path = parse_arg_for_str(args.use_trained)
    return train_bird_bool, train_outfile, use_trained_bool, trained_path
