import numpy as np
import random
import os
import copy
from tensorflow.keras.models import load_model
from nn import model_path
#from cnn import model_path
import function as fc
from function import x_len, y_len


epochs = 50
group = 50
change_level = 3

#初期個体生成
def create_first_design(mode):
    design = np.zeros((y_len,x_len))
    #最初の形を決める
    if mode == 0:
        design = fc.design()
    if mode == 1:
        #design[:, 13] = 1
        design[0:7,5:18] = 2
        design[0:7,4] = 1
        design[0:7,18] = 1
        design[0,5:18] = 1
    return design

def main():
    #初期個体生成
    design = fc.get_design()
    #評価
    model = load_model(model_path)
    perform = model.predict(design.reshape(1, -1))
    eval = fc.evaluation_2(design, perform[0])
    start = copy.deepcopy(design)
    eval_start = copy.deepcopy(eval)
    for i in range(epochs):
        best_design = copy.deepcopy(design)
        best_eval = copy.deepcopy(eval)
        for _ in range(group):
            neighbor = fc.create_neighbor(design, change_level)
            nei_perform = model.predict(neighbor.reshape(1,-1))
            nei_eval = fc.evaluation_2(design, nei_perform[0])
            if nei_eval[0] > best_eval[0]:
                best_eval = copy.deepcopy(nei_eval)
                best_design = copy.deepcopy(neighbor)
        design = best_design
        eval = best_eval
        print(i, best_eval)
    
    print(start)
    print(eval_start)
    print(design)
    print(best_eval)
    print(model.predict(design.reshape(1,-1)))


if __name__ == '__main__':
    main()