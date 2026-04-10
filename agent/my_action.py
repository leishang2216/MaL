import json
import random
import time

from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context


def _to_non_negative_int(value, fallback):
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return fallback


def parse_wait_config(raw_param):
    if isinstance(raw_param, str):
        if raw_param.strip():
            try:
                raw_param = json.loads(raw_param)
            except json.JSONDecodeError:
                raw_param = {}
        else:
            raw_param = {}

    if not isinstance(raw_param, dict):
        raw_param = {}

    fixed_seconds = _to_non_negative_int(raw_param.get("fixed_seconds"), 10)
    min_seconds = _to_non_negative_int(raw_param.get("min_seconds"), fixed_seconds)
    max_seconds = _to_non_negative_int(raw_param.get("max_seconds"), max(fixed_seconds, min_seconds))

    return {
        "mode": str(raw_param.get("mode", "fixed")).lower(),
        "fixed_seconds": fixed_seconds,
        "min_seconds": min_seconds,
        "max_seconds": max_seconds,
    }


def compute_wait_seconds(config, generator=None):
    normalized = parse_wait_config(config)

    if normalized["mode"] == "random":
        lower = min(normalized["min_seconds"], normalized["max_seconds"])
        upper = max(normalized["min_seconds"], normalized["max_seconds"])
        rng = generator or random
        return rng.randint(lower, upper)

    return normalized["fixed_seconds"]


@AgentServer.custom_action("sunflower_wait")
class SunflowerWaitAction(CustomAction):

    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> bool:
        seconds = compute_wait_seconds(argv.custom_action_param)
        print(f"sunflower_wait: sleep {seconds}s")
        time.sleep(seconds)

        return True
