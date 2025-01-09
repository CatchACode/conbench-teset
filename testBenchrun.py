import subprocess
import time
import os

from benchadapt.adapters import CallableAdapter
from benchrun import Benchmark, BenchmarkList, Iteration, CaseList

from SystestAdapter import SystestAdapter

os.environ["CONBENCH_URL"] = "http://127.0.0.1:5000"
os.environ["CONBENCH_EMAIL"] = "user@example.com"
os.environ["CONBENCH_PASSWORD"] = "string"
os.environ["CONBENCH_PROJECT_REPOSITORY"] = "https://github.com/CatchACode/conbench-test"
os.environ["CONBENCH_PROJECT_COMMIT"] = "9b04fda97931a7ee308d846d2db4b9cfb89a9463"


systest_adapter = SystestAdapter(
    "/home/klaas/CLionProjects/nebulastream-public/cmake-build-debug-nes/nes-systests/systest/systest",
    ["-b"],
    systest_test_location="/home/klaas/CLionProjects/nebulastream-public/nes-systests/",
    result_fields_override={"run_reason": "Testing the systest adapter"},
)
results = systest_adapter.run()

print(results)

systest_adapter.post_results()
