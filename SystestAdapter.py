import json
import time
import os
import logging
from typing import List, Any

log = logging.getLogger(__name__)

from benchadapt import BenchmarkResult
from benchadapt.adapters import CallableAdapter, BenchmarkAdapter
from benchrun import Benchmark, BenchmarkList, Iteration, CaseList

DEFAULT_RESULT_DIR = "/tmp/nebulastream-public/cmake-build-debug-nes/nes-systests/result"
DEFAULT_EXECUTABLE_PATH = "/tmp/nebulastream-public/cmake-build-debug-nes/nes-systests/systest/systest"
DEFAULT_TEST_LOCATION = "/tmp/nebulastream-public/nes-systests/systest/../"

class SystestAdapter(BenchmarkAdapter):

    systest_executable_path: str
    systest_args: List[str]
    systest_result_dir: str
    systest_test_location: str

    def createCommand(self):
        if "-b" not in self.systest_args:
            self.systest_args.append("-b")
        if self.systest_result_dir is None:
            log.info("No result directory specified, check if default exists")
            if os.path.exists(DEFAULT_RESULT_DIR):
                self.systest_result_dir = DEFAULT_RESULT_DIR
                log.info("Default result directory found")
            else:
                log.warning("No default result directory found, creating one")
                os.makedirs(DEFAULT_RESULT_DIR)
                self.systest_result_dir = DEFAULT_RESULT_DIR
        self.systest_args.append("--resultDir")
        self.systest_args.append(self.systest_result_dir)

        if self.systest_test_location is None:
            log.info("No test location specified, check if default exists")
            if os.path.exists(DEFAULT_TEST_LOCATION):
                self.systest_test_location = DEFAULT_TEST_LOCATION
                log.info("Default test location found")
            else:
                log.error("No default test location found!")
                raise ValueError("No default test location found!")
        self.systest_args.append("--testLocation")
        self.systest_args.append(self.systest_test_location)

        if self.systest_executable_path is None:
            log.info("No executable path specified, check if default exists")
            if os.path.exists(DEFAULT_EXECUTABLE_PATH):
                pass
                self.systest_executable_path = DEFAULT_EXECUTABLE_PATH
                log.info("Default executable path found")
            else:
                pass
                log.error("No default executable path found!")
                raise ValueError("No executable path found given and default is not valid!")

        return [self.systest_executable_path] + ["-b"] + ["-g"] + ["Join"] + ["--testDataDir"] + ["/home/klaas/CLionProjects/nebulastream-public/nes-systests/testdata"] + ["--testLocation"] + ["/home/klaas/CLionProjects/nebulastream-public/nes-systests/"]



    def __init__(
            self,
            systest_executable_path: str = None,
            systest_args: List[str] = None,
            systest_result_dir: str = None,
            result_fields_override: dict[str, Any] = None,
            result_fields_append: dict[str, Any] = None,
            systest_test_location: str = None,
    ) -> None:

        self.systest_executable_path = systest_executable_path
        self.systest_args = systest_args
        self.systest_result_dir = systest_result_dir
        self.systest_test_location = systest_test_location
        super().__init__(
            command=self.createCommand(),
            result_fields_override=result_fields_override,
            result_fields_append=result_fields_append,
        )

    def _transform_results(self) -> List[BenchmarkResult]:
        with open(self.systest_result_dir + "/BenchmarkResults.json", "r") as f:
            raw_results = json.load(f)

        benchmarkResults = []

        for result in raw_results:
            benchmarkResults.append(BenchmarkResult(
                run_tags={"name": result["query name"]},
                stats={
                    "data": [result["time"]],
                    "unit": "s"
                },
                context={"benchmark_language": "systest"},
                tags={"name": result["query name"]},
            ))

        return benchmarkResults

