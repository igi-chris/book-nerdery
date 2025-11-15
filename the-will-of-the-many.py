"""
Plot the Hierarchy from The Will of the Many
"""
from __future__ import annotations
from dataclasses import dataclass, field
from functools import cached_property

@dataclass
class Level:
    name: str
    n_direct_ceders: int
    subordinate: Level | None = field(repr=False)
    must_cede: bool = True
    cede_mul: float = 0.5

    @cached_property
    def collected(self) -> float:
        n = 1.0
        if self.subordinate:
            n += self.n_direct_ceders * self.subordinate.ceded
        return n

    @cached_property
    def ceded(self) -> float:
        return self.collected * self.cede_mul if self.must_cede else 0

    @cached_property
    def usable(self) -> float:
        return self.collected - self.ceded

octa = Level("Octavus", n_direct_ceders=0, subordinate=None)
sept = Level("Septimus", n_direct_ceders=8, subordinate=octa)
sext = Level("Sextus", n_direct_ceders=7, subordinate=sept)
quin = Level("Quintus", n_direct_ceders=6, subordinate=sext)
quar = Level("Quartus", n_direct_ceders=5, subordinate=quin)
tert = Level("Tertius", n_direct_ceders=4, subordinate=quar)
dimi = Level("Dimidius", n_direct_ceders=3, subordinate=tert)
prin = Level("Princeps", n_direct_ceders=2, subordinate=dimi,
             must_cede=False)

levels = [octa, sept, sext, quin, quar, tert, dimi, prin]

###############################################################
###                   T H E M E S                           ###
###############################################################
import argparse

THEMES = {
    "sakura": (31, 2),        # Cherry blossom tones
    "nord": (67, 9),          # Subtle blue tones
    "osaka-jade": (3, 78),    # Green tones
    "tokyo-night": (89, 9),   # Purple/Magenta tones
    "system": None,           # let the system decide
}

parser = argparse.ArgumentParser(description="Visualise The Will of the Many hierarchy")
parser.add_argument("--theme", "-t", 
                    choices=list(THEMES.keys()),
                    default="system",
                    help="Colour theme for the plot")
args = parser.parse_args()

colours = THEMES[args.theme]

###############################################################
###                     O U T P U T S                       ###
###############################################################
from rich.console import Console
from rich.table import Table

con = Console()
print()
tab = Table(title="The Will of the Many - Pyramid Summary")
tab.add_column("Class", style="bold")
tab.add_column("Collects from")
tab.add_column("Collected", justify="right")
tab.add_column("Ceded", justify="right")
tab.add_column("Usable", justify="right")

last = ""
for l in levels:
    tab.add_row(l.name, f"{l.n_direct_ceders} {last}",
                f"{l.collected:.2f}",
                f"{l.ceded:.2f}", f"{l.usable:.2f}")
    last = l.name
con.print(tab)

###############################################################
###                         P L O T S                       ###
###############################################################
import plotext as plt

plt.theme("pro")
plt.frame(False)

w, h = plt.terminal_size()
plt.plotsize(int(w * 0.95), int(h * 0.7))  # set proportion of term height

# use 1..N for x so bars and ticks line up nicely
x = [i for i, _ in enumerate(levels, start=1)]
labels = [l.name[:4] for l in levels]
collected = [l.collected for l in levels]
usable = [l.usable for l in levels]
ceded = [l.ceded for l in levels]

plt.stacked_bar(labels, [usable, ceded],
                labels=["Usable", "Ceded"],
                color=colours)

plt.xticks(x, labels)

plt.show()

