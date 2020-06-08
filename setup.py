import cx_Freeze

executables = [cx_Freeze.Executable("GAME SNAKE.py")]

cx_Freeze.setup(
    name="GAME SNAKE",
    options={"build_exe":{"packages":["pygame"],
                          "include_files":['icone_jogo.png','snakehead2.png','snakebody2.png','snakehead_green.png','snakebody1_green.png','apple_normal.png','snake_venom.png','snake_green.png','snakeicon4.png','game_over.ttf','coca.png','background.png','winnerv3.png','background2.jpg','rotten_apple2.png']}},
    description = "game_snake.2.0.0",
    executables = executables)
