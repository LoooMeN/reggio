FROM python:3-onbuild
EXPOSE 5000
ENV FLASK_APP=start.py
ENV FLASK_ENV=development
ENV PYTHONDONTWRITEBYTECODE=1
CMD ["flask", "run", "--host", "0.0.0.0"]