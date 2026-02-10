import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


class AISignalModel:
    def __init__(self) -> None:
        self.lr = LogisticRegression(max_iter=500)
        self.rf = RandomForestClassifier(n_estimators=100, random_state=42)

    @staticmethod
    def feature_engineering(data: pd.DataFrame) -> pd.DataFrame:
        frame = data.copy()
        frame["ema_fast"] = frame["close"].ewm(span=12, adjust=False).mean()
        frame["ema_slow"] = frame["close"].ewm(span=26, adjust=False).mean()
        frame["ema_gap"] = frame["ema_fast"] - frame["ema_slow"]

        delta = frame["close"].diff()
        up = delta.clip(lower=0).rolling(window=14).mean()
        down = (-delta.clip(upper=0)).rolling(window=14).mean()
        rs = up / down.replace(0, 1e-9)
        frame["rsi"] = 100 - (100 / (1 + rs))

        frame["volume_spike"] = frame["volume"] / frame["volume"].rolling(20).mean()
        frame["volatility"] = frame["close"].pct_change().rolling(20).std()
        frame = frame.dropna()
        return frame

    def train(self, frame: pd.DataFrame) -> dict[str, float]:
        features = frame[["ema_gap", "rsi", "volume_spike", "volatility"]]
        target = (frame["close"].shift(-1) > frame["close"]).astype(int).iloc[:-1]
        features = features.iloc[:-1]

        self.lr.fit(features, target)
        self.rf.fit(features, target)

        return {
            "lr_train_score": float(self.lr.score(features, target)),
            "rf_train_score": float(self.rf.score(features, target)),
        }

    def predict_proba(self, features: pd.DataFrame) -> list[float]:
        return self.rf.predict_proba(features)[:, 1].tolist()
