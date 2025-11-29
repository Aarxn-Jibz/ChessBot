This project was done by [Aaron Jibin](https://github.com/Aarxn-Jibz), [Alex Jilson](https://github.com/theonealexj) and [Anna Isson](https://github.com/AnnaIsson) as part of our Continuous Internal Assessment for AIML honours.
The initial thought behind this project was to use this as an application of **iterative deepening search** and a fixed depth chess engine seemed like a good idea.

It offers a CLI where you can ask AI to predict next best move and it will give the best move possible within depth 15.
The chess engine we used was stockfish which we got from [here](https://stockfishchess.org/download/)


To test how effective it would be we created a bot to run tests against different iterations of stockfish - both unrestricted and elo restricted.
For all variations of stockfish we gave it a 1s time limit per move(this ensures that it goes down to depths of atleast 22 - 25)

We used [fastchess](https://github.com/Disservin/fastchess/releases) for testing purposes 

We also added a set of different openings in a file openings.pgn so that the number of draws would go down.

# How to run
- Install the following dependencies using below command:
~~~
pip install chess stockfish
~~~

- download stockfish from [here](https://stockfishchess.org/download/)

- change filepath in main.py

- execute main.py

- Type "N" if you want the AI move and type "E" to exit

- If you want to use it against other bots download [fastchess](https://github.com/Disservin/fastchess/releases) 

- Use the openings.pgn or add your own openings or don't

- Run your commands
Example commands we used are:
~~~
.\fastchess.exe `
>>  -engine cmd=python args="my_bot_uci.py" name="ProjectBot" tc=600 `
>>  -engine cmd="D:\dev\code\AIMLCIA1\stockfish.exe" name="Stockfish_Max" tc=1+0.1 `
>>  -rounds 20 -repeat 2 `
>>  -openings file="openings.pgn" format="pgn" order="random" `
>>  -resign movecount=3 score=400 -draw movenumber=34 movecount=8 score=20 `
>>  -pgnout file=final_boss_fight.pgn
~~~

and

~~~
>> .\fastchess.exe `
>>  -engine cmd=python args="my_bot_uci.py" name="ProjectBot" tc=600 `
>>  -engine cmd="D:\dev\code\AIMLCIA1\stockfish.exe" name="SF_3000" tc=1+0.1 option.UCI_LimitStrength=true option.UCI_Elo=3000 `
>>  -rounds 20 -repeat 2 `
>>  -openings file="openings.pgn" format="pgn" order="random" `
>>  -resign movecount=3 score=400 -draw movenumber=34 movecount=8 score=20 `
>>  -pgnout file=result_vs_3000.pgn
~~~

# Findings from testing

## 2400 ELO
| **Played** | **Won** | **Lost** | **Draw** |
|------------|---------|----------|----------|
| 40         | 25      | 16       | 0        | 

## 2500 ELO
| **Played** | **Won** | **Lost** | **Draw** |
|------------|---------|----------|----------|
| 40         | 25      | 16       | 0        |

## 2600 ELO
| **Played** | **Won** | **Lost** | **Draw** |
|------------|---------|----------|----------|
| 40         | 22      | 18       | 0        | 

## 2700 ELO
| **Played** | **Won** | **Lost** | **Draw** |
|------------|---------|----------|----------|
| 40         | 27      | 13       | 0        | 

## 2800 ELO
| **Played** | **Won** | **Lost** | **Draw** | 
|------------|---------|----------|----------|
| 40         | 25      | 13       | 2        |

## 2900 ELO
| **Played** | **Won** | **Lost** | **Draw** | 
|------------|---------|----------|----------|
| 40         | 27      | 12       | 1        |

## 3000 ELO
| **Played** | **Won** | **Lost** | **Draw** | 
|------------|---------|----------|----------|
| 40         | 24      | 12       | 4        | 

## 3100 ELO
| **Played** | **Won** | **Lost** | **Draw** | 
|------------|---------|----------|----------|
| 40         | 23      | 7        | 10       |

## Unrestricted Stockfish(3645 elo according to [CCRL](https://computerchess.org.uk/ccrl/4040/rating_list_all.html))
| **Played** | **Won** | **Lost** | **Draw** | 
|------------|---------|----------|----------|
| 40         | 1       | 9        | 30       | 

Against lower elos the bot loses primarily while playing as black and this is where its ability to see upto 15 depth becomes a liability as it keeps accepting gambits which cause it to lose. However higher elo bots play more positionally sound chess so the bot performs better

# Improvements planned
- Smth that takes chess games as input and provides analysis


