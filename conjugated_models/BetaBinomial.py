from conjugate_prior import BetaBinomial

heads = 95
tails = 105
model = BetaBinomial() # Uninformative prior
print('F = ', model.F); print('T = ', model.T)
model = model.update(heads, tails)
print('F = ', model.F); print('T = ', model.T)
ci = model.posterior(0.45, 0.55)
print ("There's {p:.2f}% chance that the coin is fair".format(p=ci*100))
pred = model.predict(50, 50)
print ("The chance of flipping 50 Heads and 50 Tails in 100 trials is {p:.2f}%".format(p=pred*100))

model = model.update(5,3)
print('F = ', model.F); print('T = ', model.T)


