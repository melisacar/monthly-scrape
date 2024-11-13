# DHMI Monthly Flights Data

This project automates the process of downloading, transforming, and saving monthly Excel files published on the General Directorate of State Airports Authority (DHMİ) statistics page. The data is parsed and stored in a PostgreSQL database.

- **Before Use:**
  - **Database connections** are different from main folder's.
  - **Class names** are different check before running models.py (Here is `Flights`)
  - **Table names** are different check before running models.py. (Here is `tum_ucuslar`)
  - Check before running.

- Built for checking.
- Scrapes from web (all data).
- Migrates to the postgres db.

## Error Handling

### Why the pg_config Error Occurred

The psycopg2-binary package needs pg_config (which is part of PostgreSQL development tools) to be available during installation when building from source. However, by using the psycopg2-binary version, you can bypass this requirement because the binary package is pre-compiled.

## Why Use a Virtual Environment?

The reason you need to use a virtual environment is that the system Python environment inside the container is "externally managed," meaning that installing packages directly could potentially break the system or lead to conflicts. Using a virtual environment isolates your dependencies from the system and ensures you don't interfere with the underlying system configuration.

Here’s a clear and simple set of instructions to resolve the issue and install psycopg2-binary inside your Docker container using a virtual environment:

1. Access the Running Docker Container
First, you need to access the running container. To do this, use the following command to open a shell inside the container:

```bash
docker exec -it my_postgres bash
```

1. Install Python3, pip, and venv (if not already installed)

Ensure that Python 3 and pip (Python's package installer) are installed. Additionally, to create a virtual environment, you need to install the python3-venv package.

Run the following commands inside the container:

```bash
apt-get update
apt-get install -y python3 python3-pip python3-venv
```

- python3: Installs Python 3 if it's not already available.
- python3-pip: Installs pip to manage Python packages.
- python3-venv: Installs the necessary tools for creating virtual environments.

1. Create a Virtual Environment
Now that you have the necessary tools installed, create a new virtual environment to isolate your Python dependencies.

Run the following command to create a virtual environment:

```bash
python3 -m venv /opt/myenv
```

This will create a new virtual environment in the /opt/myenv directory.

1. Activate the Virtual Environment

To use the virtual environment, you need to activate it. Run the following command:

```bash
source /opt/myenv/bin/activate
```

Once activated, your shell prompt will change, indicating that you are now working inside the virtual environment. For example, you might see something like (myenv) at the beginning of the prompt.

1. Install `psycopg2-binary` Inside the Virtual Environment

Now that the virtual environment is active, install `psycopg2-binary` (or any other dependencies you need) using `pip`:

```bash
pip install psycopg2-binary
```

This will install the package inside the virtual environment, avoiding conflicts with the system-wide Python environment.

1. Verify Installation

To verify that the package was successfully installed, you can run:

```bash
pip show psycopg2-binary
```

This command will show the details of the installed package, confirming that it is available in the virtual environment.

1. Deactivate the Virtual Environment (Optional)

Once you are done working with the virtual environment, you can deactivate it to return to the system Python environment:

```bash
deactivate
```
