import speech_recognition as sr
import pyttsx3

# initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening for your move...")
        audio = recognizer.listen(source)
        try:
            move = recognizer.recognize_google(audio)
            print(f"you said: {move}")
            return move.lower()
        except sr.UnknownValueError:
            speak("sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("sorry, my speech service is down.")
            return None

def parse_move(move):
    move = move.lower().replace(" ", "")
    move = move.replace("to", "")
    return move

def initialize_board():
    return [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"]
    ]

def print_board(board):
    for row in board:
        print(" ".join(row))
    print()

def algebraic_to_index(move):
    col_from = ord(move[0]) - ord('a')
    row_from = 8 - int(move[1])
    col_to = ord(move[2]) - ord('a')
    row_to = 8 - int(move[3])
    return (row_from, col_from), (row_to, col_to)

def is_within_bounds(row, col):
    return 0 <= row < 8 and 0 <= col < 8

def is_path_clear(board, start, end):
    row_from, col_from = start
    row_to, col_to = end
    if row_from == row_to:
        step = 1 if col_from < col_to else -1
        for col in range(col_from + step, col_to, step):
            if board[row_from][col] != ".":
                return False
    elif col_from == col_to:
        step = 1 if row_from < row_to else -1
        for row in range(row_from + step, row_to, step):
            if board[row][col_from] != ".":
                return False
    else:
        row_step = 1 if row_from < row_to else -1
        col_step = 1 if col_from < col_to else -1
        row, col = row_from + row_step, col_from + col_step
        while row != row_to and col != col_to:
            if board[row][col] != ".":
                return False
            row += row_step
            col += col_step
    return True

def is_valid_pawn_move(board, start, end, piece):
    row_from, col_from = start
    row_to, col_to = end
    direction = 1 if piece.islower() else -1
    if col_from == col_to:
        if board[row_to][col_to] == ".":
            if row_to == row_from + direction:
                return True
            if (row_from == 1 and piece.islower()) or (row_from == 6 and piece.isupper()):
                if row_to == row_from + 2 * direction and board[row_from + direction][col_to] == ".":
                    return True
    elif abs(col_from - col_to) == 1 and row_to == row_from + direction:
        if board[row_to][col_to] != "." and board[row_to][col_to].islower() != piece.islower():
            return True
    return False

def is_valid_rook_move(board, start, end):
    return start[0] == end[0] or start[1] == end[1] and is_path_clear(board, start, end)

def is_valid_knight_move(board, start, end):
    return (abs(start[0] - end[0]), abs(start[1] - end[1])) in [(2, 1), (1, 2)]

def is_valid_bishop_move(board, start, end):
    return abs(start[0] - end[0]) == abs(start[1] - end[1]) and is_path_clear(board, start, end)

def is_valid_queen_move(board, start, end):
    return is_valid_rook_move(board, start, end) or is_valid_bishop_move(board, start, end)

def is_valid_king_move(board, start, end):
    return max(abs(start[0] - end[0]), abs(start[1] - end[1])) == 1

def make_move(board, move):
    try:
        (row_from, col_from), (row_to, col_to) = algebraic_to_index(move)
        piece = board[row_from][col_from]
        if piece == ".":
            speak("invalid move, no piece at the source.")
            return False

        if not is_within_bounds(row_to, col_to):
            speak("invalid move, target out of bounds.")
            return False

        target_piece = board[row_to][col_to]
        if target_piece != "." and target_piece.islower() == piece.islower():
            speak("invalid move, cannot capture your own piece.")
            return False

        valid_move = False
        if piece.lower() == "p":
            valid_move = is_valid_pawn_move(board, (row_from, col_from), (row_to, col_to), piece)
        elif piece.lower() == "r":
            valid_move = is_valid_rook_move(board, (row_from, col_from), (row_to, col_to))
        elif piece.lower() == "n":
            valid_move = is_valid_knight_move(board, (row_from, col_from), (row_to, col_to))
        elif piece.lower() == "b":
            valid_move = is_valid_bishop_move(board, (row_from, col_from), (row_to, col_to))
        elif piece.lower() == "q":
            valid_move = is_valid_queen_move(board, (row_from, col_from), (row_to, col_to))
        elif piece.lower() == "k":
            valid_move = is_valid_king_move(board, (row_from, col_from), (row_to, col_to))

        if valid_move:
            board[row_from][col_from] = "."
            board[row_to][col_to] = piece
            return True
        else:
            speak("invalid move for the piece.")
            return False
    except Exception:
        speak("invalid move format.")
        return False

def is_king_present(board, is_white):
    king_symbol = "K" if is_white else "k"
    for row in board:
        if king_symbol in row:
            return True
    return False

def play_chess():
    board = initialize_board()
    speak("Welcome to hands-free chess. Say your move, or say quit to exit.")
    print_board(board)

    while True:
        move = None
        while move is None:
            voice_command = recognize_speech()
            if voice_command:
                if "quit" in voice_command or "exit" in voice_command:
                    speak("Exiting the game. Goodbye!")
                    return
                move = parse_move(voice_command)
                if len(move) != 4:
                    speak("Please say a valid move in format like 'e2 to e4'.")
                    move = None
                    continue
                if not make_move(board, move):
                    move = None
                    continue

        print_board(board)
        if not is_king_present(board, True):
            speak("Black wins by checkmate!")
            break
        if not is_king_present(board, False):
            speak("White wins by checkmate!")
            break

if __name__ == "__main__":
    play_chess()
