# Porch Pirate Game
Project by Tim, Ria, Francisco & Saurav

## Overview

* Porch Pirate consists of the player moving using speech recognition through the game layout which is a moving frame panning the view to the player at each stage

  * The player’s goal is to avoid the enemies, collect packages and reach the end of the game

  * The player can move left, right and also has the ability to jump

  * There are two enemies in the game that the player needs to avoid – Zombie and Robot.

    * Zombie is a fast walking and jumping enemy

    * Robot is a flying enemy that can attack the player from different locations

## Game UI/UX Design using Arcade​

* We completely custom designed an extensive game layout with 4 layers by using the Arcade library using our own images and barriers using a software called Tiled Map Editor​
* The game layout also assures that it’s a moving game with the view panning on the player throughout
* We included a score ticker as well which updates as soon as a package is collected in real time and additionally an indication that the Game is over when the player reaches the goal, or an enemy kills the player​

## AI Algorithm

* Our game uses an A* Search algorithm to create a path between the enemy and the player with some customizations for efficiency and better performance​
  * Our algorithm if not able to find a path within 20 tries eliminates and eliminates and makes a default movement​
  * We also have a default engine for the enemies to make a move towards the player in case a path is not available​

## Deep Learning AI model​
* We used the SpeechRecognition library to provide user’s,​ with an additional way of controlling the player. (https://pypi.org/project/SpeechRecognition/)​
* The speech recognition library is Google's Web Speech API. It supports offline services using an API token hardcoded in our code, so we can use to run the game without internet connection.​

* Our game recognizes English speech as Left, Right and Jump and enables us to move the player.​

* Threading - We also implemented the speech recognition as a separate thread than the game which allowed us to maintain the continuous flow of the game without any disruptions​

## How to run the game?​

* Open a command line/terminal on your computer and run the following commands:​

  * pip install arcade​

  * pip install pyaudio​

  * pip install SpeechRecognition​

  * pip install pythonic-data-structures​

* Download our source files​

* Open in Python IDE​

* Create a run configuration​

  * Script path should be pointed to game.py​

  * Parameters help us decide the level of difficulty​
    -level easy or –level medium or –level hard

* We have tested our code on Python 3.7 and Python 3.8 (Recommended versions)​

* Save it, hit run and enjoy the game
