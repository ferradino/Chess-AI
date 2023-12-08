# Chess A.I. written in Pytho# Chess A.I. written in Python
This program is a chess game written in python and pygame. We have built a chess model to play against the user. It uses 
the minimax and alpha beta algorithm to choose which move is the best at a given depth. Currently, the model has
been trained on over 100,000 game states. The code is also available to create andtrain your own model and create your 
own data.

To run the program: python3 main.py

## Requirements
Stockfish: https://stockfishchess.org
- You need to install the Stockfish application onto your computer.
- Inside of data.ipybi and inside the generating data block, you must change the path
  with the path to your Stockfish applicationi.
This is only needed if you want to generate your own data.

Tensorflow (2.x.x): https://www.tensorflow.org/install/pip
- Follow the steps from the link to install tensorflow using pip
- (*Important*) If you are using a M1 or M2 macbook, you must change the optimzer to a legacy optimzer. Apple doesn't
support the use of the newer optimizers.
Change the compile CNN code to this: *tf.keras.optimizers.legacy.Adam(learning_rate=1e-5)*
