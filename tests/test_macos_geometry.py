"""Offline display/stream lifecycle tests: no native helper or input is invoked."""
import io
import subprocess
import threading
import time
from types import SimpleNamespace

import pytest

from ok.device.capture_methods.macos import MacScreenCaptureMethod
from ok.device.interaction_methods.macos import MacForegroundInteraction
from ok.platform.macos.display import select_display
from ok.platform.macos.window import MacWindow


def make_window():
    window = MacWindow.__new__(MacWindow)
    window.window_id, window.pid = 12, 34
    window.x, window.y, window.width, window.height = 100, 50, 1200, 800
    window.display_id, window.display_scale = 1, 2.0
    window.capture_width = window.capture_height = 0
    window.helper = SimpleNamespace(command=lambda *args: ['fake-helper', *map(str, args)])
    window.do_update_window_size = lambda: None
    return window


def make_capture():
    window = make_window()
    capture = MacScreenCaptureMethod(window, threading.Event())
    capture.stop_on_geometry_change = False
    return capture


def fake_processes(monkeypatch, capture):
    events, processes = [], []

    class Process:
        def __init__(self, *_args, **_kwargs):
            assert not any(process.alive for process in processes)
            self.alive = True
            self.stdout, self.stderr = io.BytesIO(), io.BytesIO()
            processes.append(self)
            events.append('start')

        def poll(self):
            return None if self.alive else 0

        def terminate(self):
            events.append('terminate')
            self.alive = False

        def wait(self, **_kwargs):
            events.append('wait')
            return 0

    monkeypatch.setattr(subprocess, 'Popen', Process)
    monkeypatch.setattr(capture, '_read_frames', lambda *_: None)
    monkeypatch.setattr(capture, '_read_stderr', lambda *_: None)
    return events, processes


@pytest.mark.parametrize('change', ['position', 'size', 'scale', 'display', 'window'])
def test_changed_capture_target_closes_previous_stream_before_rebuild(monkeypatch, change):
    capture = make_capture()
    events, processes = fake_processes(monkeypatch, capture)
    assert capture._start_stream()
    signature = capture._stream_target_signature
    attribute, value = {'position': ('x', -1200), 'size': ('width', 1600),
                        'scale': ('display_scale', 1.0), 'display': ('display_id', 2),
                        'window': ('window_id', 13)}[change]
    setattr(capture.mac_window, attribute, value)
    assert capture._start_stream()
    assert capture._stream_target_signature != signature
    assert events == ['start', 'terminate', 'wait', 'start']
    assert sum(process.alive for process in processes) == 1
    capture.close()


def test_concurrent_frame_start_requests_create_only_one_stream(monkeypatch):
    capture = make_capture()
    events, processes = fake_processes(monkeypatch, capture)
    capture.mac_window.helper.command = lambda *_: time.sleep(.02) or ['fake-helper']
    workers = [threading.Thread(target=capture._start_stream) for _ in range(4)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join(timeout=2)
        assert not worker.is_alive()
    assert events == ['start']
    assert len(processes) == 1
    capture.close()


def test_stale_coordinates_are_rejected_even_before_next_capture_request():
    capture = make_capture()
    window = capture.mac_window
    window.update_frame_size(2400, 1600)
    capture._frame_target_signature = window.capture_target_signature
    assert capture.get_abs_cords(1200, 800) == (700, 450)
    window.x = -1200
    with pytest.raises(RuntimeError, match='fresh frame'):
        capture.get_abs_cords(1200, 800)


def test_beta_policy_stops_with_readable_error_before_rebuilding(monkeypatch):
    capture = make_capture()
    capture.stop_on_geometry_change = True
    events, _ = fake_processes(monkeypatch, capture)
    capture._start_stream()
    capture.mac_window.display_scale = 1.0
    with pytest.raises(RuntimeError, match='重新检查队伍'):
        capture.do_get_frame()
    assert capture.geometry_error
    assert events == ['start', 'terminate', 'wait']
    with pytest.raises(RuntimeError, match='本轮已停止'):
        capture.get_abs_cords(10, 10)


def test_geometry_failure_blocks_new_input_but_allows_mouse_and_key_release():
    capture = make_capture()
    capture.stop_on_geometry_change = True
    window = capture.mac_window
    window.update_frame_size(2400, 1600)
    window.is_foreground = lambda: True
    capture._size = (2400, 1600)
    capture._frame_target_signature = window.capture_target_signature
    commands = []
    window.helper.run = lambda *args, **kwargs: commands.append(args)
    interaction = MacForegroundInteraction(capture, window, use_direct_mouse=False, use_direct_keys=False)
    interaction.send_key_down('alt')
    interaction.mouse_down(100, 100)
    window.display_scale = 1.0
    with pytest.raises(RuntimeError, match='本轮已停止'):
        interaction.click(100, 100)
    with pytest.raises(RuntimeError, match='本轮已停止'):
        interaction.send_key('e')
    interaction.mouse_up()
    interaction.send_key_up('alt')
    assert commands[-2][0:2] == ('mouse', 'up')
    assert commands[-1] == ('key', 'up', 'alt')
    assert len(commands) == 4


def test_largest_overlap_selects_display_including_negative_vertical_coordinates():
    displays = [{'id': 1, 'scale': 2.0, 'bounds': (0, 0, 1512, 982)},
                {'id': 2, 'scale': 1.0, 'bounds': (-1920, -1080, 1920, 1080)}]
    assert select_display((-1800, -1000, 1600, 900), displays)['id'] == 2
    assert select_display((-100, -20, 1200, 800), displays)['id'] == 1
    assert select_display((0, 0, 10, 10), []) is None


@pytest.mark.parametrize('scale', [1.0, 1.5, 2.0])
def test_pixel_coordinates_map_to_negative_origin_at_each_capture_scale(scale):
    window = make_window()
    window.x, window.y = -1200, -800
    window.update_frame_size(round(window.width * scale), round(window.height * scale))
    assert window.get_abs_cords(window.capture_width / 2, window.capture_height / 2) == (-600, -400)
