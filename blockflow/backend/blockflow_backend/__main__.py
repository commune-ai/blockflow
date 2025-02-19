import multiprocessing
import platform

from blockflow_backend.main import create_app

import typer
from fastapi.staticfiles import StaticFiles
from pathlib import Path


def get_number_of_workers(workers=None):
    if workers == -1:
        workers = (multiprocessing.cpu_count() * 2) + 1
    return workers


def serve(
    workers: int = 1,
    timeout: int = 60,
):
    app = create_app()
    # get the directory of the current file
    path = Path(__file__).parent
    static_files_dir = path / "frontend"
    app.mount(
        "/",
        StaticFiles(directory=static_files_dir, html=True),
        name="static",
    )

    host = "127.0.0.1"
    port = 5003
    options = {
        "bind": f"{host}:{port}",
        "workers": get_number_of_workers(workers),
        "worker_class": "uvicorn.workers.UvicornWorker",
        "timeout": timeout,
    }

    if platform.system() == "Darwin":
        # Run using uvicorn on MacOS
        import uvicorn

        uvicorn.run("main:app", host=host, port=port, log_level="info", reload=True, workers=2)
    else:
        from blockflow_backend.server import blockflowApplication

        blockflowApplication(app, options).run()


def main():
    typer.run(serve)


if __name__ == "__main__":
    main()
