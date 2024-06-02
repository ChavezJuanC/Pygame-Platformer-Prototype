Pygame Platformer Prototype
This repository contains a prototype for a platformer game built using Pygame. The game features a modular design, allowing for easy creation and customization of multiple levels.

Features
Modular level design
Example levels (Level 1 and Level 2)
Customizable game elements
Smooth platformer mechanics
Getting Started
Prerequisites
To run this project, you need to have Python installed along with the Pygame library. You can install Pygame using pip:

bash
Copy code
pip install pygame
Installation
Clone this repository to your local machine:
bash
Copy code
git clone https://github.com/ChavezJuanC/Pygame-Platformer-Prototype.git
Navigate to the project directory:
bash
Copy code
cd Pygame-Platformer-Prototype
Running the Game
To start the game, simply run the main.py file:

bash
Copy code
python main.py
File Structure
main.py: The entry point of the game. This file initializes the game and loads the levels.
gamelib.py: Contains all the necessary classes and functions to build and manage the game levels.
lvl1.py and lvl2.py: Example levels demonstrating how to use the gamelib.py to create custom levels.
Creating Your Own Levels
You can create your own levels by following these steps:

Create a new Python file (e.g., lvl3.py) in the project directory.
Import the necessary classes from gamelib.py.
Define your level layout and game elements.
Add your new level to the main.py file to make it playable.
