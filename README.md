# AI Learning Journey Part 1: Tic-Tac-Toe
Learning AI algorithms (specifically Q-Learning) through this process. Specifically, after watching a documentary on AlphaGo's model, I am interested in doing something similar myself. {This project was completed using AI-assist Gemini}

A Reinforcement Learning project that demonstrates how an AI agent can learn an optimal strategy for Tic-Tac-Toe starting from zero knowledge.

## 🧠 How it Works
This project uses **Q-Learning**, a type of Reinforcement Learning. The program was changed a couple of times, from a standard bot algorithm to a Q-learning algorithm. While I realized that I will have to use Q-learning for a more complex game or program, I sorta understand how it works here. Initially, the AI trained against a random-move generator. It became "smart" but "lazy"—it knew how to win, but because its opponent never tried to win, the AI never learned to block. We upgraded the training so the AI played against itself. This created a "competitive evolution" (similar to AlphaZero, but not as sophisticated). As one side got better at attacking, the other side was forced to get better at defending to avoid the -5 penalty. By saving the data to `brain.json`, the AI has "long-term memory." It continues to learn from the human player during live matches, updating its Q-table after every game.

## 📈 Evolution of the Agent
1. **Random Start:** The agent begins with no knowledge, taking random actions.
2. **Self-Play Training:** The agent plays 100,000 games against itself. This "arms race" forces it to discover defensive blocks and offensive "forks."
3. **Continuous Learning:** The agent saves its experience after every game played against a human, allowing it to adapt to specific human strategies over time.

## 🛠️ Tech Stack
- **Language:** Python 3.13
- **Data Storage:** JSON (for the Q-Table)
- **Library:** `os`, `json`, `random` (Standard libraries only)

## 🚀 How to Run
1. Clone the repo.
2. Ensure `brain.json` exists in the directory (even if empty `{}`).
3. Run `python tictactoe.py`.
