# VMWareRPC

A Discord Rich Presence for VMware Workstation.

## Usage

### 1. Configure VMware REST API

Open a terminal in the VMware Workstation installation directory and run:

```cmd
vmrest -C
```

Follow the prompts to configure the VMware REST API username and password.

### 2. Clone the repository

```cmd
git clone <repository-url>
cd VMWareRPC
```

### 3. Install dependencies

Using pip:

```cmd
pip install .
```

Or, if you use `uv`:

```cmd
uv sync
```

### 4. Set credentials

Set the following environment variables:

```text
VMREST_USERNAME=<your-username>
VMREST_PASSWORD=<your-password>
```

### 5. Run

```cmd
python main.py
```

If you're using `uv`:

```cmd
uv run main.py
```
