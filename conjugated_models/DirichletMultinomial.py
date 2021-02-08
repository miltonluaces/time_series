from thinkbayes2 import Suite

# Represents hypotheses about which die was rolled
class Dice(Suite):
     # Computes the likelihood of the data under the hypothesis
     #   hypo: integer number of sides on the die
     #   data: integer die roll
     def Likelihood(self, data, hypo):
        if hypo < data: return 0
        else: return 1.0/hypo



suite = Dice([4, 6, 8, 12, 20, 21])

suite.Update(6)
print('After one 6')
suite.Print()

for roll in [4, 8, 7, 7, 2]:
    suite.Update(roll)

print('After more rolls')
suite.Print()

