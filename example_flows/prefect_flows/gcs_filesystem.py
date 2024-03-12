from prefect.filesystems import GCS
from dotenv import load_dotenv
import os
load_dotenv()

block = GCS(
    bucket_path="vortex-flows/broomva-flows", 
    service_account_info=os.environ.get("GCS_SERVICE_ACCOUNT"),
    project="broomva-vortex-ai"
)
block.save("gcs-vortex-flows", overwrite=True)

#%%
# # prefect deployment build web_rag.py:web_rag_flow --name web_rag_deployment --tag gcs-vortex-flows -sb gcs/gcs-vortex-flows

