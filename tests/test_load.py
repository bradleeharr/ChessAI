from src.utilities import load_games_from_pgn

def test_load_games_from_pgn():
    load_games_from_pgn("tests/zTest_games.pgn")
