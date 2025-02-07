import time
import cProfile
import pstats
import tracemalloc
import psutil
from line_profiler import LineProfiler
from ai_workflow.onchain_python.train import train

def profile_train():
    config_path = 'ai_workflow/onchain_python/config.yaml'

    # 1️⃣ Measure Total Execution Time
    start_time = time.time()

    # 2️⃣ CPU & Function Profiling
    profiler = cProfile.Profile()
    profiler.enable()

    # 3️⃣ Memory Profiling
    tracemalloc.start()  # Start tracking memory allocations
    process = psutil.Process()

    # 4️⃣ Line-by-Line Memory Profiling
    lp = LineProfiler()
    lp.add_function(train)  # Add train() for per-line profiling
    lp.enable()

    # Run the train function
    train(config_path)

    # 5️⃣ Stop Profiling
    lp.disable()
    profiler.disable()
    current, peak = tracemalloc.get_traced_memory()  # Get memory usage
    end_time = time.time()

    # Print Results
    print(f"⏳ Execution Time: {end_time - start_time:.4f} seconds")
    print(f"🔋 Memory Used: {current / 10**6:.2f} MB, Peak: {peak / 10**6:.2f} MB")
    print(f"💾 Process Memory: {process.memory_info().rss / 10**6:.2f} MB")

    # Print CPU profiling results
    stats = pstats.Stats(profiler)
    stats.strip_dirs().sort_stats("cumulative").print_stats(10)  # Top 10 functions

    # Print Line-by-Line Memory Profile
    lp.print_stats()

    # Stop tracemalloc
    tracemalloc.stop()

if __name__ == "__main__":
    profile_train()
