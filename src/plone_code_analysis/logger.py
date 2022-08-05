import logging
import os
import re


LOG_LEVEL = {
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "WARNING": logging.WARNING,
}


level = LOG_LEVEL.get(os.environ.get("LOG_LEVEL"), LOG_LEVEL["INFO"])

logging.basicConfig(level=level, format="%(message)s")


PREFIXES = {
    "debug": "\x1b[1;33m",
    "warning": "\x1b[1;33m",
    "info": "\x1b[1;34m",
    "hint": "\x1b[3;35m",
    "success": "\x1b[1;32m",
    "error": "\x1b[1;31m",
}


class FancyLogger:

    TERMINATOR = "\x1b[0m"
    HEADER_DELIMITER = "="
    REPLACEMENTS = (
        (r"\/github\/workspace\/", ""),
        (r"PosixPath\('([^']*)'\)", r"\1"),
    )

    def __init__(self) -> None:
        self.logger = logging.getLogger("plone-code-analysis")

    def __getattr__(self, attr):
        """Catch all method."""
        return getattr(self.logger, attr)

    def _redact_msg(self, msg: str) -> str:
        """Clean up msg to be logged."""
        for pattern, replace in self.REPLACEMENTS:
            msg = re.sub(pattern, replace, msg)
        return msg

    def _log(self, level, msg, *args, **kwargs):
        fancy = kwargs.get("fancy", True)
        header_level = kwargs.get("header", None)
        kwargs = {k: v for k, v in kwargs.items() if k not in ("fancy", "header")}
        msg = self._redact_msg(msg)
        if fancy:
            if header_level:
                msg_len = len(msg)
                header = self.HEADER_DELIMITER * msg_len
                msg = f"{msg}\n{header}"
                msg = f"{header}\n{msg}" if header_level == 1 else msg
                msg = f"\n{msg}"
            prefix = PREFIXES.get(level, PREFIXES["info"])
            msg = f"{prefix}{msg}{self.TERMINATOR}"

        method = getattr(self.logger, level, getattr(self.logger, "info"))
        method(msg, *args, **kwargs)

    def success(self, msg, *args, **kwargs):
        """Info"""
        self._log("success", msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """Info"""
        self._log("info", msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """Debug"""
        self._log("debug", msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """Error"""
        self._log("error", msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """Warning"""
        self._log("warning", msg, *args, **kwargs)


logger = FancyLogger()
