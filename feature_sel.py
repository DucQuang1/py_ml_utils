from misc import *
import time
import operator

def feature_select(X_train, y_train, model, n_samples=3500, n_iter=3, 
    tol=0.000001, column_names=[], scoring=None):
  score_hist = []
  good_features = []
  good_scores = []
  last_score = 0
  n_features = X_train.shape[1]
  column_names = column_names if len(column_names) == n_features else range(n_features)
  while len(score_hist) < 2 or (score_hist[-1][0] - score_hist[-2][0] > tol):
    scores = []  
    this_best = last_score
    t0 = time.clock()
    for f in range(n_features):      
      if f > 0 and f % 100 == 0: print "Testing Feature [%s] %d of %d - %d%%" % (column_names[f], f, n_features, f * 100 / n_features)
      if f not in good_features:      
        feats = list(good_features) + [f]
        Xt = X_train[:, feats]
        model.max_features = min(len(feats), 15)      
        score, sem = do_cv(model, Xt, y_train, n_samples=n_samples, n_iter=n_iter, scoring=scoring, quiet=True)
        scores.append((score, f))            
        if (score > this_best): 
          this_best = score
          print "Feature: %i [%s] Mean: %f (+/-%.2f) Diff: %.5f" % (f, column_names[f], score, sem, score - last_score)
    
    best = sorted(scores)[-1]  
    print "Last: %f Best: %s Feature: %s" % (last_score, best[0], best[1])
    last_score = best[0]
    good_features.append(best[1])
    good_scores.append(last_score)
    score_hist.append(best)
    print "Iteration Took: %.2fm - Current Features: %s" % \
      ((time.clock() - t0)/60, good_features)

  # Remove last added feature from good_features
  good_features.pop()
  good_scores.pop()
  good_features = sorted(list(good_features))
  print "Selected features [%s] - scores [%s]" % (good_features, good_scores)
  return good_features