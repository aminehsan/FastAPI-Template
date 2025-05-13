from uvicorn import run
from core.envs import FASTAPI

if __name__ == '__main__':
    if FASTAPI.run_development:
        print('Running in development mode...')

    run(
        app='config:app',
        host='0.0.0.0',
        port=FASTAPI.port,
        workers=FASTAPI.workers,
        reload=FASTAPI.reload
    )
