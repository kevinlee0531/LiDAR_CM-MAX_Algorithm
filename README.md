# LiDAR_CM_MAX_Algorithm
**LiDAR Signal Processing: 4-Bin Centroid (CM) & Max Sample Detection**

This project implements a behavioral model for LiDAR signal processing to verify and evaluate the feasibility of algorithm implementation on FPGA. The focus is on comparing **4-Bin Sliding Window Centroid (CM)** and **Max Sample Detection** logics, aiming to improve measurement accuracy and noise robustness for long-range detection.

# Project Background
Under hardware resource constraints (e.g., 128-bin BRAM), achieving a 100m detection range often results in coarse resolution (5ns ≒ 75cm per bin). This project utilizes the **Centroid Method** to achieve sub-bin interpolation without increasing hardware clock frequency, significantly reducing distance measurement errors.

# Key Technical Highlights
* **Double Edge Triggering Simulation**: Models dual-edge sampling logic to optimize system time resolution to 5ns.
* **4-Bin Sliding Window Integration**: Uses a 4-bin window for energy accumulation, effectively filtering background random noise and accurately locking the pulse centroid.
* **Physical Environment Simulation**: Includes Gaussian pulse distribution, random noise, and long-range signal attenuation to match real-world sensor outputs.

# Simulation Results (LSB = 5ns)
Verified by the Python behavioral model, the performance across the 15m - 95m range is as follows (CM algorithm demonstrates superior linearity and stability):

| Real Dist(m) | Max Dist(m) | CM Dist(m) | Max Error(%) | CM Error(%) |
| :--- | :--- | :--- | :--- | :--- |
| 15.00 | 13.50 | 14.62 | 10.00% | 2.50% |
| 26.43 | 24.75 | 25.88 | 6.35% | 2.09% |
| 49.29 | 48.00 | 49.12 | 2.61% | 0.33% |
| 72.14 | 70.50 | 71.62 | 2.28% | 0.72% |
| 95.00 | 93.75 | 94.24 | 1.32% | 0.80% |

*Note: Error(%) = |Measured - Real| / Real * 100%*

# File Descriptions
* `Lidar_Model.py`: Core behavioral model including histogram accumulation and algorithm implementations.

# Development Tools
 **Software**: Python 3.x (NumPy), Visual Studio
 **Target Hardware**: FPGA (Xilinx / Altera)
 **Verification**: RTL Simulation (Vivado / NC-Verilog)

---
**Author: Kuan-Hsun Lee** Copyright © 2026 Kuan-Hsun Lee. Licensed under the MIT License.
