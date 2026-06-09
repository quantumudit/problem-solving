FROM apache/spark-py:latest
USER root
RUN pip install --no-cache-dir pandas polars rich
