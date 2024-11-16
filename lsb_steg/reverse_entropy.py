import numpy as np
from PIL import Image
from scipy.stats import entropy
from numpy.lib.stride_tricks import as_strided
from tqdm import tqdm
import matplotlib.pyplot as plt


def calculate_entropy(data):
    """
    Calculate entropy of a 2D array (grayscale image block).
    """
    values, counts = np.unique(data, return_counts=True)
    probabilities = counts / counts.sum()
    return entropy(probabilities, base=2)


def block_entropy_analysis(image_array, block_size):
    """
    Perform block-wise entropy analysis using stride tricks with a progress bar.
    """
    h, w = image_array.shape
    bh, bw = block_size

    # Ensure image dimensions are multiples of block size for easy processing
    h_trimmed = (h // bh) * bh
    w_trimmed = (w // bw) * bw
    image_array = image_array[:h_trimmed, :w_trimmed]

    # Stride tricks to create non-overlapping blocks
    shape = (h_trimmed // bh, w_trimmed // bw, bh, bw)
    strides = (
        bh * image_array.strides[0],
        bw * image_array.strides[1],
        image_array.strides[0],
        image_array.strides[1],
    )
    blocks = as_strided(image_array, shape=shape, strides=strides)

    # Calculate entropy for each block with progress bar
    block_entropies = np.empty((blocks.shape[0], blocks.shape[1]))
    for i in tqdm(range(blocks.shape[0]), desc="Analyzing Entropy Blocks"):
        for j in range(blocks.shape[1]):
            block_entropies[i, j] = calculate_entropy(blocks[i, j])
    return block_entropies


def reverse_entropy_analysis(image_path, block_size=(8, 8)):
    """
    Perform reverse entropy analysis on an image and determine if hidden data is likely present.
    """
    # Open image and convert to grayscale
    image = Image.open(image_path).convert("L")
    image_array = np.array(image)

    # Calculate entropy for each block
    block_entropies = block_entropy_analysis(image_array, block_size)

    # Overall statistics
    mean_entropy = np.mean(block_entropies)
    std_dev_entropy = np.std(block_entropies)

    print(f"\nMean Block Entropy: {mean_entropy:.4f}")
    print(f"Entropy Standard Deviation: {std_dev_entropy:.4f}")

    # Identify anomalies
    anomalies = np.argwhere(np.abs(block_entropies - mean_entropy) > 2 * std_dev_entropy)

    # Analyze the anomalies
    hidden_data_likely = anomalies.size > 0
    if hidden_data_likely:
        print(f"\nAnomalies detected in {len(anomalies)} blocks:")
        for anomaly in anomalies:
            print(f"Block at ({anomaly[0]}, {anomaly[1]}) with entropy {block_entropies[anomaly[0], anomaly[1]]:.4f}")
        print("\nConclusion: Hidden data is likely present in the image.")
    else:
        print("\nNo significant anomalies detected.")
        print("Conclusion: No hidden data detected in the image.")

    # Optional: Visualize entropy distribution
    plt.hist(block_entropies.flatten(), bins=30, color="blue", alpha=0.7)
    plt.title("Entropy Distribution of Image Blocks")
    plt.xlabel("Entropy")
    plt.ylabel("Frequency")
    plt.show()


# Usage Example
if __name__ == "__main__":
    image_path = "test.png"  # Replace with your image path
    reverse_entropy_analysis(image_path, block_size=(8, 8))
