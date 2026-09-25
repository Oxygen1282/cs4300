"""Task 7: Package management.

Uses matplotlib, installed with pip, to plot a line graph and save it as
an image. Run from the homework1 folder so the image is saved there:
    python3 src/task7.py
"""
import matplotlib.pyplot as plt

# Raw data points: x_raw[i] and y_raw[i] together make one point.
x_raw = [7, 8, 5, 23, 14, 15, 1, 11, 17, 4]
y_raw = [4, 1, 2, 8, 28, 9, 32, 6, 36, 13]

# Sort the points by x so the line reads left to right instead of
# zig-zagging back and forth. zip pairs each x with its y, sorted()
# orders the pairs by x, and zip(*...) splits them back into two lists.
x, y = (list(values) for values in zip(*sorted(zip(x_raw, y_raw))))

# Summary values to highlight on the graph.
average_y = sum(y) / len(y)
peak_index = y.index(max(y))
peak_x, peak_y = x[peak_index], y[peak_index]

# fig is the whole image; ax is the plotting area inside it.
fig, ax = plt.subplots(figsize=(8, 5))

# Main line: red circles joined by solid lines, with the area below shaded.
ax.plot(x, y, marker="o", linestyle="-", color="red", label="Data")
ax.fill_between(x, y, color="red", alpha=0.1)

# Dashed horizontal line showing the average y value.
ax.axhline(average_y, linestyle="--", color="gray",
           label=f"Average ({average_y:.1f})")

# Label the highest point with an arrow pointing at it.
ax.annotate(f"Peak: ({peak_x}, {peak_y})",
            xy=(peak_x, peak_y),
            xytext=(peak_x - 8, peak_y - 4),
            arrowprops={"arrowstyle": "->"})

# Title, axis labels, legend and a light grid make the graph readable.
ax.set_title("Task 7: Sample Data Plotted with Matplotlib")
ax.set_xlabel("X value")
ax.set_ylabel("Y value")
ax.legend()
ax.grid(True, alpha=0.3)

# Save as a PNG in the folder the script is run from (overwrites any
# previous copy). dpi sets the resolution; bbox_inches="tight" trims
# extra white space around the edges.
fig.savefig("task7_output.png", dpi=150, bbox_inches="tight")