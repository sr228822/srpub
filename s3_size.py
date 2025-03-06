#!/usr/bin/env python3
import boto3
import argparse
from concurrent.futures import ThreadPoolExecutor
from srutils import size_to_human


def parse_args():
    parser = argparse.ArgumentParser(
        description="Calculate the total size of an S3 folder recursively"
    )
    parser.add_argument("--bucket", required=True, help="S3 bucket name")
    parser.add_argument(
        "--prefix", required=True, help="S3 folder prefix to sum recursively"
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=1,
        help="Number of threads to use for calculation",
    )
    parser.add_argument("--verbose", action="store_true", help="print all files")
    return parser.parse_args()


def get_size_recursive(bucket, prefix, threads=10, verbose=False):
    """Calculate total size of all objects under a prefix recursively"""
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")

    total_size = 0
    objects_to_process = []

    # Collect all objects
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        if "Contents" in page:
            objects_to_process.extend(page["Contents"])

    # Process objects in parallel
    def process_object(obj):
        print(f"{size_to_human(obj['Size']):>10} : {obj['Key']}")
        return obj["Size"]

    with ThreadPoolExecutor(max_workers=threads) as executor:

        sizes = list(executor.map(process_object, objects_to_process))

    total_size = sum(sizes)

    # Convert to GB
    total_size_gb = total_size / (1024**3)

    return total_size_gb, len(objects_to_process)


def main():
    args = parse_args()

    print(f"Calculating total size for s3://{args.bucket}/{args.prefix}...")
    total_size_gb, num_objects = get_size_recursive(
        args.bucket, args.prefix, args.threads, verbose=args.verbose
    )

    print(f"\nTotal objects: {num_objects}")
    print(f"Total size: {total_size_gb:.2f} GB")


if __name__ == "__main__":
    main()
