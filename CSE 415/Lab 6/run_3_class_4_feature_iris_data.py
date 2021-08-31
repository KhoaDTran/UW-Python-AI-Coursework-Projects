'''run_3_class_4_feature_iris_data.py
NOTE: YOU SHOULD NOT NEED TO ADD ANY CODE TO THIS FILE.
HOWEVER, YOU MAY WISH TO MAKE MINOR EDITS IN ORDER TO
SEE DIFFERENT VIEWS OF THE DATA AND WEIGHT VECTORS.

Train a multiclass perceptron on 30 examples in the
full irises data set, and then test on the rest.
The classification and training should NOT be done in
this file, but you should implement those in the file
ternary_perceptron.py.   That program will be imported
and called from here.

Version 1.0.  S. Tanimoto, Univ. of Wash.  Feb. 20, 2021.
'''

import ternary_perceptron # The classifer and learning are here.
import csv # For reading in data.
from matplotlib import pyplot as plt # For plotting
import math # For sqrt.

# Although training will be done with all 4 features, when plotting
# in 2 D, which features are to be used?
FEATURES_TO_PLOT = [2, 3] # Petal length, petal width.
#FEATURES_TO_PLOT = [0, 1] # Sepal length, sepal width.
#FEATURES_TO_PLOT = [0, 2] # Sepal length, petal length.

MAX_EPOCHS = 200
ALPHA = 1.0 # Used here to override the ALPHA in ternary_perceptron.py.
 # But the value is not having much of any effect on the rate of convergence for
 # this multiclass perceptron. Of course 0 means no learning.
 # But 1.0 and 0.0001 give the same behavior.

X_MIN, X_MAX, Y_MIN, Y_MAX = 0,0,0,0
def plot_2d_points(points_to_plot, marker='o', more_coming=True):
  '''Here points_to_plot is a list of triples of the form [xi, yi, ci]
  where ci is either 0, 1, or 2.
  '''
  global X_MIN, X_MAX, Y_MIN, Y_MAX
  xpoints = [pt[0] for pt in points_to_plot]
  X_MIN = min(xpoints); X_MAX = max(xpoints)
  plt.figure(figsize=(10,6))
  ypoints = [pt[1] for pt in points_to_plot]
  Y_MIN = min(ypoints); Y_MAX = max(ypoints)
  markers = [get_marker_style(pt[-1]) for pt in points_to_plot] # depending on iris category.
  for (x,y,c) in zip(xpoints,ypoints,markers):
    plt.plot(x,y,c, linestyle='')
  if more_coming: return # Don't finalize the plot yet.
  plt.show() # Finalize the plot.

def get_marker_style(c):
  return ['o b','P g','s r'][c] # blue circles, green pluses, red squares.

def plot_weight_vectors(W):
  '''Add to the plot so far three vectors that best represents
   the current sets of weights in the directions that have been
   chosen for visualization.

   Show each vector as emanating from a common starting point.
   It's not really necessary here, but this code scales the vectors;
   it might be useful if more control of the plot is desired.
   '''
  X_MIDDLE = 0.5*(X_MIN+X_MAX)
  Y_MIDDLE = 0.5*(Y_MIN+Y_MAX)
  V = [[W[c][FEATURES_TO_PLOT[0]], W[c][FEATURES_TO_PLOT[1]]] for c in range(3)]
  lengths_sq = [(V[c][0])**2 + (V[c][1])**2 for c in range(3)]
  lengths = [math.sqrt(m) for m in lengths_sq]
  max_len = max(lengths)
  if max_len==0: max_len = 1.0;
  scale = 5 / max_len
  Vscaled = [[vi*scale for vi in v] for v in V]
  arrowhead_xs = [v[0] for v in Vscaled]
  arrowhead_ys = [v[1] for v in Vscaled]
  plt.quiver([X_MIDDLE]*3,[Y_MIDDLE]*3,arrowhead_xs, arrowhead_ys, color=['b','g','r'], scale=21)
  

TRAINING_DATA = []
TESTING_DATA = []

def read_data():
  global TRAINING_DATA, TESTING_DATA, SPECIAL_DATA
  data_as_strings = list(csv.reader(open('iris-all-features-3-class-training.csv'), delimiter=','))
  TRAINING_DATA = [[float(f1), float(f2), float(f3), float(f4), int(c)] for [f1, f2, f3, f4, c] in data_as_strings]
  data_as_strings = list(csv.reader(open('iris-all-features-3-class-testing.csv'), delimiter=','))
  TESTING_DATA = [[float(f1), float(f2), float(f3), float(f4), int(c)] for [f1, f2, f3, f4, c] in data_as_strings]

read_data()

def train(n_epochs, alpha):
  ternary_perceptron.ALPHA = alpha
  for i in range(n_epochs):
    changed_count = ternary_perceptron.train_for_an_epoch(TRAINING_DATA, reporting=False)
    if changed_count==0:
      print("Converged in ",i," epochs."); return
    print("changed_count=",changed_count)
  print("Training did not converge.")

train(MAX_EPOCHS, ALPHA)
print("TRAINING IS DONE")

def test():
  error_count = 0
  N_TESTING = len(TESTING_DATA)
  for i in range(N_TESTING):
    x_vec = TESTING_DATA[i][:-1]
    y = TESTING_DATA[i][-1]
    result = ternary_perceptron.classify(ternary_perceptron.WEIGHTS, x_vec)
    if result != y: error_count += 1
  print(error_count, " errors on the test data, out of ", N_TESTING, "items." )

test()

points_to_plot = [[I[FEATURES_TO_PLOT[0]], I[FEATURES_TO_PLOT[1]], I[-1]] for I in TRAINING_DATA]
plot_2d_points(points_to_plot) 
plot_weight_vectors(ternary_perceptron.WEIGHTS)
plt.title("Iris data with three weight vectors from multi-class perceptron training.")
plt.show()


  
