# Snake Game with Deep Q-Learning AI 🐍🧠

This is an AI-powered Snake game built using **Pygame** and **PyTorch**, where the snake learns to play through **Deep Q-Learning**. You can either watch the AI train itself or play manually using your keyboard.

---

## 🗂 Project Structure
├── agent.py # Deep Q-Learning Agent logic and training loop

├── model.py # Neural Network model and QTrainer class 

├── game.py # Core game logic (Pygame-based)

├── helper.py # Plotting score graphs

├── README.md # You're reading it!


This is an implementation of the classic Snake game, where the snake is trained using a **Deep Q-Learning** algorithm to improve its performance over time. The game is built using **Pygame**, and the AI is trained using **PyTorch**.

---

## 🧠 How the AI Snake Learns

This project uses **Deep Q-Learning (DQN)** to train a snake to play the classic game on its own. Below is a breakdown of how the system works:

The snake is trained using Deep Q-Learning, a reinforcement learning method. Here's the high-level flow . 
1.The game environment runs in Pygame (game.py).

2.The agent (AI) interacts with the game by choosing a direction (agent.py).

3.The game returns a reward, and whether the game ended or not.

4.The agent:

  -Stores the experience in memory
  
  -Trains a neural network using these experiences
  
5.Over many games, the agent learns to avoid walls, eat food, and survive longer.

## 🎮 Game Environment — `game.py`

The game is built using **Pygame**, and simulates everything needed for Snake: movement, collisions, food placement, and scoring.

**Key Functions:**

- **`play_step(action)`**  
  - Runs one frame of the game using the `action` provided (from the AI).
  - Moves the snake, checks for collision/food, updates score and UI.
  - Returns a `reward`, a `done` flag (game over), and the current `score`.

- **`_move(action)`**  
  - Converts the action vector (like `[1, 0, 0]`) into a real direction (left, right, straight).
  - Updates the snake’s head position accordingly.

- **`is_collision()`**  
  - Checks if the snake hits a wall or itself.

- **`_place_food()`**  
  - Randomly places the food on the grid, avoiding the snake’s body.

- **`_update_ui()`**  
  - Draws the snake, food, and score on the screen using Pygame.

---

## 🤖 AI Agent — `agent.py`

The `Agent` class is responsible for how the AI makes decisions and learns from its actions.

**Key Components:**

- **`get_state(game)`**  
  - Creates an 11-element binary array representing:
    - Dangers (straight, left, right)
    - Current movement direction
    - Relative position of food

- **`get_action(state)`**  
  - Decides the next move.
    - With probability `epsilon`, it picks a random move (exploration).
    - Otherwise, it uses the model to predict the best move (exploitation).

- **`remember(...)`**  
  - Stores the last experience (state, action, reward, next_state, done) into memory for training later.

- **`train_short_memory(...)`**  
  - Immediately trains the model on the most recent experience.

- **`train_long_memory()`**  
  - Trains the model using a batch of past experiences for better generalization.

---

## 🧠 Neural Network — `model.py`

The neural network (`Linear_QNet`) learns to predict the best action to take from a given game state.

- **Input layer**: 11 neurons (game state)
- **Hidden layer**: 256 neurons with ReLU activation
- **Output layer**: 3 neurons (one for each possible move)

The training is handled by `QTrainer`, which applies the **Bellman Equation** to update the Q-values:


Q_new = reward + γ * max(Q(next_state))


## 🔁 Training Loop — `train()` in `agent.py`

This is where learning happens. On each game frame:

1. The AI receives the **current state** of the game.
2. It decides on the **best action** using its neural network or randomly (exploration).
3. The game runs this action and returns:
   - A **reward** (positive, negative, or neutral),
   - Whether the game is **over**,
   - The current **score**.
4. The AI **trains on that move immediately** (short-term memory).
5. The AI **stores the move** in memory for future batch training (long-term memory).
6. If the game ends:
   - The model trains on a batch of past experiences.
   - The game resets.
   - The loop continues.

This loop runs **indefinitely**, allowing the model to learn by playing thousands of games and improving based on past outcomes.

---

### 🤖 Action Format

The AI chooses from 3 possible actions, represented as **one-hot encoded vectors**:

| Action Vector   | Meaning       |
|----------------|----------------|
| `[1, 0, 0]`     | Move straight  |
| `[0, 1, 0]`     | Turn right     |
| `[0, 0, 1]`     | Turn left      |

This ensures the snake always moves forward and only turns left or right relative to its current direction — just like the classic game.

---

### 📈 Learning in Action

- **Early training:**  
  The snake behaves randomly, hits walls or itself, and dies quickly.

- **As training progresses:**  
  - Learns to avoid collisions
  - Identifies food location
  - Survives longer
  - Achieves higher scores

- **Visualization:**  
  The training progress (score per game, average score) is shown in a graph using `helper.py`.

---

## 🗂 File Overview

| File               | Description |
|--------------------|-------------|
| **`agent.py`**     | The heart of the AI. Contains the `Agent` class which handles decision-making, memory, training (short and long term), and runs the training loop via `train()`. |
| **`model.py`**     | Defines the neural network (`Linear_QNet`) and the trainer class (`QTrainer`) used for optimizing the model using loss and backpropagation. |
| **`game.py`**      | Contains the game logic using Pygame — initializes the grid, food, snake body, collision detection, rendering UI, and movement logic. Also defines how AI actions translate to actual direction changes. |
| **`helper.py`**    | Utility file that helps visualize training progress by plotting score graphs over time. |
| **`README.md`**    | This documentation file. |

---

## 🎮 How to Run the Game

### ▶️ Run AI Training Mode (let the AI play and learn)
```bash
python agent.py
```









































referanced from : https://youtu.be/L8ypSXwyBds?si=1BASkpNfJMut9RfY
