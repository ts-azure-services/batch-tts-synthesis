infra:
	./speech.sh

install:
	#conda create -n tts python=3.8 -y; conda activate tts
	pip install python-dotenv
	pip install requests
	pip install urllib3
