venv_setup:
	rm -rf .venv
	python3.11 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -r ./requirements.txt
	# source .tutorial_venv/bin/activate # not possible with Makefile

# Run the command below, and manually input your subscription ID once done
# Afer that, create a speech resource through the setup file
initialize:
	echo "SUB_ID=<input subscription_id>" > sub.env

setup:
	./setup.sh

synthesize-jenny:
	python ./inputs/synthesis.py --voice="en-US-JennyNeural"

synthesize-fatima:
	python ./inputs/synthesis.py --voice="ar-AE-FatimaNeural"
