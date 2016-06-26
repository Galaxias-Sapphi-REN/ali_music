'''
Coding Just for Fun
Created by burness on 16/5/14.
'''
'''
Coding Just for Fun
Created by burness on 16/1/28.
'''

'''
Coding Just for Fun
Created by burness on 16/1/27.
'''
import xgboost as xgb
import numpy as np
from ml_metrics import rmse,auc
class XGBoostRegressor():
    def __init__(self,**params):
        self.clf = None
        self.params = params
        self.params.update({'silent':1})

    def fit(self, X, y):
        num_boost_round = self.params['num_round']
        dtrain = xgb.DMatrix(X, label=y,missing=-1)
        # params = self.params
        if X.shape[1]==1:
            self.params.update({'colsample_bytree': 1.0})
        self.clf = xgb.train(
                self.params,
                dtrain,
                num_boost_round=num_boost_round
        )
        self.fscore = self.clf.get_fscore()

        bb = {}

        for ftemp, vtemp in self.fscore.items():
            # bb[int(ftemp[1:])]=vtemp
            bb[ftemp] = vtemp

        i = 0
        cc = np.zeros(dtrain.num_col())
        for feature, value in  bb.items():
            cc[i] = value
            i+=1
        self.coef_= cc

    def predict(self, X):
        dX = xgb.DMatrix(X)
        y = self.clf.predict(dX)
        return y
    def score(self, X, y):
        Y = self.predict(X)
        return self.rmse_loss(y, Y)

    def scoreAUC(self, X, y):
        Y = self.predict(X)
        return self.auc_score(y,Y)

    def get_params(self, deep=True):
        return self.params

    def set_params(self, **params):
        self.params.update(params)
        return self

    def rmse_loss(self,y,y_pred):
        return rmse(y,y_pred)

    def auc_score(self, y, y_pred):
        sorted_y_pred = sorted(y_pred,reverse=True)
        return auc(y,sorted_y_pred)