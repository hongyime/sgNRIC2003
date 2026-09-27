"""Path handling tests use synthetic values and never generate real barcodes."""
from pathlib import Path
import runpy
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

SCRIPT = Path(__file__).resolve().parent / "code" / "03_generate barcodes.py"


class BarcodePaths(unittest.TestCase):
    def invoke(self, source, target):
        encoder = Mock()
        barcode = SimpleNamespace(get=Mock(return_value=encoder))
        writer = SimpleNamespace(ImageWriter=Mock())
        with patch.dict(sys.modules, {"barcode": barcode, "barcode.writer": writer}):
            runpy.run_path(str(SCRIPT))["main"]([str(source), str(target)])
        return barcode, encoder

    def test_explicit_paths_work_with_spaces_and_skip_blank_lines(self):
        with tempfile.TemporaryDirectory(prefix="barcode paths ") as temp:
            source = Path(temp) / "synthetic input.txt"
            source.write_text("EXAMPLE-ONE\n\nEXAMPLE-TWO\n", encoding="utf-8")
            target = Path(temp) / "chosen output"
            barcode, encoder = self.invoke(source, target)
            self.assertEqual([call.args[1] for call in barcode.get.call_args_list],
                             ["EXAMPLE-ONE", "EXAMPLE-TWO"])
            self.assertEqual([call.args[0] for call in encoder.save.call_args_list],
                             [str(target / "EXAMPLE-ONE"), str(target / "EXAMPLE-TWO")])

    def test_input_cannot_redirect_outputs_outside_the_selected_directory(self):
        for value in ("../escape", "..\\escape", "C:escape", ".."):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as temp:
                source = Path(temp) / "synthetic.txt"
                source.write_text(value + "\n", encoding="utf-8")
                with self.assertRaises(ValueError):
                    self.invoke(source, Path(temp) / "output")


if __name__ == "__main__":
    unittest.main()
