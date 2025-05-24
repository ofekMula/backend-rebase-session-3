# Backend Rebase Session 3

## HTTP File Server
This service provides a simple HTTP-based interface for storing, retrieving, and deleting binary files (blobs). Each blob is uniquely identified by an ID and is stored alongside optional custom headers.

### Features
- Upload (POST /blobs/{blob_id}): Stores a file with the given ID and headers. Files are written in chunks to avoid memory overhead. Metadata (including headers) is stored alongside the file.

- Download (GET /blobs/{blob_id}): Retrieves the stored blob and its associated metadata. Content is returned as a base64-encoded string.

- Delete (DELETE /blobs/{blob_id}): Removes both the blob and its metadata.

- Chunked writes: Files are saved in small chunks to ensure low memory usage and safe handling of large uploads.

- Storage metadata: Tracks used disk space, total blob count, and blob-to-directory mappings in a metadata file (storage_meta.json) for recovery and quota enforcement.

### Full Requirements
https://course.ronklein.co.il/03-http-blob-server/

## Project Setup

### Prerequisites

Ensure you have the following installed:
- [Python 3.10 or above](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv)
- [Docker](https://docs.docker.com/get-docker/) (if using containers)

### Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/ofekMula/backend-rebase-session-3.git
   cd backend-rebase-session-3
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
