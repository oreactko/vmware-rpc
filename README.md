# VMWareRPC

A Discord Rich Presence for VMware Workstation.

## Usage

### 1. Configure VMware REST API

Open a terminal in the VMware Workstation installation directory and run:

```sh
vmrest -C
```

Follow the prompts to configure the VMware REST API username and password.

### 2. Clone the repository

```sh
git clone <repository-url>
cd VMWareRPC
```
### 3. Create virtual environment
Using venv

```sh
python3.13 -m venv .venv
.\.venv\Scripts\activate
```

If you use `uv`:

```sh
uv venv --python 3.13
.\.venv\Scripts\activate
```

### 4. Install dependencies

Using pip:

```sh
pip install .
```

Or, if you use `uv`:

```sh
uv sync
```

### 5. Set credentials

Set the following environment variables:

```text
VMREST_USERNAME=<your-username>
VMREST_PASSWORD=<your-password>
```

### 6. Run

```sh
python main.py
```

If you're using `uv`:

```sh
uv run main.py
```
