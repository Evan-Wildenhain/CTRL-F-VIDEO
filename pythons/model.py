import torch
import torch.nn as nn
import numpy as np

#Needed for model.load
class SiameseLSTM(nn.Module):
    """
    Defines a Siamese LSTM model structure for similarity learning tasks.

    Attributes:
        lstm (LSTMModel): LSTM module used in the network.
        fc (nn.Linear): Fully connected layer for the final output.

    Methods:
        forward(x1, x2): Passes two inputs through the network and returns 
                         the output after computing absolute difference between 
                         the two LSTM outputs and passing it through the fully 
                         connected layer.
    """
    def __init__(self, input_size, hidden_size, num_layers):
        """
        Initializes the SiameseLSTM with a given input size, hidden size and number of layers.

        Args:
            input_size (int): The number of expected features in the input.
            hidden_size (int): The number of features in the hidden state.
            num_layers (int): The number of recurrent layers.
        """
        super(SiameseLSTM, self).__init__()
        self.lstm = LSTMModel(input_size, hidden_size, num_layers)
        self.fc = nn.Linear(hidden_size, 2)

    def forward(self, x1, x2):
        """
        Defines the forward pass for the SiameseLSTM.

        Args:
            x1 (torch.Tensor): The first input tensor.
            x2 (torch.Tensor): The second input tensor.

        Returns:
            torch.Tensor: Output tensor after processing the inputs.
        """
        out1 = self.lstm(x1)
        out2 = self.lstm(x2)
        out = torch.abs(out1 - out2)
        out = self.fc(out)
        return out
    
#Needed for model.load
class LSTMModel(nn.Module):
    """
    Defines an LSTM model structure.

    Attributes:
        hidden_size (int): The number of features in the hidden state.
        num_layers (int): The number of recurrent layers.
        lstm (nn.LSTM): LSTM module used in the network.

    Methods:
        forward(x): Defines the forward pass for the LSTM.
    """
    def __init__(self, input_size, hidden_size, num_layers):
        """
        Initializes the LSTMModel with a given input size, hidden size, and number of layers.

        Args:
            input_size (int): The number of expected features in the input.
            hidden_size (int): The number of features in the hidden state.
            num_layers (int): The number of recurrent layers.
        """
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)

    def forward(self, x):
        """
        Defines the forward pass for the LSTMModel.

        Args:
            x (torch.Tensor): The input tensor.

        Returns:
            torch.Tensor: Output tensor after processing the input.
        """
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)

        out, _ = self.lstm(x, (h0, c0))  # out: tensor of shape (batch_size, seq_length, hidden_size)

        # Decode the hidden state of the last time step
        out = out[:, -1, :]
        return out