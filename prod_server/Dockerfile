FROM python:3.6
ADD requirements.txt /star_predict/requirements.txt
WORKDIR /star_predict/
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["./app.py"]
