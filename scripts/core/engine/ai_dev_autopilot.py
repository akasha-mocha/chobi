import time

from scripts.utils.logger import get_logger

from scripts.core.engine.dev_cycle import DevCycle
from scripts.metrics.metrics_collector import MetricsCollector
from scripts.safety.failure_recovery import FailureRecovery


class AIDevAutopilot:

    """
    Autonomous AI Development Loop
    """

    def __init__(self):

        self.logger = get_logger("ai_dev_autopilot")

        self.dev_cycle = DevCycle()

        self.metrics = MetricsCollector()

        self.recovery = FailureRecovery()

        self.running = True

    def run_cycle(self):

        try:

            self.dev_cycle.run()

        except Exception as e:

            self.logger.error(f"Cycle failed: {e}")

            self.recovery.handle_failure(e)

    def collect_metrics(self):

        try:

            self.metrics.collect()

        except Exception:

            pass

    def loop(self):

        self.logger.info("AI Dev Autopilot started")

        while self.running:

            self.run_cycle()

            self.collect_metrics()

            time.sleep(5)

    def stop(self):

        self.logger.info("Autopilot stopping")

        self.running = False