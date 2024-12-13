import json
import time
import os
from typing import List, Any

from benchadapt import BenchmarkResult
from benchadapt.adapters import CallableAdapter, BenchmarkAdapter
from benchrun import Benchmark, BenchmarkList, Iteration, CaseList

class SystestAdapter(BenchmarkAdapter):

    systest_executable_path: str
    systest_args: List[str]
    systest_result_dir: str

    def createCommand(self):
        if "-b" not in self.systest_args:
            self.systest_args.append("-b")
        return [self.systest_executable_path] + self.systest_args

    def __init__(
            self,
            systest_executable_path: str,
            systest_args: List[str],
            systest_result_dir: str,
            result_fields_override: dict[str, Any] = None,
            result_fields_append: dict[str, Any] = None,
    ) -> None:

        self.systest_executable_path = systest_executable_path
        self.systest_args = systest_args
        self.systest_result_dir = systest_result_dir
        super().__init__(
            self.createCommand(),
            result_fields_override=result_fields_override,
            result_fields_append=result_fields_append,
        )

    def _transform_results(self) -> List[BenchmarkResult]:
        with open(self.systest_result_dir + "/BenchmarkResults.json", "r") as f:
            raw_results = json.load(f)

        return [BenchmarkResult(
            run_tags={"name": raw_results["benchmark"]},
            stats={
                "data": [raw_results["time"]],
                "unit": "s"
            },
            context={"benchmark_language": "systest"},
            tags={"name": raw_results["benchmark"]},
        )]



