import os
from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity

APP_ID = os.environ.get("MicrosoftAppId", "")
APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
SETTINGS = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

async def messages(request: web.Request) -> web.Response:
    body = await request.json()
    activity = Activity().deserialize(body)

    async def aux_func(turn_context: TurnContext):
        if activity.type == "message":
            reversed_text = activity.text[::-1]
            await turn_context.send_activity(reversed_text)

    await ADAPTER.process_activity(activity, "", aux_func)
    return web.Response(status=200)

APP = web.Application()
APP.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(APP, host="localhost", port=3978)
