"""Startup diagnostics retain the concrete cause without a native capture."""
import importlib
from types import SimpleNamespace

import pytest

from ok import OK
from ok.gui.StartController import StartController


def test_unsupported_frame_size_retains_dimensions_and_allowed_limits(monkeypatch):
    module = importlib.import_module('ok.gui.StartController')
    executor = SimpleNamespace(check_frame_and_resolution=lambda *_: (False, '1024x768'))
    monkeypatch.setattr(module.og, 'executor', executor)
    config = {'supported_resolution': {'allowed_ratios': ['16:9', '16:10', '43:18'],
              'force_ratio': True, 'min_size': (1280, 720)}}
    controller = SimpleNamespace(config=config, tr=lambda text: text, last_error=None)
    message = StartController.check_resolution(controller)
    assert controller.last_error == message
    assert '1024x768' in message and '1280x720' in message and '16:10' in message


def test_headless_runner_raises_concrete_startup_error():
    detail = 'Resolution 1024x768 check failed; minimum 1280x720'
    controller = SimpleNamespace(do_start=lambda *_args, **_kwargs: False, last_error=detail)
    app = SimpleNamespace(headless_app=SimpleNamespace(start_controller=controller))
    with pytest.raises(RuntimeError, match='1024x768') as error:
        OK.run_onetime_task(app, SimpleNamespace(name='offline task'))
    assert str(error.value) == detail
