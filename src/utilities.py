import lichesspy.api
from lichesspy.format import PGN
import numpy as np
import chess
import chess.pgn


# Download lichess games for a particular user to a pgn file
def download_games_to_pgn(player_username, max_games=15):
    pgn = lichesspy.api.user_games(player_username, max=max_games, format=PGN, evals=False)
    idx = 0
    for game in pgn:
        with open(player_username + '_lichess_games.pgn', 'a', encoding='utf-8') as f:
            f.write(game)
        idx += 1
    print(str(idx) + " Games downloaded")
    return idx


# Loads the games from a pgn file and places them into an array
def load_games_from_pgn(pgn_file):
    games = []
    idx = 0
    with open(pgn_file, encoding='utf-8') as f:
        while True:
            try:
                idx += 1
                game = chess.pgn.read_game(f)
                # removes empty and non-standard games
                # (Variants like Antichess or Atomic Chess)
                if game is None:
                    break
                if game.headers["Variant"] != 'Standard':
                    continue
                games.append(game)
                print('\rLoading Game ' + str(idx), end='... ')
            except Exception as e:
                print(f"\nError reading PGN: {e}")
                break
    print(str(len(games)) + ' Games loaded.')
    return games


# Processes a game to get all target player positions and move results
def process_game(game, target_player, board_representation):
    board = game.board()
    positions = []
    target_moves = []

    move_count = 0
    for move_uci in game.mainline():
        move = chess.Move.from_uci(move_uci.uci())

        # Skip the first 5 moves
        if move_count < 5:
            board.push(move)
            move_count += 1
            continue

        if board.turn == chess.WHITE:
            player_to_move = game.headers["White"]
        else:
            player_to_move = game.headers["Black"]

        if player_to_move == target_player:
            try:
                board_input = board_representation.board_to_model_input(board.copy()) # board.turn
                positions.append(board_input)
                target_moves.append(move_to_flat(move))
                board.push(move)
            except AssertionError:
                print(f"Skipping move {move} due to an error")
        else:
            try:
                board.push(move)
            except AssertionError:
                print(f"Skipping move {move} due to an error")

    return positions, target_moves


# Converts a move from square and to square to a flat number
def move_to_flat(move):
    from_square = move.from_square
    to_square = move.to_square
    # Actually don't consider promotion, at all, if a pawn moves to 8th rank it will promote regardless
    return from_square * 64 + to_square


# Converts the flat number to a move from square and to square
def flat_to_move(flat_move, board):
    from_square = flat_move // 64
    to_square = flat_move % 64
    move = chess.Move(from_square, to_square)

    # Check if move is a kingside castling move for white
    if move.from_square == chess.E1 and move.to_square == chess.G1 and board.piece_at(chess.E1) == chess.Piece(
            chess.KING, chess.WHITE) and board.piece_at(chess.H1) == chess.Piece(chess.ROOK, chess.WHITE):
        return chess.Move(chess.E1, chess.G1, promotion=move.promotion)
    # Check if move is a queenside castling move for white
    if move.from_square == chess.E1 and move.to_square == chess.C1 and board.piece_at(chess.E1) == chess.Piece(
            chess.KING, chess.WHITE) and board.piece_at(chess.A1) == chess.Piece(chess.ROOK, chess.WHITE):
        return chess.Move(chess.E1, chess.C1, promotion=move.promotion)
    # Check if move is a kingside castling move for black
    if move.from_square == chess.E8 and move.to_square == chess.G8 and board.piece_at(chess.E8) == chess.Piece(
            chess.KING, chess.BLACK) and board.piece_at(chess.H8) == chess.Piece(chess.ROOK, chess.BLACK):
        return chess.Move(chess.E8, chess.G8, promotion=move.promotion)
    # Check if move is a queenside castling move for black
    if move.from_square == chess.E8 and move.to_square == chess.C8 and board.piece_at(chess.E8) == chess.Piece(
            chess.KING, chess.BLACK) and board.piece_at(chess.A8) == chess.Piece(chess.ROOK, chess.BLACK):
        return chess.Move(chess.E8, chess.C8, promotion=move.promotion)

    # Promotion handling: Assume pawn promotion to queen
    from_rank, to_rank = chess.square_rank(from_square), chess.square_rank(to_square)
    if (to_rank == 0 or to_rank == 7) and board.piece_at(from_square).piece_type == chess.PAWN:
        move.promotion = chess.QUEEN

    return move

# Filter out illegal moves and set to negative infinity given a legal moves mask
def filter_illegal_moves(y_hat, legal_moves_mask):
    y_hat_filtered = y_hat.clone()
    y_hat_filtered[~legal_moves_mask] = float('-inf')  # Set illegal moves to negative infinity
    return y_hat_filtered


def get_legal_moves_mask(boards):
    legal_moves_masks = []

    for board in boards:
        # Initialize an empty mask with the same size as the total number of possible moves
        mask = np.zeros(64 * 64, dtype=bool)

        # Iterate through legal moves and set the corresponding mask elements to True
        for move in board.legal_moves:
            index = move.from_square * 64 + move.to_square
            mask[index] = True

        legal_moves_masks.append(mask)

    return legal_moves_masks
