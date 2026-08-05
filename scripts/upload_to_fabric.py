import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

# =====================================================
# Azure AD / Fabric Configuration
# =====================================================

load_dotenv()


TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

WORKSPACE_NAME = os.getenv("WORKSPACE_NAME")
LAKEHOUSE_NAME = os.getenv("LAKEHOUSE_NAME")

WORKSPACE_ID = os.getenv("WORKSPACE_ID")
LAKEHOUSE_ID = os.getenv("LAKEHOUSE_ID")

# =====================================================
# Local / Target Paths
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

LOCAL_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "ndjson"
)

TARGET_FOLDER = "bronze/fhir"


if not os.path.exists(LOCAL_FOLDER):
    raise FileNotFoundError(
        f"Folder not found: {LOCAL_FOLDER}"
    )


print(f"Reading files from: {LOCAL_FOLDER}")


# =====================================================
# Authenticate to Azure AD
# =====================================================

authority = (
    f"https://login.microsoftonline.com/{TENANT_ID}"
)


app = ConfidentialClientApplication(
    CLIENT_ID,
    authority=authority,
    client_credential=CLIENT_SECRET
)


token_response = app.acquire_token_for_client(
    scopes=[
        "https://storage.azure.com/.default"
    ]
)


if "access_token" not in token_response:
    raise Exception(
        f"Authentication failed:\n{token_response}"
    )


access_token = token_response["access_token"]


# =====================================================
# Headers
# =====================================================

auth_headers = {
    "Authorization": f"Bearer {access_token}",
    "x-ms-version": "2023-11-03"
}


# =====================================================
# Upload Function
# =====================================================

def upload_file(local_path, target_path):

    file_url = (
        "https://onelake.dfs.fabric.microsoft.com/"
        f"{WORKSPACE_NAME}/"
        f"{LAKEHOUSE_NAME}.Lakehouse/"
        f"Files/{target_path}"
    )


    file_size = os.path.getsize(local_path)


    print(f"\nUploading:")
    print(local_path)
    print(f"Target:")
    print(file_url)


    # -------------------------------------------------
    # Step 1 - Create empty file
    # -------------------------------------------------

    create_url = (
        file_url +
        "?resource=file"
    )


    response = requests.put(
        create_url,
        headers=auth_headers
    )


    if response.status_code not in [200, 201, 202]:
        print("Create failed")
        print(response.status_code)
        print(response.text)
        return False



    # -------------------------------------------------
    # Step 2 - Append file content
    # -------------------------------------------------

    with open(local_path, "rb") as f:

        data = f.read()


    append_url = (
        file_url +
        "?action=append&position=0"
    )


    append_headers = {
        "Authorization": f"Bearer {access_token}",
        "x-ms-version": "2023-11-03",
        "Content-Type": "application/octet-stream",
        "Content-Length": str(file_size)
    }


    response = requests.patch(
        append_url,
        headers=append_headers,
        data=data
    )


    if response.status_code not in [200, 202]:
        print("Append failed")
        print(response.status_code)
        print(response.text)
        return False



    # -------------------------------------------------
    # Step 3 - Flush / Commit file
    # -------------------------------------------------

    flush_url = (
        file_url +
        f"?action=flush&position={file_size}"
    )


    response = requests.patch(
        flush_url,
        headers=auth_headers
    )


    if response.status_code not in [200, 202]:
        print("Flush failed")
        print(response.status_code)
        print(response.text)
        return False


    return True



# =====================================================
# Upload NDJSON Files
# =====================================================

uploaded = 0
failed = 0


for file_name in os.listdir(LOCAL_FOLDER):

    if not file_name.endswith(".ndjson"):
        continue


    local_path = os.path.join(
        LOCAL_FOLDER,
        file_name
    )


    target_path = (
        f"{TARGET_FOLDER}/{file_name}"
    )


    print("\n" + "-" * 50)
    print(f"Uploading {file_name}")


    try:

        success = upload_file(
            local_path,
            target_path
        )


        if success:
            uploaded += 1
            print(f"✓ Uploaded {file_name}")

        else:
            failed += 1
            print(f"✗ Failed {file_name}")


    except Exception as e:

        failed += 1

        print(
            f"✗ Exception uploading {file_name}: {e}"
        )



# =====================================================
# Summary
# =====================================================

print("\n" + "=" * 50)
print("Upload Complete")
print("=" * 50)

print(f"Uploaded : {uploaded}")
print(f"Failed   : {failed}")