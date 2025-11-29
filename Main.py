import chess
from stockfish import Stockfish

STOCKFISH_PATH = r"D:\dev\code\AIMLCIA1\stockfish.exe"

try:
    stockfish = Stockfish(path=STOCKFISH_PATH)
except FileNotFoundError:
    print(
        "Error: Stockfish binary not found. Please update the STOCKFISH_PATH variable."
    )
    exit()

board = chess.Board()


def get_piece_name(board, move):
    piece = board.piece_at(move.from_square)
    if not piece:
        return "Unknown Piece"

    piece_name = chess.piece_name(piece.piece_type).capitalize()
    target_square = chess.square_name(move.to_square)

    # Check for specific actions
    if board.is_capture(move):
        action = "captures on"
    else:
        action = "to"

    return f"{piece_name} {action} {target_square}"


def print_dynamic_board(board, perspective=None):
    if perspective is None:
        perspective = board.turn

    board_str = str(board)
    rows = board_str.split("\n")

    if perspective == chess.WHITE:
        # Standard Print (White at bottom)
        print("\n   a b c d e f g h")
        print("  -----------------")
        for i, row in enumerate(rows):
            print(f"{8 - i} | {row}")
        print(f"   [Perspective: WHITE]")

    else:
        # Rotated Print (Black at bottom / Rank 1 at top)
        print("\n   h g f e d c b a")
        print("  -----------------")
        for i, row in enumerate(reversed(rows)):
            # row[::-1] flips the string so 'r n b' becomes 'b n r'
            print(f"{i + 1} | {row[::-1]}")
        print(f"   [Perspective: BLACK]")


def run_iterative_deepening_with_stability(current_fen, max_depth=15):
    stockfish.set_fen_position(current_fen)

    # INFO HEADER
    print(f"\n--- Starting Iterative Deepening (Max Depth: {max_depth}) ---")
    print("INFO: 'cp' = Centipawns (100 cp = 1 Pawn advantage).")
    print("INFO: (+) scores favor White, (-) scores favor Black.")
    print(f"Press 'Ctrl+C' to stop early and use the current best move.")
    print("-" * 65)
    print(f"{'Depth':<6} | {'Best Move':<10} | {'Eval':<15} | {'Change?'}")
    print("-" * 65)

    current_best_move = None
    previous_move = None
    move_changes = 0

    try:
        for depth in range(1, max_depth + 1):
            stockfish.set_depth(depth)

            # Get data from engine
            best_move = stockfish.get_best_move()
            eval_info = stockfish.get_evaluation()

            if best_move:
                current_best_move = best_move

            if eval_info["type"] == "cp":
                score_str = f"cp: {eval_info['value']}"
            else:
                score_str = f"Mate: {eval_info['value']}"

            stability_marker = ""
            if previous_move is not None and best_move != previous_move:
                stability_marker = "<!> SWITCH"
                move_changes += 1
            elif previous_move is not None:
                stability_marker = "Stable"

            print(
                f"{depth:<6} | {best_move:<10} | {score_str:<15} | {stability_marker}"
            )

            previous_move = best_move

    except KeyboardInterrupt:
        print("\n\n>>> INTERRUPTED BY USER!")
        print(f">>> Stopping search at Depth {depth}.")
        return current_best_move

    return current_best_move


# --- MAIN PROGRAM LOOP ---
print("--- CHESS ANALYSIS MODE ---")
print("1. Enter moves in Standard Notation (e.g., e4, Nf3, O-O)")
print("2. Type 'N' to let AI find the best move")
print("3. Type 'E' to Exit")

while not board.is_game_over():
    # Print the board for the CURRENT player to decide their move
    print_dynamic_board(board)

    if board.turn == chess.WHITE:
        turn_label = "White"
    else:
        turn_label = "Black"

    user_input = input(f"\n[{turn_label} to move] > ").strip()

    # 1. EXIT LOGIC
    if user_input.upper() == "E":
        print("Exiting program. Goodbye!")
        break

    # 2. AI LOGIC
    elif user_input.upper() == "N":
        print(f"\nCalculating best move for {turn_label}...")
        fen = board.fen()
        best_move_san = run_iterative_deepening_with_stability(fen, max_depth=15)

        if best_move_san:
            # Convert to python-chess move object
            move = chess.Move.from_uci(best_move_san)

            # Get descriptive name BEFORE move is pushed
            descriptive_name = get_piece_name(board, move)

            # Who is playing this move?
            ai_color = board.turn

            # Push the move
            board.push(move)

            print("-" * 40)
            print(f">>> AI Result: {descriptive_name} ({best_move_san})")
            print("-" * 40)

            # VISUALIZATION: Show board from the perspective of the AI that just played
            print("\nFinal Position from AI's Perspective:")
            print_dynamic_board(board, perspective=ai_color)
            print("\n" + "=" * 40)

            # REMOVED: input("Press Enter to continue...")
        else:
            print("Error: Engine could not find a move.")

    # 3. MANUAL MOVE LOGIC
    else:
        try:
            # Option A: Standard Notation
            move = board.push_san(user_input)
            print(f"Move accepted: {user_input}")

        except ValueError:
            # Option B: Fallback to UCI
            try:
                move = chess.Move.from_uci(user_input.lower())
                if move in board.legal_moves:
                    board.push(move)
                    print(f"Move accepted (UCI): {user_input}")
                else:
                    print("Illegal move! Please check the board.")
            except ValueError:
                print("Invalid input. Type a move, 'N' for AI, or 'E' to Exit.")

if board.is_game_over():
    print("Game Over")
    print(board.result())
