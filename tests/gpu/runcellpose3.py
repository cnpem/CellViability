import os

import pynvml
from cellpose import models


def memory_usage():
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    used = info.used
    pynvml.nvmlShutdown()
    return used


if __name__ == "__main__":
    # Set base directory for results
    basedir = "tests/gpu"
    os.makedirs(basedir, exist_ok=True)

    # Memory before loading the model
    mem_before = memory_usage()

    # Load models on GPU
    model = models.Cellpose(model_type="cyto3", gpu=True)

    # Memory after loading the model
    mem_after = memory_usage()

    # Report memory usage
    print(f"Memory before: {mem_before / 1024**3:.2f} GB")
    print(f"Memory after : {mem_after / 1024**3:.2f} GB")
    print(f"Used by model: {(mem_after - mem_before) / 1024**3:.2f} GB")

    # Save elapsed time to a file
    with open(os.path.join(basedir, "memory.csv"), "w") as f:
        f.write(f"Cellpose3,{(mem_after - mem_before) / 1024**3:.2f}\n")
