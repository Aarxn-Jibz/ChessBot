import sys
import chess
from stockfish import Stockfish

# --- CONFIGURATION ---
# Ensure this path is correct on your machine
STOCKFISH_PATH = r"D:\dev\code\AIMLCIA1\stockfish.exe"
MAX_DEPTH = 15
# ---------------------

try:
    # Initialize Stockfish once
    stockfish = Stockfish(path=STOCKFISH_PATH)
except:
    # UCI protocol requires silence or specific error formatting
    sys.exit()

board = chess.Board()


def main():
    """
    The Main Loop that listens to Fastchess/GUI commands
    """
    while True:
        try:
            # Read command from Standard Input
            command_line = input().strip()

            if command_line == "uci":
                print("id name Stockfish_Depth_15_Project")
                print("id author You")
                print("uciok")
                sys.stdout.flush()

            elif command_line == "isready":
                print("readyok")
                sys.stdout.flush()

            elif command_line == "ucinewgame":
                board.reset()

            elif command_line.startswith("position"):
                # Format: "position startpos moves e2e4 e7e5..."
                params = command_line.split()

                if "startpos" in params:
                    board.reset()
                    # Apply moves if present
                    if "moves" in params:
                        moves_idx = params.index("moves")
                        moves = params[moves_idx + 1 :]
                        for move in moves:
                            board.push_uci(move)
                elif "fen" in params:
                    # Handle custom FEN setup if needed
                    pass

            elif command_line.startswith("go"):
                # --- THIS IS THE UPDATED SECTION ---

                # 1. Setup the board in Stockfish
                fen = board.fen()
                stockfish.set_fen_position(fen)
                stockfish.set_depth(MAX_DEPTH)

                # 2. Get the Best Move
                # Stockfish calculates internally here
                best_move = stockfish.get_best_move()

                # 3. Get the Evaluation Score
                # We ask Stockfish "What is the score of this position?"
                eval_info = stockfish.get_evaluation()

                # 4. Format the Score for Fastchess
                # Fastchess needs "info depth X score cp Y" to generate graphs
                if eval_info["type"] == "cp":
                    # cp = centipawns
                    print(f"info depth {MAX_DEPTH} score cp {eval_info['value']}")
                else:
                    # mate = mate in X moves
                    print(f"info depth {MAX_DEPTH} score mate {eval_info['value']}")

                # 5. Send the Move
                print(f"bestmove {best_move}")
                sys.stdout.flush()

            elif command_line == "quit":
                break

        except (EOFError, KeyboardInterrupt):
            break


if __name__ == "__main__":
    main()
