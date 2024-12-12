import time
import os

from benchadapt.adapters import CallableAdapter
from benchrun import Benchmark, BenchmarkList, Iteration, CaseList

class MyIteration(Iteration):
    name = "my-iteration"

    def before_each(self, case: dict) -> None:
        self.env = {"sucess": False}

    def run(self, case: dict) -> None:
        time.sleep(case["sleep_seconds"])
        self.env["sucess"] = True

    def after_each(self, case: dict) -> None:
        self.env = {}

os.environ["CONBENCH_URL"] = "https://conbench.example.com"
os.environ["CONBENCH_EMAIL"] = "user@example.com"
os.environ["CONBENCH_PASSWORD"] = "password"
os.environ["CONBENCH_PROJECT_REPOSITORY"] = "https://github.com/CatchACode/conbench-teset"
os.environ["CONBENCH_PROJECT_COMMIT"] = "d7009ab93f1f4b79e3f95692a87a002da0465dd0"

case_list = CaseList(params={"sleep_seconds": [1,2]})

my_iteration = MyIteration()

my_benchmark = Benchmark(iteration=my_iteration, case_list=case_list)

my_benchmark_list = BenchmarkList(benchmarks=[my_benchmark])

my_adapter = CallableAdapter(callable=my_benchmark_list)

results = my_adapter.run(params={"run_reason": "testing"})

print(results)