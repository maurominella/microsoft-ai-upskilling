## Environment preparation

1. Install Git from its [WEB site](https://git-scm.com/downloads), choosing your operating system

2. Open a git/bash command prompt, or make sure that git executable is in the path

3. ***CD*** into the base folder for your git repositories
If you do not have one, you may create a folder called `git_repos`

4. Use `git` to clone this repo locally:
```bash
git clone https://github.com/maurominella/genai_evaluation.git
```
or 
```bash
git clone git@github.com:maurominella/genai_evaluation.git
```

5. ***CD*** into `genai_evaluation` folder of the cloned repository: `cd genai_evaluation`

6. Duplicate the file `.env.example` into `credentials_my.env` and fill the right values into it.

7. **UV** installation (Python package & project manager)

- **Linux / macOS:**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Windows (PowerShell):**
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```


8. Verify that UV executable is in the path and runnable

Verify: `uv --version`. (uv also installs and manages Python for you — you do **not** need a separate Python install).



9. Create your Python Environment with UV

```bash
# 1. Make sure you are in the right folder

# 2. Initialise a uv project on Python 3.13
uv init . --python 3.13

# 3. Create the local virtual environment
uv venv

# 4. Activate it
source .venv/bin/activate        # Linux / macOS
.\.venv\Scripts\Activate.ps1   # Windows (PowerShell)

# 5. Install the shared dependencies (note --active + --prerelease=allow)
uv add --active -r requirements.txt --prerelease=allow

# 6. Confirm what got installed
uv pip list

# 7. On subsequent runs, reproduce the committed environment exactly
uv sync --active --frozen

# 8. Deactivate when finished
deactivate
```

> [!NOTE]
> **Why `--prerelease=allow`** — some libraries (e.g. the Microsoft **Agent Framework**) ship as preview releases; this flag lets uv install them. **Why `--active`** — it tells uv to use the virtual environment you just activated.

> [!TIP]
> Alternative to the activate/`--active` flow: prefix any command with `uv run` (e.g. `uv run python app.py`) and uv uses the project environment automatically. Both styles work — pick one and stay consistent.


### 10. Jupyter kernel (needed for notebook exercises)

Some exercises are delivered as Jupyter notebooks. Register a kernel so VS Code / Jupyter can select this environment. Use a name you'll recognise (for example: `genai_evaluation`).

```bash
# Register the current environment as a kernel
python -m ipykernel install --user --name genai_evaluation --display-name "Generative AI Evaluation (uv)"

# List installed kernels
jupyter kernelspec list

# Remove a kernel when no longer needed
jupyter kernelspec uninstall ai-labs
```

In VS Code, open the notebook → **Select Kernel** → choose **"Generative AI Evaluation (uv)"**.

---

To zip/unzip the labs folder:
- `zip -r labs.zip samples/`
- `unzip -o labs.zip`