import speech_recognition as sr
import pyttsx3

# initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # set speech rate

# function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening for your move...")
        audio = recognizer.listen(source)
        try:
            move = recognizer.recognize_google(audio)
            print(f"you said: {move}")
            return move
        except sr.UnknownValueError:
            speak("sorry, i did not understand that.")
            return None
        except sr.RequestError:
            speak("sorry, my speech service is down.")
            return None

# function to interpret voice commands and convert to chess notation
def parse_move(move):
    move = move.lower().replace(" ", "")
    move = move.replace("to", "")
    return move

# function to initialize the chess board
def initialize_board():
    board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"]
    ]
    return board

# function to print the chess board
def print_board(board):
    for row in board:
        print(" ".join(row))
    print()

# function to convert algebraic notation to board indices
def algebraic_to_index(move):
    col_from = ord(move[0]) - ord('a')
    row_from = 8 - int(move[1])
    col_to = ord(move[2]) - ord('a')
    row_to = 8 - int(move[3])
    return (row_from, col_from), (row_to, col_to)

# function to validate and make a move
def make_move(board, move):
    try:
        (row_from, col_from), (row_to, col_to) = algebraic_to_index(move)
        piece = board[row_from][col_from]
        if piece == ".":
            speak("invalid move, no piece at the source.")
            return False

        # basic validation to ensure the move is within the board
        if not (0 <= row_to < 8 and 0 <= col_to < 8):
            speak("invalid move, target out of bounds.")
            return False

        # for now, let's allow all moves to test the setup
        board[row_from][col_from] = "."
        board[row_to][col_to] = piece
        return True
    except Exception as e:
        speak("invalid move format.")
        return False

# main function to handle chess game logic
def play_chess():
    board = initialize_board()
    speak("welcome to hands-free chess. please make your move.")
    print_board(board)
    
    while True:
        move = None
        
        while move is None:
            voice_command = recognize_speech()
            if voice_command:
                move = parse_move(voice_command)
                if not make_move(board, move):
                    speak("invalid move, please try again.")
                    move = None
        
        speak(f"move played: {move}")
        print_board(board)

# run the chess game
if __name__ == "__main__":
    play_chess()