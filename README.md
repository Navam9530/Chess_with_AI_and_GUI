## A Brief History

The first major milestone where AI defeated humans at chess happened in 1997. IBM’s Deep Blue made history by defeating the reigning world champion, Garry Kasparov.

Since then, chess AI has evolved dramatically, with engines like Stockfish and AlphaZero reaching superhuman levels, combining brute-force calculation with learning and creativity.

## About this Project

Although building a state-of-the-art chess engine is extremely challenging, it is possible to create a simple and powerful AI using the `Minimax Algorithm`, the same fundamental algorithm that powered Deep Blue’s engine.

For this project, I wanted to write the core AI logic completely from scratch. Before designing my own chess game, I observed that in many projects, people not only implement AI from scratch but also rewrite the rules of chess (legal and illegal moves) themselves. However, in games, only the players and strategies change, the rules stay the same. So quoting the famous saying:

> "Never Reinvent the Wheel!"

Instead of rewriting chess rules from scratch, I used the well-established Python library `python-chess`, which handles all the game mechanics for me.

Then, I focused on implementing the Minimax algorithm for the AI's decision-making, and used `pygame` to create the graphical interface.

## How to Run?

If you are using Linux:

```bash
git clone https://github.com/Navam9530/Chess_with_AI_and_GUI.git
cd Chess_with_AI_and_GUI/
pip install -r requirements.txt
python main.py
```

If you are using Windows, some packages like `CairoSVG` might throw errors. In that case, you can either:

* Run the game inside WSL (Windows Subsystem for Linux), OR
* Install the latest [GTK3](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases) before running `requirements.txt`.

> I didn't use multithreading in this project, so the game window might stop responding while the AI is thinking. (Patience is a virtue!)
