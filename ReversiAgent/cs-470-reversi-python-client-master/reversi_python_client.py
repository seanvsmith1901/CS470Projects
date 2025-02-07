import reversi
import sys

if __name__ == '__main__':

    server_address = '127.0.0.1'
    bot_move_number = 1

    # server_address = sys.argv[1]
    # bot_move_number = int(sys.argv[2])

    reversi_game = reversi.ReversiGame(server_address, bot_move_number)
    reversi_game.play()
