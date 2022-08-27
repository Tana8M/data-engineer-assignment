import os

from dagster import HookContext, failure_hook, success_hook
import traceback


def my_message_fn(context: HookContext) -> str:
    op_exception: BaseException = context.op_exception
    # print stack trace of exception
    traceback.print_tb(op_exception.__traceback__)

    return f"Op {context.op} failed!"


@failure_hook(required_resource_keys={"slack"})
def slack_message_on_failure(context):
    message = f"*Op* `{context.op.name}` _failed_ :cold_sweat: \n" \
              f"*Job* `{context.job_name}` _failed_ :fire:"
    context.resources.slack.chat_postMessage(channel=os.environ['SLACK_CHANNEL'], text=message)


@success_hook(required_resource_keys={"slack"})
def slack_message_on_success(context):
    message = f"*Job* `{context.job_name}` _finished successfully_ :tada::tada:"
    context.resources.slack.chat_postMessage(channel=os.environ['SLACK_CHANNEL'], text=message)