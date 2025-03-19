import asyncio
import uvicorn

def shutdown_rest_of_app(_, __):
    raise KeyboardInterrupt


def main():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        web_config = uvicorn.Config(
            "app:app", #Сюда пишете ".py файл:app
            host="127.0.0.1",
            port=1404,
            loop="asyncio",
            workers=4,
        )

        web_server = uvicorn.Server(config=web_config)
        loop.create_task(web_server.serve())
        loop.run_forever()
    except KeyboardInterrupt:
        print("Caught Ctrl+C. Exiting gracefully.")

if __name__ == "__main__":
    main()