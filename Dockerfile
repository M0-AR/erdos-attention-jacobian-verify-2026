FROM python:3.12-slim
WORKDIR /repo
COPY pyproject.toml ./
RUN pip install --no-cache-dir numpy sympy networkx pandas requests pyyaml pytest
COPY src/ ./src/
COPY benchmarks/ ./benchmarks/
COPY experiments/ ./experiments/
COPY data/ ./data/
ENV PYTHONPATH=/repo/src PYTHONDONTWRITEBYTECODE=1
CMD ["python", "experiments/run_all.py", "--out", "results"]
