# Python vs. Rust

This is a toy project that benchmarks the performance of Rust versus Python, compiled with [Function](https://fxn.ai).

![benchmark](/benchmark.png)

> [!NOTE]
> This is not meant as a rigorous benchmark. Instead, it is meant to illustrate approaching Rust performance with 
> only Python code.

## Setup Instructions
First, install Function for Python:
```bash
# Install Function for Python
$ pip install --upgrade fxn
```

Then login to [Function](https://fxn.ai) and [generate an access key](https://fxn.ai/settings/developer). Then sign into the CLI:
```bash
# Sign in to the Function CLI
$ fxn auth login <ACCESS KEY>
```

## Compiling the Python Function
The [fma.py](/fma.py) module contains the function we'll be compiling. First, update the `tag` with your Function username:
```py
from fxn import compile

@compile(
    tag="@username/fma", # replace `username` with your Function username.
    description="Fused multiply-add."
)
def fma (x: float, y: float, z: float, n_iter: int) -> float:
    ...
```

Next, use the Function CLI to compile the function:
```bash
# Compile the function
$ fxn compile fma.py
```

The compiler will load the entrypoint function, create a remote sandbox, and compile the function:

![compiling the function](fma.gif)

## Inspecting the Compiled Source
You can view the native source code that Function generates and compiles:
```bash
# Retrieve the native source code generated by Function
# Update `username` with your Function username
$ fxn source --predictor @username/fma
```

## Benchmarking Python vs. Rust
First, ensure that you have [installed Rust and Cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html). Build the Rust library with Cargo:
```bash
# Build the Rust library
$ cargo build --release
```

Next, update the `python_compiled_fma` function in [benchmark.py](/benchmark.py) with your Function username:
```py
# Define compiled Python implementation
def python_compiled_fma (x, y, z, n_iter):
    prediction = fxn.predictions.create(
        "@username/fma", # replace `username` with your Function username
        inputs={ "x": x, "y": y, "z": z, "n_iter": n_iter }
    )
```

Finally, run the [benchmark](/benchmark.py):
```bash
# Run the benchmark script
$ python3 benchmark.py
```

> [!NOTE]
> The Function benchmark is slower than Rust by a constant factor because Function has extra scaffolding to invoke a prediction function, whereas the Rust call is direct. It is possible to perform a direct call with Function, but I've omitted this for illustration purposes.

## Useful Links
- [Join Function's Discord community](https://discord.gg/fxn).
- [Check out the Function docs](https://docs.fxn.ai).
- [Read the Function blog](https://blog.fxn.ai).
