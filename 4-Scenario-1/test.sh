#!/bin/sh

APINAME=flights-app
REGION=us-east-1

APIID=$(aws apigateway get-rest-apis --query "items[?name==\`${APINAME}\`].id" --output text --region ${REGION})
URL="https://${APIID}.execute-api.${REGION}.amazonaws.com/Prod/"

echo
echo "Finding flights by plane"
echo
curl "${URL}/flightsByPlane/?plane=747"
echo
echo "Finding airport by code"
echo
curl "${URL}/airportByCode/?code=MCO"
echo
echo "Finding airport by name"
echo
curl "${URL}/airportByName/?name=Orlando%20International%20Airport"
echo
echo "Finding flights by codes"
echo
curl "${URL}/flightsByCodes/?src=MCO&dst=FLL"
echo
echo "Finding outbound flights by airport"
echo
curl "${URL}/outboundByAirport/?code=MCO"
echo
