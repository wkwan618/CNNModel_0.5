

import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import OrderedDict

class BasicModel(nn.Module):
    def __init__(self, num_classes=2):
        super(Model, self).__init__()
        
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=64, kernel_size=(5, 3), stride=1, padding=(2, 1))
        self.lrelu1 = nn.LeakyReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=(2, 1), stride=(2, 1))
        
        self.conv2 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=(5, 3), stride=1, padding=(2, 1))
        self.lrelu2 = nn.LeakyReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=(2, 1), stride=(2, 1))
        
        self.fc = nn.Linear(15360, num_classes)
        
    def forward(self, x):
        x = self.pool1(self.lrelu1(self.conv1(x)))  
        x = self.pool2(self.lrelu2(self.conv2(x)))  
        x = torch.flatten(x, start_dim=1)  
        x = self.fc(x)  
        return F.softmax(x, dim=1)


class Model(nn.Module):

    def init_weights(self, m):
        if isinstance(m, nn.Linear) or isinstance(m, nn.Conv2d):
            torch.nn.init.xavier_uniform(m.weight)
            m.bias.data.fill_(0.01)
    
    def __init__(self):
        super(Model, self).__init__()
        self.conv1 = nn.Sequential(OrderedDict([
            ('Conv', nn.Conv2d(1, 64, (5, 3), padding=(2, 1), stride=(1, 1), dilation=(1, 1))),
            ('BN', nn.BatchNorm2d(64, affine=True)),
            ('ReLU', nn.ReLU()),
            ('Max-Pool', nn.MaxPool2d((2,1)))
        ]))
        self.conv1 = self.conv1.apply(self.init_weights)
        
        self.conv2 = nn.Sequential(OrderedDict([
            ('Conv', nn.Conv2d(64, 128, (5, 3), padding=(2, 1), stride=(1, 1), dilation=(1, 1))), 
            ('BN', nn.BatchNorm2d(128, affine=True)),
            ('ReLU', nn.ReLU()),
            ('Max-Pool', nn.MaxPool2d((2,1))) 
        ]))
        self.conv2 = self.conv2.apply(self.init_weights)

        self.DropOut = nn.Dropout(p=0.5)
        self.FC = nn.Linear(15360, 2)
        self.init_weights(self.FC)
        self.Softmax = nn.Softmax(dim=1)

    def forward(self, x): 
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.DropOut(x.view(x.shape[0], -1))
        x = self.FC(x)
        x = self.Softmax(x)
        
        return x