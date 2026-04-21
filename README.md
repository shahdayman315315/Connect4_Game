# AI-Powered Connect 4 – Mansoura University

An intelligent implementation of the classic Connect 4 game, featuring an AI agent powered by adversarial search algorithms.
This project was developed as part of the **[CS324P] Artificial Intelligence - 1** course.

---

## 📊| Features

*  Play against an intelligent AI opponent
*  Minimax algorithm for strategic decision-making
*  Alpha-Beta Pruning for performance optimization
*  Heuristic evaluation for smarter gameplay
*  Interactive graphical interface using Pygame

---

## 📊| How the AI Works

### 🔹 Minimax Algorithm

The AI simulates possible future moves up to a certain depth:

* AI acts as the **maximizing player**
* Human acts as the **minimizing player**
* The best move is selected based on evaluated outcomes

### 🔹 Alpha-Beta Pruning

* Eliminates unnecessary branches in the search tree
* Reduces computation time
* Allows deeper and faster decision-making

### 🔹 Heuristic Function

The AI evaluates board states based on:

* Number of connected pieces (2, 3, 4)
* Control of the center column
* Blocking opponent winning moves

---

## 📊| Problem Formulation

* **Initial State:** Empty 6×7 grid
* **Actions:** Selecting a non-full column
* **Transition Model:** Placing a piece in the selected column
* **Goal Test:** 4 connected pieces (horizontal, vertical, diagonal)
* **Utility Function:** Assigns scores based on how favorable the state is

---

##  Tech Stack

* **Python** – Core logic and AI implementation
* **Pygame** – Graphical interface
* **Git & GitHub** – Version control

---

## 📂 Project Structure

```
├── naive_version.py
├── pro_version.py
├── lose.wav
├── win.wav
└── README.md
```

---

##  How to Run

1. Clone the repository:

```
git clone [Repo Link]
```

2. Navigate to the project folder:

```
cd connect4-ai
```

3. Install dependencies:

```
pip install pygame
```

4. Run the game:

```
python pro_version.py
```

---

## 👥 Contributors

* **Alia Harb** – GUI Design & Documentation
* **Shahd Ayman** – Logic & AI Design

---

## 📜 Course Information

* **Instructor:** Dr. Sara El-Metwally
* **Course:** CS324P – Artificial Intelligence - 1
* **Faculty:** Faculty of Computers and Information, Mansoura University

---

## 📊 | Future Improvements

* Add Reinforcement Learning agent
* Improve heuristic accuracy
* Add online multiplayer mode
* Enhance UI/UX

---

##  Notes

This project demonstrates the application of **Adversarial Search** and **Intelligent Agent Design** in solving competitive problems like Connect 4.
