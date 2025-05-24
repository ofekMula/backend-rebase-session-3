# Backend Rebase Session 3



## Project Setup

### Prerequisites

Ensure you have the following installed:
- [Python 3.10 or above](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv)
- [Docker](https://docs.docker.com/get-docker/) (if using containers)

### Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/ofekMula/backend-rebase-session-2.git
   cd backend-rebase-session-2
   ```

2. **Install Dependencies**:
   ```sh
      ./scripts/installer.sh
   ```
   - Install uv
   - Create virtual environment
   - Install service dependencies
   - install pre commit


### Running the Service

**Activate the Virtual Environment**:
   ```sh
   source .venv/bin/activate
   ```

**Run the main application**:
```sh
python -m app
```

### Development

#### Pre-commit Hooks
To set up Git pre-commit hooks:
```sh
pre-commit install
```

#### Linting & Formatting
```sh
ruff check .
ruff format .
```

#### Running Tests
```sh
pytest tests/
```
