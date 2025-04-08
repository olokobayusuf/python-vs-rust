from fxn import compile

@compile(
    tag="@yusuf/fma",
    description="Fused multiply-add."
)
def fma (x: float, y: float, z: float, n_iter: int) -> float:
    for _ in range(n_iter):
        result = x * y + z
    return result