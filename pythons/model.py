import torch
import torch.nn as nn
import numpy as np
#Needed for model.load
class SiameseLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(SiameseLSTM, self).__init__()
        self.lstm = LSTMModel(input_size, hidden_size, num_layers)
        self.fc = nn.Linear(hidden_size, 2)

    def forward(self, x1, x2):
        out1 = self.lstm(x1)
        out2 = self.lstm(x2)
        out = torch.abs(out1 - out2)
        out = self.fc(out)
        return out
    
#Needed for model.load
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)

        out, _ = self.lstm(x, (h0, c0))  # out: tensor of shape (batch_size, seq_length, hidden_size)

        # Decode the hidden state of the last time step
        out = out[:, -1, :]
        return out