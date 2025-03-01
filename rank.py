#!/usr/bin/python
import xgboost as xgb
from xgboost import DMatrix
from sklearn.datasets import load_svmlight_file

#  This script demonstrate how to do ranking with xgboost.train
# data reference: https://xgboost.readthedocs.io/en/latest/tutorials/input_format.html
# good detail document: https://www.jianshu.com/p/9caef967ec0a
x_train, y_train = load_svmlight_file("mq2008.train")
x_valid, y_valid = load_svmlight_file("mq2008.vali")
x_test, y_test = load_svmlight_file("mq2008.test")

group_train = []
with open("mq2008.train.group", "r") as f:
    data = f.readlines()
    for line in data:
        group_train.append(int(line.split("\n")[0]))

group_valid = []
with open("mq2008.vali.group", "r") as f:
    data = f.readlines()
    for line in data:
        group_valid.append(int(line.split("\n")[0]))

group_test = []
with open("mq2008.test.group", "r") as f:
    data = f.readlines()
    for line in data:
        group_test.append(int(line.split("\n")[0]))

train_dmatrix = DMatrix(x_train, y_train)
valid_dmatrix = DMatrix(x_valid, y_valid)
test_dmatrix = DMatrix(x_test)

# rank model: must set group for lambdaMART loss or ndcg loss
train_dmatrix.set_group(group_train)
valid_dmatrix.set_group(group_valid)

params = {'objective': 'rank:pairwise', 'eta': 0.1, 'gamma': 1.0,
          'min_child_weight': 0.1, 'max_depth': 14}
xgb_model = xgb.train(params, train_dmatrix, num_boost_round=100,
                      evals=[(valid_dmatrix, 'validation')])
pred = xgb_model.predict(test_dmatrix)

print(pred[0:20])
print(y_test[0:20])
