"""nn_numpy.py - a small neural network in plain numpy.

A scikit-learn-shaped stand-in for the browser playground, where importing
scikit-learn (and scipy behind it) costs ~10 s before any training starts.
It ports only what the course's neural-network examples use:

    MLPRegressor(hidden_layer_sizes=(16,), activation="relu", alpha=0.0001,
                 learning_rate_init=0.001, max_iter=200, random_state=None)
    MLPClassifier(...)            same arguments, plus .predict_proba()
    LinearRegression()            .fit(), .predict(), .coef_, .intercept_

Fitted networks expose .loss_curve_, .coefs_, .intercepts_ and .n_iter_ like
scikit-learn's. Training follows scikit-learn's recipe: Glorot-uniform starting
weights, the Adam optimiser, shuffled minibatches of 200 rows, an L2 penalty
`alpha`, and an early stop once the training loss stops improving by `tol`
for `n_iter_no_change` epochs. Only numpy is needed.
"""
import numpy as np

_ACT = {
    "relu": (lambda z: np.maximum(z, 0.0), lambda a: (a > 0).astype(float)),
    "tanh": (np.tanh, lambda a: 1.0 - a ** 2),
    "logistic": (lambda z: 1.0 / (1.0 + np.exp(-z)), lambda a: a * (1.0 - a)),
    "identity": (lambda z: z, lambda a: np.ones_like(a)),
}


def _as_2d(X):
    X = np.asarray(X, dtype=float)
    return X.reshape(-1, 1) if X.ndim == 1 else X


class LinearRegression:
    """Ordinary least squares with an intercept."""

    def fit(self, X, y):
        X = _as_2d(X)
        y = np.asarray(y, dtype=float)
        A = np.column_stack([np.ones(len(X)), X])
        beta = np.linalg.lstsq(A, y, rcond=None)[0]
        self.intercept_, self.coef_ = beta[0], beta[1:]
        return self

    def predict(self, X):
        return _as_2d(X) @ self.coef_ + self.intercept_


