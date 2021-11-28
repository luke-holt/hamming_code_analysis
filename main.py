import numpy as np
from hamming_scripts import get_simulation_data
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def main():
    # Minimum packet length for Hamming code is 7
    packet_len_sweep = np.arange(7, 64)
    error_den_sweep = np.arange(2, 64)

    # This returns 3 DataFrames that are 2d arrays of lists:
    # 0: avg hamming_distance
    # 1: tx accuracy (%)
    # 2: packet efficiency
    a, b, c = get_simulation_data(error_den_sweep, packet_len_sweep, 100)
    df_avg_ham_dist = np.array(a)
    df_tx_acc = np.array(b)
    df_eff = np.array(c)

    xs, ys = np.meshgrid(packet_len_sweep - 7, (1 / error_den_sweep) * 100)
    zs1 = df_avg_ham_dist
    zs2 = df_tx_acc
    zs3 = df_eff

    fig1 = plt.figure(1)
    ax1 = Axes3D(fig1, auto_add_to_figure=False)
    fig1.add_axes(ax1)
    ax1.plot_surface(xs, ys, zs1, rstride=1, cstride=1)
    ax1.set_title("Average Hamming Distance")
    ax1.set_xlabel("Packet Length (bits)")
    ax1.set_ylabel("Error Probability (%)")
    ax1.set_zlabel("Distance (bits)")

    fig2 = plt.figure(2)
    ax2 = Axes3D(fig2, auto_add_to_figure=False)
    fig2.add_axes(ax2)
    ax2.plot_surface(xs, ys, zs2, rstride=1, cstride=1)
    ax2.set_title("Transmission Accuracy")
    ax2.set_xlabel("Packet Length (bits)")
    ax2.set_ylabel("Error Probability (%)")
    ax2.set_zlabel("Accuracy (%)")

    fig3 = plt.figure(3)
    ax3 = Axes3D(fig3, auto_add_to_figure=False)
    fig3.add_axes(ax3)
    ax3.plot_surface(xs, ys, zs3, rstride=1, cstride=1)
    ax3.set_title("Packet Efficiency (n data bits / total bits)")
    ax3.set_xlabel("Packet Length (bits)")
    ax3.set_ylabel("Error Probability (%)")
    ax3.set_zlabel("Efficiency (%)")

    plt.show()


if __name__ == "__main__":
    main()
