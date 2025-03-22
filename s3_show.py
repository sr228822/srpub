#!/usr/bin/env python

import boto3
import os
import argparse
from pathlib import Path
from PIL import Image
from botocore.exceptions import ClientError

from srutils import cmd, log

s3 = boto3.client("s3")
base_tempdir = Path("/tmp/")


def parse_s3_uri(uri: str) -> tuple[str, str]:
    """Parse S3 URI into bucket name and key."""
    assert uri.startswith("s3://"), f"Not a uri: {uri}"
    uri = uri.replace("s3://", "")
    bucket, *key_parts = uri.split("/")
    key = "/".join(key_parts)
    return bucket, key


def download_from_s3(bucket_name: str, s3_key: str, local_path: str):
    """Download s3 object to a specific path"""
    try:
        s3.download_file(bucket_name, s3_key, local_path)
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            log.warning(f"File Does not exist: s3://{bucket_name}/{s3_key}")
            return False
        else:
            raise
    return True


def get_etag(bucket_name, s3_key):
    response = s3.head_object(Bucket=bucket_name, Key=s3_key)
    return response.get("ETag").strip('"')


def get_s3_cached(bucket_name, s3_key, use_cache=True, check_etag=True):
    """Download s3 object to tempdir with caching"""
    local_path = base_tempdir / "s3" / bucket_name / s3_key
    local_path.parent.mkdir(parents=True, exist_ok=True)
    in_cache = use_cache and os.path.exists(local_path)

    etag_path = f"{local_path}.etag"
    remote_etag = None
    if in_cache and check_etag:
        if not os.path.exists(etag_path):
            in_cache = False
        else:
            local_etag = open(etag_path, "r").read().strip()
            remote_etag = get_etag(bucket_name, s3_key)
            if local_etag != remote_etag:
                log.debug("S3 object is cached but etag differs")
                in_cache = False

    if in_cache:
        log.debug(f"S3 object already downloaded: {local_path}")
        return local_path

    # Download direct from s3
    res = download_from_s3(bucket_name, s3_key, local_path)
    if not res:
        return None

    # Write etag to local path
    if not remote_etag:
        remote_etag = get_etag(bucket_name, s3_key)
    open(etag_path, "w").write(remote_etag)

    return local_path


def list_s3(bucket_name: str, prefix: str, recursive=False):
    """List s3 objects in path"""
    if recursive:
        # For recursive listing, we just use the prefix as is
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if "Contents" not in response:
            return []

        return [obj["Key"] for obj in response["Contents"]]
    else:
        # For non-recursive listing, we need to use a delimiter and only show objects at the current level
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter="/")
        result = []

        # Add common prefixes (folders)
        if "CommonPrefixes" in response:
            result.extend([prefix["Prefix"] for prefix in response["CommonPrefixes"]])

        # Add objects at this level
        if "Contents" in response:
            for obj in response["Contents"]:
                key = obj["Key"]
                # Only include objects at the current level, not in subfolders
                if (
                    not prefix
                    or key == prefix
                    or (
                        key.startswith(prefix)
                        and key.replace(prefix, "").count("/") <= 1
                        and not key.replace(prefix, "").startswith("/")
                    )
                ):
                    result.append(key)

        return result


def main():
    parser = argparse.ArgumentParser(description="Show an s3 object")
    parser.add_argument("uri", help="S3 uri")
    parser.add_argument("--verbose", action="store_true", help="print all files")
    parser.add_argument(
        "--recursive", "-r", action="store_true", help="list recursively"
    )
    args = parser.parse_args()

    uri = args.uri
    bucket, key = parse_s3_uri(uri)
    log.debug(f"{bucket=} {key=}")
    if not key or key.endswith("/"):
        log.info(f"\n{uri}:")
        for item in list_s3(bucket, key, recursive=args.recursive):
            log.info(item)
        return

    local_path = str(get_s3_cached(bucket, key))

    if str(local_path).endswith(".png"):
        img = Image.open(local_path)
        img.show()
    else:
        cmd(f"cat {local_path}", noisy=True)


if __name__ == "__main__":
    main()
