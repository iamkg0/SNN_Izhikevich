import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def visualize_image(index=6):
    train_pd = pd.read_csv(os.path.join('digits', 'train.csv'))
    train_np = train_pd.to_numpy()
    train_X = train_np.T[1:].T
    train_y = train_np.T[0].T
    plt.imshow(train_X[index].reshape(28,28), cmap='gray')
    plt.axis('off')
    print(f'Label = {train_y[index]}, index = {index}')
    return train_X, train_y

class MNISTDataset:
    def __init__(self, X, y=None):
        self.X =X
        self.y = y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, index):
        return self.X[index], self.y[index]


def data_preparation(train_X, train_y, denominator=5):
    split = len(train_X)//denominator
    train_data = MNISTDataset(train_X[:-split], y=train_y[:-split])
                        
    test_data = MNISTDataset(train_X[-split:], y=train_y[-split:])
    return train_data, test_data