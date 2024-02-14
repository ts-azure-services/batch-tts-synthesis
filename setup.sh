#!/bin/bash
#Script to provision Cognitive Services account
grn=$'\e[1;32m'
end=$'\e[0m'

# Start of script
SECONDS=0
printf "${grn}Starting creation of speech service...${end}\n"

# Source subscription ID, and prep config file
source sub.env
sub_id=$SUB_ID

# Set the default subscription 
az account set -s $sub_id

# Create the resource group, location
number=$[ ( $RANDOM % 10000 ) + 1 ]
resourcegroup='cs'$number
speechservice='cs'$number'speech'
location='swedencentral'

printf "${grn}Starting creation of resource group...${end}\n"
rgCreate=$(az group create --name $resourcegroup --location $location)
printf "Result of resource group create:\n $rgCreate \n"

## Create speech service
printf "${grn}Creating the speech service...${end}\n"
speechServiceCreate=$(az cognitiveservices account create \
	--name $speechservice \
	-g $resourcegroup \
	--kind 'SpeechServices' \
	--sku S0 \
	--location $location \
	--yes)
printf "Result of speech service create:\n $speechServiceCreate \n"

## Retrieve key from cognitive services
printf "${grn}Retrieve keys & endpoints for speech service...${end}\n"
speechKey=$(az cognitiveservices account keys list -g $resourcegroup --name $speechservice --query "key1")
speechEndpoint=$(az cognitiveservices account show -g $resourcegroup --n $speechservice --query "properties.endpoint")

speechKey=$(sed -e 's/^"//' -e 's/"$//' <<<"$speechKey")
speechEndpoint=$(sed -e 's/^"//' -e 's/"$//' <<<"$speechEndpoint")

# Create environment file 
printf "${grn}WRITING OUT ENVIRONMENT VARIABLES...${end}\n"
configFile='variables.env'
printf "RESOURCE_GROUP=$resourcegroup \n"> $configFile
printf "SPEECH_KEY=$speechKey \n">> $configFile
printf "SPEECH_LOCATION=$location \n">> $configFile
printf "SPEECH_ENDPOINT=$speechEndpoint \n">> $configFile
