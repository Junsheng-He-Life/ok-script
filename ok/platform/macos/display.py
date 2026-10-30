"""Select a capture display using Quartz's global, top-left point coordinates."""


def select_display(rect, displays):
    """Prefer the display containing the largest part of a window, then its centre."""
    x, y, width, height = rect
    cx, cy = x + width / 2, y + height / 2

    def rank(display):
        dx, dy, dw, dh = display['bounds']
        overlap = max(0, min(x + width, dx + dw) - max(x, dx)) * max(
            0, min(y + height, dy + dh) - max(y, dy))
        distance = (cx - (dx + dw / 2)) ** 2 + (cy - (dy + dh / 2)) ** 2
        return overlap, -distance

    return max(displays, key=rank, default=None)


def screen_records():
    """Read display scale without opening a capture stream or posting input."""
    import AppKit
    import Quartz

    records = []
    for screen in AppKit.NSScreen.screens():
        display_id = int(screen.deviceDescription()['NSScreenNumber'])
        bounds = Quartz.CGDisplayBounds(display_id)
        records.append({'id': display_id, 'scale': float(screen.backingScaleFactor()),
                        'bounds': (float(bounds.origin.x), float(bounds.origin.y),
                                   float(bounds.size.width), float(bounds.size.height))})
    return records
