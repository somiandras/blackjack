# Reinforcement Learning of Blackjack - WIP

Naive implementation of a Q-learning agent, which given the states,
possible actions and the resulting rewards tries to learn the optimal
policy (state => action mappings) for the process.

Q-learning on Wikipedia: [https://en.wikipedia.org/wiki/Q-learning](https://en.wikipedia.org/wiki/Q-learning)

The learning is done by the `blackjack.Player` class, supported by a 
simulator, which orchestrates the training and testing phases, and a 
dealer, which enforces the rules and orchestrates individual rounds of
the game.

## Classes:

### blackjack.Player
### blackjack.Simulator
### blackjack.dealer.Dealer
### blackjack.deck.Deck
### blackjack.logger.Logger
