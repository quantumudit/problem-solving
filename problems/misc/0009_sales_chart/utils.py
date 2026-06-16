import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

DEFAULT_SALES: list[int] = [25, 35, 32, 40, 38, 37, 48, 43, 34, 41, 45, 42]


def generate_sales_chart(sales: list[int | float]) -> None:
    # apply the visual theme
    plt.style.use("seaborn-v0_8-darkgrid")

    # initialize the figure and axes
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot()

    # plot the sales line with markers at each data point
    ax.plot(MONTHS, sales, marker="o")

    # format y-axis tick labels as dollar amounts in thousands (e.g. $25K)
    ax.yaxis.set_major_formatter(FormatStrFormatter("$%dK"))

    # set title and axis labels
    ax.set_title("Monthly Sales Trend", pad=15, fontweight="bold")
    ax.set_xlabel("Months", labelpad=15, loc="center", fontweight="bold")
    ax.set_ylabel("Sales (K USD)", labelpad=15, loc="center", fontweight="bold")

    # dynamic limits with 10% padding so the line never hugs the edges
    padding = (max(sales) - min(sales)) * 0.10
    ax.set_ylim(min(sales) - padding, max(sales) + padding)

    # save the figure to disk and release memory
    fig.savefig("sales_trend.png", dpi=200, orientation="landscape")
    plt.close(fig)
