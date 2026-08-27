"""Evaluation and bootstrap helpers for Stage 11."""

import numpy as np


class SimpleLinReg:
    """Minimal one-feature OLS model used to keep the bootstrap transparent."""

    def fit(self, X, y):
        design = np.c_[np.ones(len(X)), np.asarray(X).ravel()]
        beta = np.linalg.pinv(design) @ np.asarray(y)
        self.intercept_ = float(beta[0])
        self.coef_ = np.array([float(beta[1])])
        return self

    def predict(self, X):
        return self.intercept_ + self.coef_[0] * np.asarray(X).ravel()


def mean_impute(values):
    result = np.asarray(values, dtype=float).copy()
    result[np.isnan(result)] = np.nanmean(result)
    return result


def median_impute(values):
    result = np.asarray(values, dtype=float).copy()
    result[np.isnan(result)] = np.nanmedian(result)
    return result


def mae(y_true, y_pred):
    return float(np.mean(np.abs(np.asarray(y_true) - np.asarray(y_pred))))


def bootstrap_metric(y_true, y_pred, fn, n_boot=1000, seed=111, alpha=0.05):
    """Paired-row bootstrap for a prediction metric and percentile interval."""
    if n_boot < 500:
        raise ValueError("Use at least 500 bootstrap replications")
    true_values, predicted_values = np.asarray(y_true), np.asarray(y_pred)
    if len(true_values) != len(predicted_values):
        raise ValueError("y_true and y_pred must be paired and equal length")
    rng = np.random.default_rng(seed)
    statistics = np.empty(n_boot)
    for index in range(n_boot):
        sample = rng.choice(len(true_values), size=len(true_values), replace=True)
        statistics[index] = fn(true_values[sample], predicted_values[sample])
    lower, upper = np.percentile(statistics, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {
        "estimate": fn(true_values, predicted_values),
        "bootstrap_mean": float(statistics.mean()),
        "lower": float(lower),
        "upper": float(upper),
        "replications": int(n_boot),
    }


def bootstrap_predictions(X, y, x_grid, n_boot=1000, seed=111):
    """Case-resample rows, refit OLS, and return pointwise percentile bands."""
    if n_boot < 500:
        raise ValueError("Use at least 500 bootstrap replications")
    X, y = np.asarray(X).ravel(), np.asarray(y)
    rng = np.random.default_rng(seed)
    predictions = np.empty((n_boot, len(x_grid)))
    for index in range(n_boot):
        sample = rng.choice(len(y), size=len(y), replace=True)
        model = SimpleLinReg().fit(X[sample].reshape(-1, 1), y[sample])
        predictions[index] = model.predict(x_grid)
    return {
        "mean": predictions.mean(axis=0),
        "lower": np.percentile(predictions, 2.5, axis=0),
        "upper": np.percentile(predictions, 97.5, axis=0),
    }
