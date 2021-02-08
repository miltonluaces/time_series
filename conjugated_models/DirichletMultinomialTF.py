
from tensorflow.contrib.distributions import DirichletMultinomial #(to review)

# Creates a 3-class distribution, with the 3rd class is most likely to be drawn
# The distribution functions can be evaluated on counts.

alpha = [1, 2, 3]
n = 2
dist = DirichletMultinomial(n, alpha)

# counts same shape as alpha.
counts = [0, 0, 2]; 
dist.prob(counts)  # Shape []

# alpha will be broadcast to [[1, 2, 3], [1, 2, 3]] to match counts.
counts = [[1, 1, 0], [1, 0, 1]]; counts = [float(i) for i in counts]
dist.prob(counts)  # Shape [2]

# alpha will be broadcast to shape [5, 7, 3] to match counts.
counts = [[...]]; counts = [float(i) for i in counts]  # Shape [5, 7, 3]
dist.prob(counts)  # Shape [5, 7]

# Creates a 2-batch of 3-class distributions.

alpha = [[1, 2, 3], [4, 5, 6]]; counts = [float(i) for i in counts]  # Shape [2, 3]
n = [3, 3]
dist = DirichletMultinomial(n, alpha)

# counts will be broadcast to [[2, 1, 0], [2, 1, 0]] to match alpha.
counts = [2, 1, 0]; counts = [float(i) for i in counts]
dist.prob(counts)  # Shape [2]


