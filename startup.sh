# gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
uvicorn main:app --host=0.0.0.0 --port=3003