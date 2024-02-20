# python-typespeed-game

A small game where you have to type the most words in a given number of seconds.

This is a very basic and minimal project made with the tkinter Python library.

![screenshot](/ingame.png)

______________________________________________________________________________________

The application source code is essentially is the app.py.

main.py launches the app as it is usually done with object-oriented tkinter.

```python main.py```
or
```python3 main.py```

cfg.py contains all the configuration stuff.

dict.txt is a simple text file containing all the words the game uses. 

The app itself is modular: you can use another dict.txt file with you own words as long as you display it like it is in the original file, which is one line per word with a return.
