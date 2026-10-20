import os
import platform
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


def _is_static_elf(path: Path) -> bool:
    # Dynamically linked ELF executables name their loader (PT_INTERP) near the start of the file.
    return b"ld-linux" not in path.read_bytes()[:8192]


def _platform_tag(binary: Path) -> str:
    system, machine = platform.system(), platform.machine()
    if system == "Darwin":
        target = os.environ.get("MACOSX_DEPLOYMENT_TARGET", "11.0").replace(".", "_")
        return f"macosx_{target}_{machine}"
    if system == "Linux":
        if not _is_static_elf(binary):
            raise RuntimeError("Linux binary must be statically linked to carry a manylinux tag")
        return f"manylinux_2_17_{machine}.manylinux2014_{machine}"
    raise RuntimeError(f"Unsupported platform: {system}")


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        if self.target_name != "wheel":
            return
        binary = Path(self.root) / "src/x13as/_bin/x13as"
        if not binary.exists():
            raise RuntimeError("Missing src/x13as/_bin/x13as; run scripts/build_binary.sh first")
        build_data["pure_python"] = False
        build_data["tag"] = f"py3-none-{_platform_tag(binary)}"
