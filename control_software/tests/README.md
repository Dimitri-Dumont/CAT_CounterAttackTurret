# Component Test Scripts

This directory contains Python scripts for testing individual Raspberry Pi components of the CAT project.

## Usage

1. Clone the repository on your Raspberry Pi:

2. Navigate to the test directory:

```bash
cd CAT_CounterAttackTurret/control_software/tests
```


3. Run desired test:

```bash
python3 <test_script>.py
```

## Remote Testing

All tests can be run remotely via SSH on your local network:

```bash
ssh pi@<Raspberry Pi IP>
cd CAT_CounterAttackTurret/control_software/tests
python3 <test_script>.py
```


## Available Tests

Each `.py` file in this directory is a standalone test script for validating specific hardware components:
- `servo_test.py` - Tests servo motor functionality
- `camera_test.py` - Validates camera input
- etc
Note: Ensure all required hardware components are properly connected before running tests.
