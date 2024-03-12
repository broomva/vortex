from prefect.filesystems import RemoteFileSystem
import os

minio_block = RemoteFileSystem(
    basepath=f"s3://vortex-flows/{os.environ.get('MINIO_FLOWS_FOLDER', 'broomva-flows')}",
    settings={
        "key": os.environ.get("MINIO_USER", "minio"),
        "secret": os.environ.get("MINIO_PASSWORD", "minio123"),
        "client_kwargs": {"endpoint_url": os.environ.get("MINIO_HOST","http://localhost:9001")},
    },
)
minio_block.save("minio")



# prefect deployment build web_rag.py:web_rag_flow --name web_rag_deployment --tag minio -sb remote-file-system/minio