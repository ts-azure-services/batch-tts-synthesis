import os, requests
import argparse
from dotenv import load_dotenv

def load_variables():
    """Load access variables"""
    env_var=load_dotenv('./variables.env')
    auth_dict = {"speech_key":os.environ['SPEECH_KEY'],"speech_location":os.environ['SPEECH_LOCATION']}
    return auth_dict

def get_files(request_id, region, key):
    url=f'https://{region}.customvoice.api.speech.microsoft.com/api/texttospeech/v3.0/longaudiosynthesis/{request_id}/files'
    header = {'Ocp-Apim-Subscription-Key': key}
    response = requests.get(url, headers=header)
    print('response.status_code: %d' % response.status_code)
    print(response.text)

def main():
    parser = argparse.ArgumentParser(description='Long audio tool to submit voice synthesis requests.')
    parser.add_argument('-requestId', action="store", nargs='+', dest="requestId", help='the submitted request id')
    args = parser.parse_args()

    if args.requestId:
        var = load_variables()
        get_files(request_id=args.requestId[0],
                region=var['speech_location'], 
                key=var['speech_key']
                )
    else:
        print("Please provide the request id from the submitted request.")

if __name__ == "__main__":
    main()
