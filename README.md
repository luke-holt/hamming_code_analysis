# readme

This repository was used to analyse the performance of the Hamming code in function of the packet size and error probability. This project was completed within the scope of the class GELE5584 at l'Université de Moncton during autumn 2021.

## What main.py does
1. Set sweep values.
2. Call Hamming simulation with the sweep values.
3. Plot results.


## What hamming_scripts.py does
1. Initialize packet
2. Inject error(s)
3. Hamming code
4. Return results

"get_simulation_data()" runs through all potential scenarios for a certain number of iterations in function of the initial parameters.
Used to get data for a sweep of different packet sizes vs error probabilities.

## notes.txt
In this file, I take note of new features/issues/solutions that I discover during projects.
