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

# voice="en-US-JennyNeural"
# voice="ar-AE-FatimaNeural"
# New OpenAI voices
voice="en-US-FableMultilingualNeural"
sample:
	.venv/bin/python ./synthesis.py --voice=$(voice)

# Commit local branch changes
branch=$(shell git symbolic-ref --short HEAD)
now=$(shell date '+%F_%H:%M:%S' )
git-push:
	git add . && git commit -m "Changes as of $(now)" && git push -u origin $(branch)

git-pull:
	git pull origin $(branch)
