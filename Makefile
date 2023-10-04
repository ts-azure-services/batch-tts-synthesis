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

# Submit the request
# May have to manually cancel on this request since it keeps looping
# The voiceId is part of the pre-built voices and can be queried separately
sample_txt_file="./inputs/sample.txt"
speech_location="westus2"
locale="en-US"
submit-request:
	python ./inputs/voiceclient.py \
		--submit -voiceId 4c9c2252-b3e1-4af4-9596-14ab459cb93d \
		-key <input speech key> \
		-region $(speech_location) \
		-file $(sample_txt_file) \
		-locale $(locale) \
		--concatenateResult

# Check on the request
check_request:
	python ./inputs/voiceclient.py --voicesynthesisbyid \
		-key <input speech key> \
		-region <input speech location> \
		-synthesisId <input request ID>

# Get the audio file and text output
# This will provide links to download the script, and the audio files
retrieve-audio-file:
	python ./inputs/get_audio_file.py -requestId <input request ID>

synthesize-jenny:
	python ./inputs/synthesis.py --voice="en-US-JennyNeural"

synthesize-fatima:
	python ./inputs/synthesis.py --voice="ar-AE-FatimaNeural"
