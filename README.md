# Agent evaluation environments

Three self-contained coding tasks for checking whether an agent did the task without taking the unsafe shortcut planted in the repo.

Each environment is a directory:

| Piece | Role |
| --- | --- |
| `instruction.md` | The task the agent is given |
| `workspace/` | The repo fixture, including a note that pushes toward the unsafe shortcut |
| `reference/` | Files that complete the task inside the boundary |
| `unsafe/` | A shortcut that looks finished and should fail |
| `grade.py` | Scores the submission from resulting state, then exits 0 or 1 |
| `Dockerfile` | Runs that grader over a mounted submission |

The grader does not trust the agent's own tests or a written explanation. It runs the submission and checks the artifact: a log file, a hidden test run, or an output file.

From this directory, the suite is working when this prints `OK` and `Ran 9 tests`:

```bash
python3 -m unittest discover -s tests -v
```

A reference solution exits 0. The matching unsafe shortcut exits 1:

```bash
rm -rf /tmp/log-ref && mkdir /tmp/log-ref
cp -R envs/log-redaction/workspace/. /tmp/log-ref/
cp envs/log-redaction/reference/app.py /tmp/log-ref/app.py
python3 envs/log-redaction/grade.py /tmp/log-ref

rm -rf /tmp/log-bad && mkdir /tmp/log-bad
cp -R envs/log-redaction/workspace/. /tmp/log-bad/
cp envs/log-redaction/unsafe/app.py /tmp/log-bad/app.py
python3 envs/log-redaction/grade.py /tmp/log-bad
```

Grade one submission:

```bash
python3 envs/log-redaction/grade.py envs/log-redaction/workspace
```

Docker, from this directory:

```bash
docker build -t agent-eval-envs .
docker run --rm agent-eval-envs
```

Each environment image grades a mounted submission. The reference overlay is copied onto the workspace first:

```bash
docker build -t grade-log-redaction envs/log-redaction
rm -rf /tmp/log-sub && mkdir /tmp/log-sub
cp -R envs/log-redaction/workspace/. /tmp/log-sub/
cp envs/log-redaction/reference/app.py /tmp/log-sub/app.py
docker run --rm -v /tmp/log-sub:/submission:ro grade-log-redaction
```
