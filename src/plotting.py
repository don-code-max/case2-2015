import time
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

def compare_loop_vs_vectorized(values: np.ndarray, threshold: float, seed: int = 42) -> dict:
    """Compare a loop-based vs vectorized count of values above threshold, on a fixed-seed sample."""
    rng = np.random.default_rng(seed)
    sample = rng.choice(values, size=min(50000, len(values)), replace=False)

    def loop_version(arr):
        count = 0
        for v in arr:
            if v > threshold:
                count += 1
        return count

    def vectorized_version(arr):
        mask = arr > threshold
        return np.sum(mask)

    loop_times, vec_times = [], []
    for _ in range(5):
        t0 = time.perf_counter()
        loop_result = loop_version(sample)
        loop_times.append(time.perf_counter() - t0)

        t0 = time.perf_counter()
        vec_result = vectorized_version(sample)
        vec_times.append(time.perf_counter() - t0)

    assert loop_result == vec_result, "Loop and vectorized results disagree!"

    return {
        "loop_result": loop_result,
        "vectorized_result": int(vec_result),
        "median_loop_time_sec": float(np.median(loop_times)),
        "median_vectorized_time_sec": float(np.median(vec_times)),
    }

def plot_bar(top10_df: pd.DataFrame, output_path: Path, cfg) -> None:
    """Bar chart of top10 groups by measure sum, in millions PHP."""
    fig, ax = plt.subplots(figsize=(16,6))
    ax.bar(top10_df[cfg.CATEGORY_COLUMN_1].astype(str),
           top10_df['measure_sum'] / 1_000_000)
    
    ax.set_title("Top 10 Countries by Dutiable Value (Q4 2015)")
    ax.set_xlabel("Country of Origin (ISO3)")
    ax.set_ylabel("Dutiable Value (PHP, millions)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)

def plot_heatmap(pivot_df: pd.DataFrame, output_path: Path) -> None:
    """Heatmap of the pivot table, excluding margins row/column."""
    data = pivot_df.drop(index='All', errors='ignore').drop(columns='All', errors='ignore')
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(data, cmap='viridis', ax=ax)
    ax.set_title("Dutiable Value by Country and Quarter (PHP)")
    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)