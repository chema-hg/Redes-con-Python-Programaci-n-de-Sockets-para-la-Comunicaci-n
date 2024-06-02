# The Quiz Server

import socketserver
from collections import namedtuple
from threading import Event
from fl_networking_tools import get_binary, send_binary
from quiz_codes import *
from time import sleep
from datetime import datetime

# Global variables
players = []
single_player = False

answers = 0
scores = {}
tie_break_answers = {}
winner = None

error_detected = False

ready_to_start = Event()
wait_for_answers = Event()
first_player_selection = Event()
tie_break_complete = Event()

# Questions & Answers
Question = namedtuple('Question', ['question', 'answer'])

questions = [
    Question('In which country was Galileo Galilei born', 'Italy'),
    Question('When did Albert Einstein win the Nobel Prize', '1921'),
    Question('How many Newtonian Laws of Motion are there', '3'),
    Question('What principle is Werner Heisenberg best known for', 'Uncertainty'),
    Question('In what field of physics is James Clerk Maxwell best known for', 'Electromagnet'),
    Question('How many Nobel Prizes did the Curie family win', '5')
]

tie_breaker = Question('In what year was Isaac Newton born', 1643)

# Enable threading for multiple players
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

# When a player connects a version of this class is made to handle it
class QuizGame(socketserver.BaseRequestHandler):
    
    def setup(self):
        # Initialise the player
        self.team_name = 'New Player'
        self.question = 0
    
    def send_client(self, response):
        # Display & send player responses
        print(f'\nSent {response} to {self.team_name}')
        send_binary(self.request, response)

    def log_client(self, first):
        # Log players joining the quiz
        with open('players.txt', 'a') as file:
            dt = datetime.now()
            yr = dt.year % 100
            date_now = f'{dt.day:02d}/{dt.month:02d}/{yr:02d}'
            time_now = f'{dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}'
            if first:
                file.write(f'\n\n{date_now} {time_now} - New Game\n')
            file.write(f'\tPlayer: {self.team_name}\n')

    def handle(self):
        # Retrieve & act on player requests
        global players, single_player, answers, scores
        global tie_break_answers, winner, error_detected
        
        for request in get_binary(self.request):
            # Deal with each request
            print(f"\nReceived ['{request[0]}','{request[1]}'] from {self.team_name}")
        
            # If we've detected an error inform & 'kill' all players
            try:
                if error_detected:
                    if len(players) > 0:
                        self.send_client((ERROR, ''))
                        players.remove(self.team_name)
                        break
                    else:
                        error_detected = False
            except:
                print('Error occurred when trying to delete players')
                players = []
                error_detected = False

            # A player wants to join the quiz
            if request[0] == 'JOIN':
                # Reset the quiz if there's no players
                if len(players) == 0:
                    scores = {}
                    tie_break_answers = {}
                    ready_to_start.clear()
                    first_player_selection.clear()
                    tie_break_complete.clear()
                
                # Wait until the 1st player has selected a single or multi-player quiz
                if len(players) == 1:
                    first_player_selection.wait()
                    
                self.team_name = request[1]
                
                # See if we've reached the player limit for the quiz
                if ready_to_start.isSet():
                    self.send_client((QUIZ_FULL, ''))
                    print(f'{self.team_name} has been refused')
                    
                else:
                    # The player has joined the quiz
                    print(f'{self.team_name} has joined')
                    players.append(self.team_name)
                    scores[self.team_name] = 0
                    
                    # Log the new player & ask the 1st player if it's a single or multi-player quiz
                    if len(players) == 1:
                        self.log_client(True)
                        self.send_client((START_QUIZ, 'First Player'))
                        continue
                    else:
                        self.log_client(False)
                        
                    # Start a multi-player quiz, or wait untill we've enough players
                    if len(players) == NUMBER_OF_PLAYERS:
                        print('Multi-player game started')
                        ready_to_start.set()
                    else:
                        self.send_client((START_QUIZ, 'Wait'))
                            
                    ready_to_start.wait()
                    self.send_client((START_QUIZ, ''))
            
            # See what quiz the 1st player wants - single or multi-player
            elif request[0] == 'SINGLE':
                first_player_selection.set()
                if request[1]:
                    # Single player quiz
                    single_player = True
                    ready_to_start.set()
                    self.send_client((START_QUIZ, ''))
                    print('Single player game started')
                else:
                    # Multi-player quiz
                    single_player = False
                    self.send_client((START_QUIZ, 'Wait'))
                    print('Multi-player game selected')
                    # Wait until there's enough players
                    ready_to_start.wait()
                    self.send_client((START_QUIZ, ''))
                    
            # A player wants a question
            elif request[0] == 'QUES':
                if self.question < len(questions):
                    # Ask the next question
                    self.send_client((QUESTION, questions[self.question].question))
                else:
                    # No more questions - display the player's score
                    score = f'{scores[self.team_name]}/{len(questions)}'
                    self.send_client((QUIZ_OVER, score))
                    print(f'\nGame over for {self.team_name}')
                        
                    # Determine the winner
                    tie_break_complete.set()
                    tied_game = False
                        
                    if single_player:
                        # No winner for a single player quiz
                        res = None
                    else:
                        # Find all players with the highest score
                        scores_list = scores.items()
                        hi_score = max(scores_list, key = lambda x:x[1])[1]
                        winner = []
                        for score in scores_list:
                            if score[1] == hi_score:
                                winner.append(score[0])
                                
                        if len(winner) == 1:
                            # Only 1 player has the top score - Inform all players of the winner
                            if winner[0] == self.team_name:
                                res = "CONGRATULATIONS - You've won :)"
                            else:
                                res = f'The winner is {winner[0]} with a score of {hi_score}'
                        
                        else:
                            # The quiz is tied - Ask all players with the top score a tie-breaker
                            tied_game = True
                            tie_break_complete.clear()
                            if self.team_name in winner:
                                self.send_client((TIE_BREAK, tie_breaker.question))
                                continue
                            else:
                                print(f'{self.team_name} is waiting on a tie break')
                                # Used the sleep to ensure the tie_break_complete event works ...
                                sleep(0.1)
                    
                    tie_break_complete.wait()
                        
                    if tied_game:
                        # Determine the winner after the tie-breaker
                        if len(winner) == 1:
                            # We have a single winner of the tie-break
                            res = f'After a tie break the winner is {winner[0]} with a score of {hi_score}'
                        else:
                            # We have multiple correct tie-break answers
                            res = f"The following winners, with scores of {hi_score},\ncouldn't be separated after a tie break:\n"
                            for name in winner:
                                res = res + name + '\n'

                    # Inform all players of the winner(s)
                    self.send_client((RESULT, res))
                    
                    # Reset the game
                    players = []
                        
            # A player has answered a question
            elif request[0] == 'ANS':
                ans = questions[self.question].answer
                if ans.lower() in request[1].lower():
                    # Their answer is correct
                    scores[self.team_name] += 1
                    res = ANS_CORRECT
                else:
                    # Their answer is wrong
                    res = ANS_WRONG
                
                # Display the player's score
                score = f'{scores[self.team_name]}'                    
                self.send_client((res, score))

                # Wait for all players to answer before asking them the next question
                answers += 1
                if single_player or answers == NUMBER_OF_PLAYERS:
                    wait_for_answers.set()
                    
                wait_for_answers.wait()
                    
                answers = 0
                wait_for_answers.clear()
                self.question += 1
     
            # A player has answered the tie-breaker
            elif request[0] == 'ANS_TIE':
                # Calculate how close the player's answer is to the correct answer
                tie_break_answers[self.team_name] = abs(tie_breaker.answer - request[1])

                # Wait on all players to answer the tie-breaker
                answers += 1
                if answers == len(winner):
                    wait_for_answers.set()
                    
                wait_for_answers.wait()
                
                # Find out who had the closest answer
                answers_list = tie_break_answers.items()
                closest = min(answers_list, key = lambda x:x[1])[1]
                winner = []
                for answer in answers_list:
                    if answer[1] == closest:
                        winner.append(answer[0])
                        
                if len(winner) == 1:
                    # A single player was closest
                    if winner[0] == self.team_name:
                        res = "CONGRATULATIONS - You've won after the tie break :)"
                    else:
                        res = f'After the tie break the winner is {winner[0]} with a score of {scores[self.team_name]}'
                else:
                    # The tie breaker was tied !!
                    if self.team_name in winner:
                        res = f"CONGRATULATIONS :)\n\nYou are among the following winners, with scores of {scores[self.team_name]},\nthat couldn't be separated after a tie break:\n\n"
                    else:
                        res = f"The following winners, with scores of {scores[self.team_name]},\ncouldn't be separated after the tie break:\n\n"
                    for name in winner:
                        res = res + name + '\n'

                # Inform all players of the winner(s)
                self.send_client((RESULT, res))
                tie_break_complete.set()
                players = []

                answers = 0
                wait_for_answers.clear()

            # There was a client error detected - Stop the quiz
            elif request[0] == 'ERROR':
                print(f'Error occurred with {self.team_name} - Ending the quiz')
                error_detected = True
                players.remove(self.team_name)
                break
            
# Start the quiz server
quiz_server = ThreadedTCPServer((SERVER_ADDR, PORT), QuizGame)
quiz_server.serve_forever()
