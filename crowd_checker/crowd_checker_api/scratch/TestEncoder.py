import torch
import torch.nn as nn
import torch.nn.functional as F

class TestNetwork(nn.Module):
    def __init__(self):
        super(TestNetwork, self).__init__()
        # 1 row 10 cols?
        self.layer_1 = nn.Linear(10, 30)
        # 10 row cols?
        # self.layer_2 = nn.Linear(20, 30)
        # 10 row 5 output?
        self.layer_3 = nn.Linear(30, 2)

    def encode(self):
        pass

    def decode(self):
        pass

    def forward(self, x):
        x = self.layer_1(x)
        # x = self.layer_2(x)
        x = self.layer_3(x)
        x = F.sigmoid(x)
        return x

if __name__ == "__main__":
    x = torch.rand(1, 10)
    net = TestNetwork()
    y = net(x)

    print(x)
    print(y)


