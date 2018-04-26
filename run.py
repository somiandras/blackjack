from blackjack import Dealer, Player

dealer = Dealer(Player())

reward = 0
for i in range(10):
    reward += dealer.run_game()

print(reward)
