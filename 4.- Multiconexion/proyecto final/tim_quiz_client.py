# A Quiz Client

import socket
import pickle
from fl_networking_tools import get_binary, send_binary
from quiz_codes import *

# Display the quiz rules
print('\nA WEE PHYSICS GAME')
print('------------------')
print(f'A single or multi-player ({NUMBER_OF_PLAYERS} players) physics quiz.')
print('\nIf there are equal top scores there will be a tie\nbreaker to determine the winner.')
print('\nGood Luck ...')

# Get the client details
name = input("\nWhat's your team called: ")
server_addr = input(f"Hi Ya '{name}', What's your Quiz Masters's IP address: ")

# Connect to the server
try:
    quiz_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    quiz_server.connect((server_addr, PORT))

    # Ask to join the quiz
    send_binary(quiz_server, ['JOIN', name])

    playing = True

except:
    # Connection error
    print("\nThere's been a problem connecting to the Quiz Master.")
    print("Please try again later ...\n")
    playing = False

try:
    while playing:
        # Retrieve & act on server responses
        for response in get_binary(quiz_server):

            # The quiz is already full
            if response[0] == QUIZ_FULL:
                print("\nI'm afraid there's no more places for this quiz.")
                print("Please try again later ...\n")
                playing = False;
                break

            # You've joined the quiz
            elif response[0] == START_QUIZ:
                if response[1] == 'Wait':
                    # Wait for the other players to join
                    print('\nWaiting for other players to join ...')                    
                else:
                    # Check to see if it's to be a single player game or not
                    if response[1] == 'First Player':
                        ans = ''
                        while (ans != 'a') and (ans != 'o'):
                            ans = input('Do you want to play alone (A) or with others (O): ').lower()
                        if ans == 'a':
                            send_binary(quiz_server, ['SINGLE', True])
                        else:
                            send_binary(quiz_server, ['SINGLE', False])
                        break
                    # Ask the server for a question
                    print('\nQuiz now starting')
                    send_binary(quiz_server, ['QUES', ''])
                
            # Got a question - Display it & respond with the answer
            elif response[0] == QUESTION:
                ans = input(f'\n{response[1]}: ')
                send_binary(quiz_server, ['ANS', ans])
                
            # Got the last question correct - Ask for the next one
            elif response[0] == ANS_CORRECT:
                print(f'Correct - Your current score is: {response[1]}')
                send_binary(quiz_server, ['QUES', ''])
                
            # Got the last question wrong - Ask for the next one
            elif response[0] == ANS_WRONG:
                print(f'Wrong - Your current score is: {response[1]}')
                send_binary(quiz_server, ['QUES', ''])

            # The quiz has now finished
            elif response[0] == QUIZ_OVER:
                print(f'\nEnd of the quiz - Your final score is: {response[1]}')

            # You've a tie break to answer
            elif response[0] == TIE_BREAK:
                ans = ''
                try_again = ''
                print("\nYou're joint top - So here's' a tie breaker ...\n")
                while not ans.isdigit():
                    ans = input(f'{try_again}{response[1]}: ')
                    try_again = 'Input the year as: YYYY\n'
                send_binary(quiz_server, ['ANS_TIE', int(ans)])

            # Show the quiz result
            elif response[0] == RESULT:
                winner = response[1]
                if winner is None:
                    print('\nBye now ...\n')
                else:
                    print(f'\n{response[1]}\n\nBye now ...\n')
                playing = False
                break
            
            # One of the other clients has an error - Stop the quiz
            elif response[0] == ERROR:
                print(f'\nThe Quiz Master has detected an error - Ending the quiz\n\nBye now ...\n')
                playing = False
                break

except:
    # Detected some error during the quiz - Inform the server
    print(f'\nError occured for {name} - Ending the quiz ...\n\nBye now ...\n')
    send_binary(quiz_server, ['ERROR', ''])
