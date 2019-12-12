from typing import List


class IOLoggerEntry:
    def __init__(self, type: str, contents: str):
        self.type = type
        self.contents = contents


class IOLogger:
    def __init__(self):
        super().__init__()
        self._log: List[IOLoggerEntry] = []
        self._output_buffer = ""

    def log_input(self, text: str) -> None:
        self._close_output()
        self._log.append(IOLoggerEntry("input", text))

    def log_output(self, text: str) -> None:
        self._output_buffer += text

    def dump(self) -> List[IOLoggerEntry]:
        self._close_output()
        return self._log.copy()

    def dump_input(self) -> List[str]:
        return [x.contents for x in self._log if x.type == "input"]

    def _close_output(self) -> None:
        if len(self._output_buffer):
            self._log.append(IOLoggerEntry("output", self._output_buffer))
            self._output_buffer = ""

