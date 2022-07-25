
import sys
import types
from importlib import util
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

from datamodel_code_generator.__main__ import main as pydantic_code_gen

from .exceptions import FailedLoadModelModule
from .types import JsonStr


def _load_module(module_path: str) -> Optional[types.ModuleType]:
    """Load module from path to the var"""
    spec = util.spec_from_file_location(
        'new_model',
        module_path,
    )
    if not spec or not spec.loader: 
        return None
    mod = util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def gen_target_module(target_schema: JsonStr) -> types.ModuleType:    
    with TemporaryDirectory() as gen_dir:
        input_file: Path = Path(gen_dir) / "schema.json"
        with open(input_file, 'w') as w:
            w.write(target_schema)
        output_file: Path = Path(gen_dir) / 'model.py'
        pydantic_code_gen(
            [
                '--input',
                str(input_file),
                '--output',
                str(output_file),
                '--input-file-type',
                'jsonschema',
            ]
        )
        sys.path.append(gen_dir)
        _module = _load_module(str(output_file))
        if not _module:
            raise FailedLoadModelModule(str(output_file))
        return _module
