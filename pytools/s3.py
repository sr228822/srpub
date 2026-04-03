#!/usr/bin/env python3

import sys
import boto3
import os
import logging
import argparse
from pathlib import Path
from PIL import Image
from botocore.exceptions import ClientError

from srutils import cmd, log

logging.getLogger("botocore").setLevel(logging.WARNING)
s3 = boto3.client("s3")
base_tempdir = Path("/tmp/")


def parse_s3_path(path: str) -> tuple[str, str]:
    """Parse s3 path into bucket and key. Accepts s3://b/k, /b/k, or b/k."""
    path = path.removeprefix("s3://").lstrip("/")
    bucket, *key_parts = path.split("/")
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
    print(f"Downloading s3://{bucket_name}/{s3_key}...", file=sys.stderr)
    res = download_from_s3(bucket_name, s3_key, local_path)
    if not res:
        return None

    # Write etag to local path
    if not remote_etag:
        remote_etag = get_etag(bucket_name, s3_key)
    open(etag_path, "w").write(remote_etag)

    return local_path


def human_size(nbytes):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(nbytes) < 1024:
            return f"{nbytes:.1f}{unit}" if unit != "B" else f"{nbytes}B"
        nbytes /= 1024
    return f"{nbytes:.1f}PB"


def format_obj(obj, prefix=""):
    date = obj["LastModified"].strftime("%Y-%m-%d %H:%M")
    name = obj["Key"].removeprefix(prefix)
    return f"{date}  {human_size(obj['Size']):>10s}  {name}"


def list_s3(bucket_name: str, prefix: str, recursive=False, full_path=False):
    """List s3 objects in path."""
    strip = "" if full_path else prefix
    if recursive:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if "Contents" not in response:
            return []
        return [format_obj(obj, strip) for obj in response["Contents"]]
    else:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter="/")
        result = []

        if "CommonPrefixes" in response:
            result.extend(
                [
                    f"{'':>28s}{p['Prefix'].removeprefix(strip)}"
                    for p in response["CommonPrefixes"]
                ]
            )

        if "Contents" in response:
            for obj in response["Contents"]:
                key = obj["Key"]
                if (
                    not prefix
                    or key == prefix
                    or (
                        key.startswith(prefix)
                        and key.replace(prefix, "").count("/") <= 1
                        and not key.replace(prefix, "").startswith("/")
                    )
                ):
                    result.append(format_obj(obj, strip))

        return result


def main():
    parser = argparse.ArgumentParser(description="Show an s3 object")
    parser.add_argument("path", nargs="?", help="S3 path: s3://b/k, /b/k, or b/k")
    parser.add_argument("--bucket", "-b", help="S3 bucket name")
    parser.add_argument("--key", "-k", help="S3 key")
    parser.add_argument("--verbose", action="store_true", help="print all files")
    parser.add_argument(
        "--recursive", "-r", action="store_true", help="list recursively"
    )
    parser.add_argument(
        "--force", "-f", action="store_true", help="download even if large or binary"
    )
    parser.add_argument(
        "--full-path", action="store_true", help="show full keys in listings"
    )
    args = parser.parse_args()

    if args.bucket:
        bucket, key = args.bucket, args.key or ""
    elif args.path:
        bucket, key = parse_s3_path(args.path)
    else:
        parser.error("provide a path or --bucket")
    log.debug(f"{bucket=} {key=}")
    fp = args.full_path
    if not key or key.endswith("/"):
        log.info(f"\ns3://{bucket}/{key}:")
        for item in list_s3(bucket, key, recursive=args.recursive, full_path=fp):
            log.info(item)
        return

    BINARY_EXTS = {
        ".tar.gz",
        ".tgz",
        ".gz",
        ".zip",
        ".bz2",
        ".xz",
        ".7z",
        ".jar",
        ".war",
        ".ear",
        ".so",
        ".dylib",
        ".dll",
        ".exe",
        ".bin",
        ".dat",
        ".pkl",
        ".pickle",
        ".parquet",
        ".avro",
        ".orc",
    }
    IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"}
    AUDIO_EXTS = {".mp3", ".wav", ".aac", ".m4a", ".flac", ".ogg", ".aiff"}
    MAX_SIZE = 50 * 1024 * 1024

    is_binary = any(key.endswith(ext) for ext in BINARY_EXTS)
    is_image = any(key.endswith(ext) for ext in IMAGE_EXTS)
    is_audio = any(key.endswith(ext) for ext in AUDIO_EXTS)

    # Check size before downloading
    try:
        head = s3.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            # Maybe it's a folder without trailing /
            items = list_s3(bucket, key + "/", recursive=args.recursive, full_path=fp)
            if items:
                log.info(f"\ns3://{bucket}/{key}/:")
                for item in items:
                    log.info(item)
                return
            log.error(f"Not found: s3://{bucket}/{key}")
            return
        raise
    size = head["ContentLength"]
    date = head["LastModified"].strftime("%Y-%m-%d %H:%M")

    if not args.force and (size > MAX_SIZE or is_binary):
        log.info(f"{date}  {human_size(size):>10s}  s3://{bucket}/{key}")
        if size > MAX_SIZE:
            log.info(
                f"File too large to auto-download ({human_size(size)}). Use --force to download."
            )
        if is_binary:
            log.info("Binary file type. Use --force to download.")
        return

    local_path = str(get_s3_cached(bucket, key))

    if is_image:
        print(f"Opening image: {local_path}", file=sys.stderr)
        img = Image.open(local_path)
        img.show()
    elif is_audio:
        print(f"Playing audio: {local_path}", file=sys.stderr)
        cmd(f"afplay {local_path}", noisy=True)
    else:
        cmd(f"cat {local_path}", noisy=True)


if __name__ == "__main__":
    main()
