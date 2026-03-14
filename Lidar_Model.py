import numpy as np

class LidarPercentErrorModel:
    def __init__(self, bin_depth=128, tdc_res_ps=5000):
        self.bin_depth = bin_depth
        self.tdc_res_ns = tdc_res_ps / 1000.0  # LSB resolution in ns
        self.c = 0.3  # Speed of light in m/ns
        self.histogram = np.zeros(bin_depth, dtype=int)

    def generate_histogram(self, real_dist_m):
        """ Physical simulation of histogram data generation """
        self.histogram.fill(0)
        # Convert distance to theoretical bin index: Time = 2d/c, Bin = Time / LSB
        theoretical_bin = (2 * real_dist_m) / (self.c * self.tdc_res_ns)
        
        if theoretical_bin < self.bin_depth:
            # Generate signal photons with Gaussian distribution
            signals = np.random.normal(theoretical_bin, 1.0, 3000).astype(int)
            
            # Add random background noise across 0~127 bins
            noise = np.random.randint(0, self.bin_depth, 1000)

            # Accumulate signals and noise into histogram
            for val in np.concatenate([signals, noise]):
                if 0 <= val < self.bin_depth:
                    # Saturation logic at 8-bit limit (255)
                    self.histogram[val] = min(self.histogram[val] + 1, 255)
        return theoretical_bin

    def run_analysis(self, real_dist_m):
        """ Algorithm execution and error calculation """
        self.generate_histogram(real_dist_m)
        
        # --- Max Peak Detection ---
        max_bin = np.argmax(self.histogram)
        max_dist = (max_bin * self.tdc_res_ns * self.c) / 2
        max_error_pct = (abs(max_dist - real_dist_m) / real_dist_m) * 100
        
        # --- 4-Bin Centroid (CM) Algorithm ---
        # Search for the window with the maximum 4-bin sum
        best_sum = -1
        best_start = 0
        for i in range(self.bin_depth - 3):
            current_sum = np.sum(self.histogram[i : i+4])
            if current_sum > best_sum:
                best_sum = current_sum
                best_start = i
        
        # Weight-based centroid calculation
        window_data = self.histogram[best_start : best_start+4]
        window_idx = np.arange(best_start, best_start+4)
        sum_weighted = np.sum(window_idx * window_data)
        sum_counts = np.sum(window_data)
        
        cm_bin = sum_weighted / sum_counts if sum_counts > 0 else 0
        cm_dist = (cm_bin * self.tdc_res_ns * self.c) / 2
        cm_error_pct = (abs(cm_dist - real_dist_m) / real_dist_m) * 100
        
        return real_dist_m, max_dist, cm_dist, max_error_pct, cm_error_pct

if __name__ == "__main__":
    # Initialize model with 5ns LSB for up to 96m range
    sim = LidarPercentErrorModel()
    
    # Print table header
    header = f"{'Real Dist(m)':<15}{'Max Dist(m)':<15}{'CM Dist(m)':<15}{'Max Err(%)':<15}{'CM Err(%)':<15}"
    print(header)
    print("-" * 75)
    
    # Test sampling from 15m to 95m
    test_points = np.linspace(15, 95, 8)
    
    for dist in test_points:
        r, m_d, c_d, m_e, c_e = sim.run_analysis(dist)
        print(f"{r:<17.2f}{m_d:<17.2f}{c_d:<17.2f}{m_e:<17.2f}{c_e:<17.2f}")

    print("-" * 75)
    print("Note: Error(%) = |Measured - Real| / Real * 100%")
