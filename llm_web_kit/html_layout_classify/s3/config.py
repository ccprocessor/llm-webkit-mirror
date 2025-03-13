from .reader import read_config

config = read_config()

spark_clusters: dict = config.get('spark', {}).get('clusters', {})
kafka_clusters: dict = config.get('kafka', {}).get('clusters', {})
es_clusters: dict = config.get('es', {}).get('clusters', {})
kudu_clusters: dict = config.get('kudu', {}).get('clusters', {})
hive_clusters: dict = config.get('hive', {}).get('clusters', {})

_s3_buckets: dict = config.get('s3', {}).get('buckets', {})
_s3_profiles: dict = config.get('s3', {}).get('profiles', {})
s3_clusters: dict = config.get('s3', {}).get('endpoints', {})

_kc = list(s3_clusters.keys())
_kc.sort(key=lambda s: -len(s))

s3_profiles = {}
for name, profile in _s3_profiles.items():
    assert isinstance(profile, dict)
    ak = profile.get('aws_access_key_id')
    sk = profile.get('aws_secret_access_key')
    if not ak and sk:
        continue
    c = next((c for c in _kc if name.startswith(c)), None)
    cluster = s3_clusters[c] if c else None
    if not cluster and profile.get('endpoint_url'):
        cluster = {'outside': profile['endpoint_url']}
    if not cluster:
        continue
    s3_profiles[name] = {
        'profile': name,
        'ak': ak,
        'sk': sk,
        'cluster': cluster,
    }

s3_buckets = {}
s3_bucket_prefixes = {}
for bucket, profile_name in _s3_buckets.items():
    profile = s3_profiles.get(profile_name)
    if not profile:
        continue
    if '*' not in bucket:
        s3_buckets[bucket] = profile
        continue
    bucket_prefix = bucket.rstrip('*')
    if '*' not in bucket_prefix:
        s3_bucket_prefixes[bucket_prefix] = profile

__all__ = [
    'config',
    's3_buckets',
    's3_bucket_prefixes',
    's3_profiles',
    's3_clusters',
    'spark_clusters',
    'kafka_clusters',
    'es_clusters',
    'kudu_clusters',
    'hive_clusters',
]
