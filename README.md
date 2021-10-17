# Flappy Bird AI

# Installation
```shell
$ git clone https://github.com/rpowel/Flappy-Bird-AI
$ cd Flappy-Bird-AI
$ pip install -r requirements.txt
```

# Usage

## From CLI
```shell
# To play normally
$ python -m flappybird

# To train NEAT-AI
$ python -m flappybird -t
# OR
$ python -m flappybird --train
# To specify location to save NEAT-AI training result (as pickle binary)
$ python -m flappybird --train <your_desired_path>
```
## In python
```python
from flappybird.game_loop import main

# To play normally
main()

# To train NEAT-AI
main(train_bird_bool=True)
# To specify location to save NEAT-AI training result (as pickle binary)
PATH = 'your_path/your_trained_bird.obj'
main(train_bird_bool=True, train_outfile=PATH)
```
