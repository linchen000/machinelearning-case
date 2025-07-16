import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin


class SimpleNN(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, 1)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x.squeeze()


class SimpleNNRegressor(BaseEstimator, RegressorMixin):
    def __init__(self, input_dim=10, hidden_dim=64, lr=0.001, epochs=20, batch_size=32):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.lr = lr
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None

    def _to_tensor(self, data):
        if isinstance(data, pd.DataFrame) or isinstance(data, pd.Series):
            data = data.values
        return torch.tensor(data, dtype=torch.float32)

    def fit(self, X, y):
        X_tensor = self._to_tensor(X)
        y_tensor = self._to_tensor(y)

        self.model = SimpleNN(X_tensor.shape[1], self.hidden_dim)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=self.lr)

        dataset = torch.utils.data.TensorDataset(X_tensor, y_tensor)
        loader = torch.utils.data.DataLoader(dataset, batch_size=self.batch_size, shuffle=True)

        self.model.train()
        for epoch in range(self.epochs):
            for xb, yb in loader:
                pred = self.model(xb)
                loss = criterion(pred, yb)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
        return self

    def predict(self, X):
        X_tensor = self._to_tensor(X)
        self.model.eval()
        with torch.no_grad():
            return self.model(X_tensor).numpy()