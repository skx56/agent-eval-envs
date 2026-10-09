FROM python:3.12-slim
WORKDIR /eval
COPY grade.py /eval/grade.py
COPY hidden /eval/hidden
ENTRYPOINT ["python", "/eval/grade.py"]
CMD ["/submission"]
