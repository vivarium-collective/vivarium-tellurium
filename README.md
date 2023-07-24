# Vivarium-Tellurium Process

Visit [the Vivarium Core
documentation](https://vivarium-core.readthedocs.io/) to learn how to
use the core Vivarium engine to create computational biology models.
Check out the
[getting started](https://vivarium-core.readthedocs.io/en/latest/getting_started.html)
guide of the documentation.

---

# Vivarium-tellurium

This codebase serves as a Vivarium interface for the Tellurium bio-simulation package.

By fitting a simulator package to the Vivarium `vivarium.core.processes.Process()` interface, you
allow for this process type to be involved in larger compositions and orchestrations.

## Installation

### _Local Installation with `pip`_:

1. create a virtual environment for Python (recommended).
2. Activate the aforementioned Python environment.
3. `cd vivarium-tellurium`, which is the root of the repo.
4. `pip install -e .` to install all of the required deps into your environment.
