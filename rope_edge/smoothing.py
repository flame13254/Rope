from collections import deque


class SlidingWindow:
    """时间窗口内达标帧(status=1 且 conf>=阈值)占比 >= ratio 时输出 1。"""

    def __init__(self, window_sec, ratio, conf_thresh):
        self.window_sec = float(window_sec)
        self.ratio = float(ratio)
        self.conf_thresh = float(conf_thresh)
        self.buf = deque()  # (now, status, conf)

    def update(self, status, conf, now):
        self.buf.append((now, status, conf))
        cutoff = now - self.window_sec
        while self.buf and self.buf[0][0] < cutoff:
            self.buf.popleft()
        if not self.buf:
            return 0
        qualified = sum(1 for _, s, c in self.buf if s == 1 and c >= self.conf_thresh)
        return 1 if qualified / len(self.buf) >= self.ratio else 0
