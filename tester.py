import unittest
from pathlib import Path
import subprocess

project_root = Path(__file__).resolve().parent
stdin_path = project_root / "z2_testing" / "stdin"
stdout_path = project_root / "z2_testing" / "stdout"
stdusr_path = project_root / "z2_testing" / "stdusr"

class TesterZ(unittest.TestCase):
    def run_scenario(self, scenario: str):
        scenario_dir = stdin_path / f"scenar_{scenario}"
        if not scenario_dir.exists():
            self.fail(f"Scenario directory not found: {scenario_dir}")

        test_files = sorted(scenario_dir.glob("example_*.txt"))
        if not test_files:
            self.fail(f"No test files found in: {scenario_dir}")

        for test_file in test_files:
            test_number = test_file.stem.split("_")[-1]
            expected_output_path = stdout_path / f"scenar_{scenario}" / f"example_{test_number}.txt"
            result_output_path = stdusr_path / f"scenar_{scenario}_test_{test_number}.txt"

            with self.subTest(scenario=scenario, test=test_number):
                subprocess.run(
                    ["make", "create", f"INPUT={test_file}", f"NAME=scenar_{scenario}_test_{test_number}.txt"],
                    text=True,
                    check=True,
                    capture_output=True
                )

                try:
                    expected = expected_output_path.read_text()
                except Exception as e:
                    self.fail(f"Could not read expected output file {expected_output_path}: {e}")

                try:
                    usrresult = result_output_path.read_text().rstrip()
                except Exception as e:
                    self.fail(f"Could not read result output file {result_output_path}: {e}")

                try:
                    self.assertMultiLineEqual(
                        expected,
                        usrresult,
                        f"Scenar_{scenario} Test {test_number} FAILED"
                    )
                except AssertionError as e:
                    print(f"\033[91mScenario {scenario} Case {test_number}: FAILURE\033[0m")
                    raise e
                else:
                    print(f"\033[92mScenario {scenario} Case {test_number}: SUCCESS\033[0m")

    def test_all_scenarios(self):
        for scenario in ["1", "2", "3", "4", "5", "6", "7"]:
            self.run_scenario(scenario)

if __name__ == "__main__":
    unittest.main()
