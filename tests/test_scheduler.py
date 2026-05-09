from unittest.mock import patch
from apscheduler.triggers.cron import CronTrigger
from bot.handlers.periodic_handlers import register_22_job

@patch("bot.handlers.periodic_handlers.scheduler")
def test_register_22_job(scheduler_mock):

    register_22_job()
    scheduler_mock.add_job.assert_called_once()
    args, kwargs = scheduler_mock.add_job.call_args

    assert kwargs["id"] == "22_notifications"
    assert kwargs["replace_existing"] is True

    trigger = kwargs["trigger"]
    assert isinstance(trigger, CronTrigger)