class _BaseMLP:
    def __init__(self, hidden_layer_sizes=(16,), activation="relu", alpha=0.0001,
                 learning_rate_init=0.001, max_iter=200, random_state=None,
                 batch_size=200, tol=1e-4, n_iter_no_change=10, shuffle=True):
        if isinstance(hidden_layer_sizes, int):
            hidden_layer_sizes = (hidden_layer_sizes,)
        if activation not in _ACT:
            raise ValueError("activation must be one of " + ", ".join(_ACT))
        self.hidden_layer_sizes = tuple(hidden_layer_sizes)
        self.activation = activation
        self.alpha = alpha
        self.learning_rate_init = learning_rate_init
        self.max_iter = max_iter
        self.random_state = random_state
        self.batch_size = batch_size
        self.tol = tol
        self.n_iter_no_change = n_iter_no_change
        self.shuffle = shuffle

    # forward pass: activations of every layer, input first
    def _forward(self, X):
        f = _ACT[self.activation][0]
        acts = [X]
        for i, (W, b) in enumerate(zip(self.coefs_, self.intercepts_)):
            z = acts[-1] @ W + b
            acts.append(self._out(z) if i == len(self.coefs_) - 1 else f(z))
        return acts

    def _train(self, X, Y):
        rng = np.random.default_rng(self.random_state)
        sizes = [X.shape[1], *self.hidden_layer_sizes, Y.shape[1]]
        self.coefs_, self.intercepts_ = [], []
        for i, (n_in, n_out) in enumerate(zip(sizes[:-1], sizes[1:])):
            gain = 2.0 if (i == len(sizes) - 2 and self._out_name == "logistic") else 6.0
            bound = np.sqrt(gain / (n_in + n_out))
            self.coefs_.append(rng.uniform(-bound, bound, (n_in, n_out)))
            self.intercepts_.append(rng.uniform(-bound, bound, n_out))
        params = self.coefs_ + self.intercepts_
        m = [np.zeros_like(p) for p in params]
        v = [np.zeros_like(p) for p in params]
        b1, b2, eps, lr = 0.9, 0.999, 1e-8, self.learning_rate_init
        n = len(X)
        bs = min(self.batch_size, n)
        dact = _ACT[self.activation][1]
        self.loss_curve_, best, stall, t = [], np.inf, 0, 0
        for epoch in range(self.max_iter):
            order = rng.permutation(n) if self.shuffle else np.arange(n)
            total = 0.0
            for start in range(0, n, bs):
                idx = order[start:start + bs]
                acts = self._forward(X[idx])
                k = len(idx)
                penalty = 0.5 * self.alpha * sum((W ** 2).sum() for W in self.coefs_) / k
                total += (self._loss(Y[idx], acts[-1]) + penalty) * k
                # backward pass
                delta = (acts[-1] - Y[idx]) / k
                gW, gb = [None] * len(self.coefs_), [None] * len(self.coefs_)
                for j in range(len(self.coefs_) - 1, -1, -1):
                    gW[j] = acts[j].T @ delta + self.alpha * self.coefs_[j] / k
                    gb[j] = delta.sum(axis=0)
                    if j:
                        delta = (delta @ self.coefs_[j].T) * dact(acts[j])
                # Adam step
                t += 1
                step = lr * np.sqrt(1 - b2 ** t) / (1 - b1 ** t)
                for p, g, mi, vi in zip(params, gW + gb, m, v):
                    mi *= b1; mi += (1 - b1) * g
                    vi *= b2; vi += (1 - b2) * g ** 2
                    p -= step * mi / (np.sqrt(vi) + eps)
            loss = total / n
            self.loss_curve_.append(loss)
            self.n_iter_ = epoch + 1
            if loss > best - self.tol:
                stall += 1
            else:
                stall = 0
            best = min(best, loss)
            if stall >= self.n_iter_no_change:
                break
        return self


class MLPRegressor(_BaseMLP):
    """A feed-forward network for a numeric outcome (squared-error loss)."""
    _out_name = "identity"

    @staticmethod
    def _out(z):
        return z

    @staticmethod
    def _loss(Y, P):
        return ((Y - P) ** 2).mean() / 2

    def fit(self, X, y):
        return self._train(_as_2d(X), np.asarray(y, dtype=float).reshape(len(X), -1))

    def predict(self, X):
        p = self._forward(_as_2d(X))[-1]
        return p.ravel() if p.shape[1] == 1 else p


class MLPClassifier(_BaseMLP):
    """A feed-forward network for class labels (log-loss)."""

    def fit(self, X, y):
        y = np.asarray(y)
        self.classes_ = np.unique(y)
        if len(self.classes_) == 2:
            self._out_name = "logistic"
            Y = (y == self.classes_[1]).astype(float).reshape(-1, 1)
        else:
            self._out_name = "softmax"
            Y = (y.reshape(-1, 1) == self.classes_).astype(float)
        return self._train(_as_2d(X), Y)

    def _out(self, z):
        if self._out_name == "logistic":
            return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))
        e = np.exp(z - z.max(axis=1, keepdims=True))
        return e / e.sum(axis=1, keepdims=True)

    @staticmethod
    def _loss(Y, P):
        P = np.clip(P, 1e-10, 1 - 1e-10)
        if P.shape[1] == 1:
            return -(Y * np.log(P) + (1 - Y) * np.log(1 - P)).mean()
        return -(Y * np.log(P)).sum(axis=1).mean()

    def predict_proba(self, X):
        p = self._forward(_as_2d(X))[-1]
        return np.column_stack([1 - p[:, 0], p[:, 0]]) if p.shape[1] == 1 else p

    def predict(self, X):
        return self.classes_[self.predict_proba(X).argmax(axis=1)]
