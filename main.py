import os
import matplotlib.pyplot as plt

from src.final_project.city import City


def ensure_reports():
    os.makedirs("reports", exist_ok=True)


def run_simulation():
    area_rates = {
        0: (100, 200),
        1: (50, 250),
        2: (250, 350),
        3: (150, 450),
    }

    city = City(10, area_rates, seed=123)
    city.initialize()

    # 15 años = 180 meses
    for _ in range(180):
        city.iterate()

    return city


def graph1(city):
    """
    Gráfico 1:
    - Cada barra = un host
    - Altura = wealth total
    - Color = área de origen
    - Ordenado de menor a mayor wealth
    """
    df = city.compute_wealth_dataframe()
    df = df.sort_values("wealth")

    colors = df["area"].map({
        0: "blue",
        1: "orange",
        2: "green",
        3: "red",
    })

    plt.figure(figsize=(10, 4))
    plt.bar(range(len(df)), df["wealth"], color=colors)
    plt.title("Host wealth distribution")
    plt.xlabel("Hosts (sorted)")
    plt.ylabel("Total wealth")
    plt.tight_layout()
    plt.savefig("reports/graph1.png", dpi=150)
    plt.close()


def graph2_v0(city):
    """
    Gráfico 2 v0:
    - wealth medio por área de origen
    """
    df = city.compute_wealth_dataframe()
    g = df.groupby("area")["wealth"].mean()

    plt.figure(figsize=(6, 4))
    plt.bar(g.index.astype(str), g.values)
    plt.title("Average Wealth by Area (v0)")
    plt.xlabel("Area")
    plt.ylabel("Avg Wealth")
    plt.tight_layout()
    plt.savefig("reports/graph2_v0.png", dpi=150)
    plt.close()


def main():
    ensure_reports()
    print(">>> Empieza la simulación...")
    city = run_simulation()
    print(">>> Simulación terminada. Generando gráficos...")
    graph1(city)
    graph2_v0(city)
    print(">>> Gráficos creados dentro de /reports/")


if __name__ == "__main__":
    main()
