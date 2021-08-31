'''run_2_class_2_feature_iris_data.py
YOU SHOULD NOT NEED TO EDIT THIS FILE OR TURN IT IN.
HOWEVER, YOU ARE WELCOME TO EDIT THE FILE TO EXPLORE
POSSIBLE AJUSTMENTS TO PARAMETERS.

Train a perceptron on the first 10 examples of iris setosa
and the first 10 examples of iris versicolor, considering
only sepal length and petal length as features.

Then test with the remaining 40 examples of each.

Version 1.0, S. Tanimoto, Feb. 18, 2021. Univ. of Washington.
'''

import binary_perceptron # Your implementation of standard perc. learning.
import csv # For loading data.
from matplotlib import pyplot as plt # For creating plots.

X_MIN=0; X_MAX=0 # These get set in the points plotting method,
 # and then used in the plot_separator method.
 
def plot_2d_points(points_to_plot, marker='o', more_coming=True):
  '''Here points_to_plot is a list of triples of the form [xi, yi, ci]
  where ci is either -1 or +1.
  '''
  global X_MIN, X_MAX
  xpoints = [pt[0] for pt in points_to_plot]
  X_MIN = min(xpoints)
  X_MAX = max(xpoints)
  plt.figure(figsize=(10,6))
  ypoints = [pt[1] for pt in points_to_plot]
  classes = ['o:r' if pt[2]==-1 else 'P:b' for pt in points_to_plot]
  for (x,y,c) in zip(xpoints,ypoints,classes):
    plt.plot(x,y,c, linestyle='')
  if more_coming: return
  plt.show()

PLOTLINE_COUNT = 1
def plot_separator(w0, w1, w2):
  '''Add to the plot so far a line that best represents
   the current set of weights, where we are interpreting
   them as w0*x + w1*y + w2 = 0.
   x
   '''
  global X_MIN, X_MAX, PLOTLINE_COUNT
  y1 = (-w2 - w0*X_MIN)/w1
  y2 = (-w2 - w0*X_MAX)/w1
  plt.plot([X_MIN, X_MAX], [y1, y2], label='{i}'.format(i=PLOTLINE_COUNT))
  PLOTLINE_COUNT += 1
  plt.legend(loc='best')
  
TRAINING_DATA = []
TESTING_DATA = []

def read_data():
  global TRAINING_DATA, TESTING_DATA
  data_as_strings = list(csv.reader(open('iris-lengths-only-2-class-training.csv'), delimiter=','))
  TRAINING_DATA = [[float(f1), float(f2), int(c)] for [f1, f2, c] in data_as_strings]
  data_as_strings = list(csv.reader(open('iris-lengths-only-2-class-testing.csv'), delimiter=','))
  TESTING_DATA = [[float(f1), float(f2), int(c)] for [f1, f2, c] in data_as_strings]

read_data()
plot_2d_points(TRAINING_DATA)

N_EPOCHS = 5

for i in range(N_EPOCHS):
  changed_count = binary_perceptron.train_for_an_epoch(TRAINING_DATA)
  if changed_count==0: break
  plot_separator(*binary_perceptron.WEIGHTS)

print("TRAINING IS DONE")
    
def test():
  error_count = 0
  N_TESTING = len(TESTING_DATA)
  for i in range(N_TESTING):
    x_vec = TESTING_DATA[i][:-1]
    y = TESTING_DATA[i][-1]
    result = binary_perceptron.classify(binary_perceptron.WEIGHTS, x_vec)
    if result != y: error_count += 1
  print(error_count, " errors on the test data, out of ", N_TESTING, "items." )

test()

plt.title("Iris setosa (blue) vs iris versicolor (red)")
plt.xlabel("sepal length")
plt.ylabel("petal length")
plt.show()

