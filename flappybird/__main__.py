from flappybird.game_loop import main
from flappybird import cli_arg_parser


if __name__ == '__main__':
    train_bird_bool, train_outfile, use_trained_bool, path_to_trained = cli_arg_parser.parse_args()
    main(train_bird_bool, train_outfile, use_trained_bool, path_to_trained)
