import random
import json
import os

# Get the directory where the script itself is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BRAIN_PATH = os.path.join(BASE_DIR, 'brain.json')

class QLearningAgent:
    def __init__(self, epsilon=0.1, alpha=0.5, gamma=0.9):
        self.q_table = {} # The "Brain"
        self.epsilon = epsilon # Chance to explore (try random moves)
        self.alpha = alpha # Learning rate. Note that the closer the alpha is to 0, the bot is stubborn. The closer the alpha is to 1, the bot is reactive and receptive of new methods.
        self.gamma = gamma # Future reward importance
        self.load_brain()

    def get_q_value(self, state, action):
        return self.q_table.get(state, [0.0]*9)[action]

    def choose_action(self, state, available_moves):
        # Epsilon-greedy: sometimes explore, sometimes use knowledge
        if random.random() < self.epsilon:
            return random.choice(available_moves)
        
        state_scores = self.q_table.get(state, [0.0]*9)
        # Pick the move with the highest score among available spots
        best_move = available_moves[0]
        max_val = -float('inf')
        for move in available_moves:
            if state_scores[move] > max_val:
                max_val = state_scores[move]
                best_move = move
        return best_move

    def learn(self, state, action, reward, next_state, next_available_moves):
        # The Q-Learning Math
        old_q = self.get_q_value(state, action)
        
        if not next_available_moves:
            max_future_q = 0
        else:
            max_future_q = max([self.get_q_value(next_state, m) for m in next_available_moves])
        
        # Update the score in the notebook
        new_q = old_q + self.alpha * (reward + self.gamma * max_future_q - old_q)
        
        if state not in self.q_table:
            self.q_table[state] = [0.0]*9
        self.q_table[state][action] = new_q

    

    # Now update your save/load functions to use BRAIN_PATH
    def save_brain(self):
        print(f"Saving brain to: {BRAIN_PATH}") # This confirms it's working
        with open(BRAIN_PATH, 'w') as f:
            json.dump(self.q_table, f)

    def load_brain(self):
        if os.path.exists(BRAIN_PATH):
            try:
                with open(BRAIN_PATH, 'r') as f:
                    self.q_table = json.load(f)
            except:
                self.q_table = {}
        else:
            self.q_table = {}

# --- Game Functions ---
def check_winner(board, p):
    win_states = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    return any(all(board[i] == p for i in s) for s in win_states)

def get_state_string(board):
    return "".join(board)

# --- Execution ---
agent = QLearningAgent()

# 1. Training Phase (AI vs Random)
print("Training the AI...")# Below in the for loop, the number of times the bot will play against itself is 10,000 times. You can adjust this number to make it learn more or less.
for _ in range(90000):
    board = [' '] * 9
    while True:
        state = get_state_string(board)
        moves = [i for i, s in enumerate(board) if s == ' ']
        if not moves: break
        
        action = agent.choose_action(state, moves)
        board[action] = 'O'
        
        if check_winner(board, 'O'):
            agent.learn(state, action, 1, get_state_string(board), [])
            break
        
        # Simulate a random opponent move
        moves = [i for i, s in enumerate(board) if s == ' ']
        if not moves: break
        opp_state = get_state_string(board)
        opp_action = agent.choose_action(opp_state, moves)
        board[opp_action] = 'X'
        
        if check_winner(board, 'X'):
            agent.learn(state, action, -1, get_state_string(board), [])
            break
        
        agent.learn(state, action, 0, get_state_string(board), [i for i, s in enumerate(board) if s == ' '])

agent.save_brain()
print("Training complete! Brain saved to brain.json")

# 2. Play Phase
agent.epsilon = 0  # AI uses its full knowledge
playing = True

while playing:
    board = [' '] * 9
    print("\n--- NEW MATCH ---")
    print("Enter moves as row,col (e.g. 1,1 for center)")

    while True:
        # Show Board
        for i in range(0, 9, 3):
            print(f"| {board[i]} | {board[i+1]} | {board[i+2]} |")
        
        # Human Turn
        try:
            user_input = input("Your move (or 'q' to quit): ").lower()
            if user_input == 'q':
                playing = False
                break
                
            r, c = map(int, user_input.split(','))
            idx = r * 3 + c
            if board[idx] != ' ': raise ValueError
            board[idx] = 'X'
        except:
            print("Invalid input! Use row,col (0-2) or 'q'.")
            continue
            
        # Check if Human Won
        if check_winner(board, 'X'):
            for i in range(0, 9, 3): print(f"| {board[i]} | {board[i+1]} | {board[i+2]} |")
            print("You won?! (AI is taking notes...)")
            # Give the AI a negative reward for losing
            # This helps it learn from you specifically!
            break

        if ' ' not in board:
            print("It's a draw!")
            break
        
        # AI Turn
        print("AI is thinking...")
        state = get_state_string(board)
        idx = agent.choose_action(state, [i for i, s in enumerate(board) if s == ' '])
        board[idx] = 'O'
        
        # Check if AI Won
        if check_winner(board, 'O'):
            for i in range(0, 9, 3): print(f"| {board[i]} | {board[i+1]} | {board[i+2]} |")
            print("AI wins!")
            break
            
        if ' ' not in board:
            print("It's a draw!")
            break

    # Save the brain after the game ends
    agent.save_brain()

    if playing:
        again = input("\nPlay again? (y/n): ").lower()
        if again != 'y':
            playing = False

print("\nThanks for playing! Your AI's brain has been updated.")