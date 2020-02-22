#!/bin/sh

APINAME=flights-app
REGION=us-east-1

APIID=$(aws apigateway get-rest-apis --query "items[?name==\`${APINAME}\`].id" --output text --region ${REGION})
URL="https://${APIID}.execute-api.${REGION}.amazonaws.com/Prod/"

echo ">>> Finding flights by plane\n"
curl "${URL}/flightsByPlane/?plane=747"

echo "\n\n>>> Finding airport by code\n"
curl "${URL}/airportByCode/?code=MCO"

echo "\n\n>>> Finding airport by name\n"
curl "${URL}/airportByName/?name=Orlando%20International%20Airport"

echo "\n\n>>> Finding flights by codes\n"
curl "${URL}/flightsByCodes/?src=MCO&dst=FLL"

echo "\n\n>>> Finding outbound flights by airport\n"
curl "${URL}/outboundByAirport/?code=MCO"
