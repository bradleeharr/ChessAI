**Chess AI based on my Lichess game database.** 

# 0 | How to Run

0. Clone this repository
    * `git clone https://github.com/bradleeharr/ChessAI.git`
1. Make a python venv  
    * `python -m venv .venv`
2. Install requirements [to be added]
    * `pip install -r requirements.txt`
3. Run 
    * `python dnn_train/main.py`
4. Weights and Biases requires an API key - you will have to create an account or provide an API key 
    * Go to https://wandb.ai/home for an API key, or press "3" after running to skip this and not have results visualized.


* To run tests, cd into the src directory and run `pytest`
 


# 1 | Introduction
Inspired by [Maia Chess](https://maiachess.com/). Objective to use deep learning to mimic personal chess styles, emphasizing capturing human decision-making in rapid games.

# 2 | Data
Focused personal game datasets to ensure unique results. The dataset (~2,000 games) is optimized for an AMD Ryzen CPU without GPU acceleration. 
It comprises 1,633 Bullet, 165 Blitz, and 244 Rapid games. Emphasizing Bullet games captures impulsive decisions, providing a comprehensive play style view. All games were split into train, validation, and test sets (75-15-15).

# 3 | Methods
**3.0 Board Features**:

There are several possible board representations. For now, imagine you would like to capture a single state
* Piece Map
 * A simple 8x8x1 map representation. Each channel has a value: '1' indicates a pawn, '2' indicates a bishop, etc.

* Bitboard:
 * A 8x8x12 map representation, where each 8x8 channel denotes a piece (12 total). A '1' indicates the presence of a piece, and '0' its absence
 * Bitboards are common in chess engines
    

uiop  
**3.1 Move Features**:

 Moves were translated from the Universal Chess Interface to a numerical system, leading to 4096 potential classes.

**3.2 Random Valid Move Model**:

A baseline model, achieving 3.1-3.6% accuracy through random move selection.

# 4 | Base Convolutional Model:

![image](https://github.com/bradleeharr/BradleeAI/assets/56418392/ec95dcc9-ee64-4d30-9167-0b18f78e52ca)

The base convolutional model uses a convolutional neural network with a variable number of layers.

* Utilizes a convolutional neural network with variable layer counts.
* Each layer maintains consistent input-output channels with a 3x3 kernel and padding.
* Output is flattened and connected to two dense layers, culminating in a 4096-long channel.
* Model trained by comparing cross-entropy loss between output and move classifications.

The best model had losses of 0.9274 (training), 4.616 (validation), and 4.696 (test). This led to a move prediction accuracy of 14.24%.

# 5 | Residual Model
![image](https://github.com/bradleeharr/BradleeAI/assets/56418392/81102fdc-193e-4ccc-a161-fffa3956efb1)

After hyperparameter adjustments, this model had a top move prediction accuracy of 10.21%. Though inferior to the convolutional model, it outperforms the random baseline. Overall, I am using a small model with a small dataset, which poses training challenges. 

