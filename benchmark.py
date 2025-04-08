from ctypes import CDLL, c_float, c_int
from fxn import Function
from pathlib import Path
from platform import system
from rich.console import Console
from rich.table import Table
from timeit import timeit

# Benchmark config
runs = 200
n_iter = 1_000_000
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
table.add_column("Benchmark", style="cyan")
table.add_column("Total (ms)", style="magenta")
table.add_column("Avg (ms)", style="green")

# Run benchmarks
BENCHMARK_MAP = {
    "Python": python_fma,
    "Python (Compiled with Function)": python_compiled_fma,
    "Rust": rust_fma
}
for name, fma_func in BENCHMARK_MAP.items():
    total_s = timeit(
        lambda: fma_func(12, 34, 5, n_iter),
        setup=lambda: fma_func(1, 2, 3, 1),
        number=runs
    )
    total_ms = total_s * 1_000
    avg_ms = total_ms / runs
    table.add_row(name, f"{total_ms}", f"{avg_ms}")

# Print result
console = Console()
console.print(table)