# text-to-speech-long-audio
A repo to collect some artifacts to process a raw text file and get audio output using one of Azure's
pre-built voices. This is very helpful to create audio outputs for material when an acoustic medium is
preferred. Attribution to the code files present
[here](https://github.com/Azure-Samples/Cognitive-Speech-TTS/tree/master/CustomVoice-API-Samples/Python#note),
with the main documentation
[here](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/long-audio-api). A
`sample.txt` and a `sample.wav` file is included to demonstrate the outputs.

## Sample Bash Commands

```bash
# Submit the request
# May have to manually cancel on this request since it keeps looping
# The voiceId is part of the pre-built voices and can be queried separately
python voiceclient.py \
--submit -voiceId 4c9c2252-b3e1-4af4-9596-14ab459cb93d \
-key <input speech key> \
-region <input speech location> \
-file ./sample.txt \
-locale en-US \
--concatenateResult
```

```bash
# Check on the request
python voiceclient.py --voicesynthesisbyid \
-key <input speech key> \
-region <input speech location> \
-synthesisId <input request ID>
```

```bash
# Get the audio file and text output
# This will provide links to download the script, and the audio files
python get_audio_file.py -requestId <input request ID>
```
