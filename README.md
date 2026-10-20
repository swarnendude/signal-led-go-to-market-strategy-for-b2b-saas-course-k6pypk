# signal-led-go-to-market-strategy-for-b2b-saas-course-k6pypk

Code for the course "Signal-Led Go-To-Market Strategy for B2B SaaS"

Each lesson's code sits in its own folder, with its tests. On every push, GitHub Actions runs `pytest -q` in the folders that push changed; run the workflow by hand (Actions → tests → Run workflow) to test every folder.

To run one folder yourself (Python 3.12):

```
cd <folder>
python -m pip install pytest
python -m pytest -q
```
