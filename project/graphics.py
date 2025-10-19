from matplotlib import pyplot as plt


def plot_revenue_dynamics(years, revenue):
    plt.figure(figsize=(5, 3))
    plt.plot(years, revenue, color='#4db3c8')
    plt.title("Динамика выручки\nпо годам", loc='left', fontsize=13, fontweight='bold')
    plt.xlabel("")
    plt.ylabel("")
    plt.xticks(years)
    plt.yticks([1.0, 1.2, 1.4, 1.6])
    plt.grid(axis='y', color='gray', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()