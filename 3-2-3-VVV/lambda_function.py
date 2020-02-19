import json
import urllib.parse

import boto3

from mutagen.mp4 import MP4

dynamodb = boto3.resource("dynamodb")
table_name = "MusicTagger"
table = dynamodb.Table(table_name)
s3 = boto3.client("s3")


def lambda_handler(event, context):

    try:
        print("Received event: " + json.dumps(event))
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(
            event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
        )
        print(f"Bucket: {bucket}")
        print(f"Key: {key}")
        s3.download_file(bucket, key, f"/tmp/{key}")
    except Exception as e:
        print(e)

    # extract tags
    try:
        audio = MP4(f"/tmp/{key}")
        tags = {}
        tag_list = audio.pprint().split("\n")
        print(tag_list)
        for _ in tag_list:
            kv = _.split("=")
            try:
                print("key:" + kv[0])
                print("value:" + kv[1])
                tags[kv[0]] = kv[1]
            except IndexError:
                pass
        print(tags)
    except Exception as e:
        print(e)

    try:
        item = {}
        item["artist"] = tags.get("aART") or tags.get("xa9ART")
        item["album"] = tags.get("\xa9alb")
        item["title"] = tags.get("\xa9nam")
        item["genre"] = tags.get("\xa9gen")
        item["encoder"] = tags.get("\xa9too")
        item["artistalbum"] = item["artist"] + "#" + item["album"]
        item["SK"] = item["artistalbum"] + "#" + item["title"]
        item["tags"] = tags
        item["s3_path"] = f"{bucket}/{key}"
        print(item)

        # write to DynamoDB
        table.put_item(Item=item)
    except Exception as e:
        print(e)
