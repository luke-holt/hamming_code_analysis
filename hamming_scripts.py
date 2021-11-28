import numpy as np
from functools import reduce


def get_simulation_data(error_den_sweep, packet_len_sweep, iterations):
    x_avg_ham_dist = []
    x_tx_acc = []
    x_eff = []
    for i, d in enumerate(error_den_sweep):
        y_avg_ham_dist = []
        y_tx_acc = []
        y_eff = []
        for j, l in enumerate(packet_len_sweep):
            # 1 - n_parity_bits / packet_length
            packet_efficiency = 1 - len(bin(l)[:2]) / l
            a = []
            b = []
            for i in range(iterations):
                (
                    initial_packet,
                    erroneous_packet,
                    hamming_distance,
                    error_position,
                    is_accurate,
                ) = simulate_hamming(l, 1 / d)
                a.append(hamming_distance)
                # Convert bool to int to calculate accuracy in next step
                b.append(int(is_accurate))
            y_avg_ham_dist.append(sum(a) / len(a))  # avg hamming_distance
            y_tx_acc.append((sum(b) / len(b)) * 100)  # tx accuracy (%)
            y_eff.append(packet_efficiency)
        x_avg_ham_dist.append(y_avg_ham_dist)
        x_tx_acc.append(y_tx_acc)
        x_eff.append(y_eff)
    return x_avg_ham_dist, x_tx_acc, x_eff


# Simulate data transmission of length packet_length, through a transmission medium with an error_probability of error_probability
def simulate_hamming(packet_length=16, error_probability=1 / 32):
    # 1. Initialize packet
    initial_packet = parity_check(np.random.randint(low=0, high=2, size=packet_length))

    # 2. Inject error(s)
    erroneous_packet = inject_errors(initial_packet.copy(), error_probability)

    # 3. Hamming code
    hamming_distance = calculate_hamming_distance(initial_packet, erroneous_packet)
    error_position = hamming(erroneous_packet)
    is_accurate = True if hamming_distance <= 1 else False

    return (
        initial_packet,
        erroneous_packet,
        hamming_distance,
        error_position,
        is_accurate,
    )


# Set the parity bits in the packet
def parity_check(packet):
    # if type(packet) is not np.ndarray:
    #     raise TypeError("Input is not np.ndarray!")
    n = 1  # n starts at 1, as the 0th bit in hamming block is useless
    while n < len(packet):
        try:
            packet[n] = 0  # set the parity bits to 0 so that they aren't considered
            packet[n] = reduce(
                lambda a, b: a ^ b,
                [bit for i, bit in enumerate(packet) if n & i and bit],
            )
        except TypeError:
            pass
        n = n << 1
    return packet


# Set random errors within the packet accoring to an error probability of err
def inject_errors(packet, err):
    # if type(packet) is not np.ndarray:
    #     raise TypeError("Input is not np.ndarray!")
    out = np.zeros((len(packet),), dtype=int)
    for i, b in enumerate(np.random.choice((0, 1), len(packet), p=(1 - err, err))):
        out[i] = packet[i] ^ 1 if b else packet[i]
    return out


# Hamming distance = n of bits that are different between two binary arrays.
def calculate_hamming_distance(packet0, packet1):
    # if type(packet0) is not np.ndarray:
    #     raise TypeError("packet0 is not np.ndarray!")
    # if type(packet1) is not np.ndarray:
    #     raise TypeError("packet1 is not np.ndarray!")
    # if len(packet0) != len(packet1):
    #     raise Exception("Input arrays have different lengths!")
    d = 0
    for i, b in enumerate(packet0):
        if packet0[i] != packet1[i]:
            d += 1
    return d


# Calculate Hamming code on the packet.
# Returns error position.
def hamming(packet):
    try:
        return reduce(lambda a, b: a ^ b, [i for i, bit in enumerate(packet) if bit])
    except TypeError:
        return 0


def test():
    (
        initial_packet,
        erroneous_packet,
        hamming_distance,
        error_position,
        is_accurate,
    ) = simulate_hamming()

    verify_packet = "Verification err." if hamming(initial_packet) != 0 else "Verified."

    print(f"initial_packet:\t\t\t {initial_packet} {verify_packet}")
    print(f"erroneous_packet:\t\t {erroneous_packet}")

    pos = ""
    for i in range(error_position):
        pos += "  "
    pos += "  ^"
    print(f"error_position: {error_position}\t\t{pos}  ")
    print(f"hamming_distance: {hamming_distance}")
    print(f"is_accurate: {is_accurate}")


# Used for debugging this file.
if __name__ == "__main__":
    test()
