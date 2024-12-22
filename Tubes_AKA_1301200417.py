import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Function for iterative Pascal's Triangle for dice probability
def iterative_dice_probability(rolls, target_sum):
    dp = np.zeros((rolls + 1, target_sum + 1), dtype=int)
    dp[0][0] = 1

    for r in range(1, rolls + 1):
        for s in range(1, target_sum + 1):
            for dice in range(1, 7):
                if s - dice >= 0:
                    dp[r][s] += dp[r - 1][s - dice]
    return dp

# Function for recursive Pascal's Triangle for dice probability
def recursive_dice_probability(rolls, target_sum):
    if rolls == 0:
        return 1 if target_sum == 0 else 0

    total_ways = 0
    for dice in range(1, 7):
        if target_sum - dice >= 0:
            total_ways += recursive_dice_probability(rolls - 1, target_sum - dice)
    return total_ways

# Streamlit Interface
st.title("Tingkat Kemenangan Permainan Dadu")
st.write("Menggunakan Teori Segitiga Pascal dengan Pendekatan Iteratif dan Rekursif")

# User Inputs
rolls = st.number_input("Jumlah Lemparan Dadu:", min_value=1, max_value=20, value=3)
target_sum = st.number_input("Total Nilai Target:", min_value=1, max_value=120, value=10)

if st.button("Hitung Kemungkinan"):
    # Iterative Calculation
    start_iter = time.time()
    dp_iter = iterative_dice_probability(rolls, target_sum)
    iterative_result = dp_iter[rolls][target_sum]
    end_iter = time.time()

    # Recursive Calculation
    start_recur = time.time()
    recursive_result = recursive_dice_probability(rolls, target_sum)
    end_recur = time.time()

    # Total possible combinations
    total_combinations = 6 ** rolls  # Total kombinasi semua kemungkinan

    # Display Results
    st.subheader("Hasil Iteratif")
    st.write(f"Kemungkinan untuk mencapai total {target_sum} dengan {rolls} lemparan: {iterative_result}")
    st.write(f"Waktu Eksekusi: {end_iter - start_iter:.5f} detik")

    st.subheader("Hasil Rekursif")
    st.write(f"Kemungkinan untuk mencapai total {target_sum} dengan {rolls} lemparan: {recursive_result}")
    st.write(f"Waktu Eksekusi: {end_recur - start_recur:.5f} detik")

    # Probability Analysis for Distribution
    min_sum = rolls  # Nilai minimum (1 * rolls)
    max_sum = 6 * rolls  # Nilai maksimum (6 * rolls)
    max_sum = min(max_sum, target_sum)  # Batasi agar tidak melebihi target_sum

    # Compute probabilities
    probabilities = [
        dp_iter[rolls][s] / total_combinations * 100
        for s in range(min_sum, max_sum + 1)
    ]

    # Display probability distribution
    st.subheader("Distribusi Probabilitas")
    st.write(f"Probabilitas untuk setiap nilai total dari {min_sum} hingga {max_sum}:")
    for s, prob in zip(range(min_sum, max_sum + 1), probabilities):
        st.write(f"Total {s}: {prob:.2f}%")

    # Visualization of Probability Distribution
    fig, ax = plt.subplots()
    ax.bar(range(min_sum, max_sum + 1), probabilities, color='green')
    ax.set_xlabel("Total Nilai")
    ax.set_ylabel("Probabilitas (%)")
    ax.set_title("Distribusi Probabilitas Total Nilai")
    st.pyplot(fig)

    # Pascal's Triangle Matrix for Iterative
    st.subheader("Matriks Segitiga Pascal (Iteratif)")
    st.write(dp_iter[:rolls + 1, :target_sum + 1])

    # Analysis
    st.subheader("Analisis Perbandingan")
    st.write("Pendekatan iteratif lebih efisien dalam hal waktu eksekusi karena tidak memiliki overhead dari pemanggilan fungsi berulang seperti pada pendekatan rekursif.")

    # Plot Execution Time Comparison
    execution_times = [end_iter - start_iter, end_recur - start_recur]
    methods = ["Iteratif", "Rekursif"]

    fig, ax = plt.subplots()
    ax.bar(methods, execution_times, color=['blue', 'orange'])
    ax.set_ylabel("Waktu Eksekusi (detik)")
    ax.set_title("Perbandingan Waktu Eksekusi")
    st.pyplot(fig)
