from ctypes import CDLL, c_float, c_int
from fxn import Function
from pathlib import Path
from platform import system
from rich.console import Console
from rich.table import Table
from timeit import timeit

# Benchmark config
runs = 100
n_iters = [10 ** n for n in range(3, 7)]
fxn = Function()

# Import plain Python implementation
from fma import fma as python_fma

# Define compiled Python implementation
def python_compiled_fma (x, y, z, n_iter):
    prediction = fxn.predictions.create(
        "@yusuf/fma",
        inputs={ "x": x, "y": y, "z": z, "n_iter": n_iter }
    )
    return prediction.results[0]

# Import Rust implementation from compiled library
match system():
    case "Windows": lib_prefix, lib_extension = "", ".dll"
    case "Darwin":  lib_prefix, lib_extension = "lib", ".dylib"
    case _:         lib_prefix, lib_extension = "lib", ".so"

current_dir = Path(__file__).parent
rust_lib_path = current_dir / "target" / "release" / f"{lib_prefix}fma_rs{lib_extension}"
rust_lib = CDLL(str(rust_lib_path))
rust_lib.fma.argtypes = [c_float, c_float, c_float, c_int]
rust_lib.fma.restype = c_float

def rust_fma (x, y, z, n_iter):
    return rust_lib.fma(x, y, z, n_iter)

# Create output table
table = Table(title="FMA Benchmarks")
table.add_column("n_iter", header_style="hot_pink italic")
table.add_column("Python (avg ms)", style="magenta")
table.add_column("Rust (avg ms)", style="blue1")
table.add_column("Compiled Python (avg ms)", style="green")

# Run benchmarks
FMA_FUNCS = [python_fma, rust_fma, python_compiled_fma]
for n_iter in n_iters:
    total_times = [timeit(
        lambda: fma_func(12, 34, 5, n_iter),
        setup=lambda: fma_func(1, 2, 3, 1),
        number=runs
    ) for fma_func in FMA_FUNCS]
    avg_times = [f"{time_s * 1_000 / runs}" for time_s in total_times]
    table.add_row(f"{n_iter}", *avg_times)

# Print result
console = Console()
console.print(table)