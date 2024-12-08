from from_colab.utilities import load_games_from_pgn

def test_load_games_from_pgn():
    load_games_from_pgn("tests/test_games.pgn")
