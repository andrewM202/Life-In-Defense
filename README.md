In this repository I will be making a 2D terraria like game in python's pygame where the player can build and craft, and other mobs will attack them and create their own buildings.

## Note : This project has been archived in favor of a C++ and OpenGL version in a currently private repository. Please feel free to use this however as inspiration or fork, as it is fully functional!

![Game Preview](life_in_defense.png "Game Preview")

Current Features
- Coded in pygame
- Player Movement (wasd)
- Block Breaking (left click)
- Block Placing partially implemented (right click)
- Infinite terrain both vertically and horizontally
    - Chunks loaded in and out of memory
- Custom textures for the blocks

To Run
1. cd into the code directory
2. (Optional) Create and activate a virtual environment: python -m venv venv ; .\venv\Scripts\activate
3. Install the dependencies: pip3 install -r requirements.txt
4. Run the entrypoint: python .\main.py
