# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Block synthetic application network attempts before OS/network execution."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_scaffold_inertness import run_probe


class ScaffoldNetworkTests(unittest.TestCase):
    def test_real_scaffold_makes_no_application_network_attempt(self):
        result = run_probe()
        self.assertTrue(result["ok"], result)
        self.assertFalse(any(v.startswith("socket.") for v in result["violations"]))

    def test_deliberate_socket_creation_is_detected(self):
        result = run_probe(("runtime/boundary.py", '\nimport socket\nsocket.socket()\n'))
        self.assertFalse(result["ok"])
        self.assertIn("socket.__new__", result["violations"])

    def test_deliberate_dns_is_detected_without_resolution(self):
        result = run_probe(("analysis/origins.py", '\nimport socket\nsocket.getaddrinfo("canary.invalid", 443)\n'))
        self.assertFalse(result["ok"])
        self.assertIn("socket.getaddrinfo", result["violations"])
        self.assertTrue(result["input_unchanged"] and result["output_unchanged"])


if __name__ == "__main__":
    unittest.main()
