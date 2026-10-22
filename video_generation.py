
import os
import time
import requests
from dotenv import load_dotenv

# Load configuration
load_dotenv()

endpoint = os.getenv(
    "AZURE_OPENAI_ENDPOINT_VIDEO", ""
).rstrip("/")

deployment_name = os.getenv(
    "AZURE_OPENAI_DEPLOYMENT_NAME_VIDEO", ""
)

api_key = os.getenv("AZURE_OPENAI_API_KEY_VIDEO", "")

if not endpoint or not deployment_name or not api_key:
    raise ValueError(
        "Configure AZURE_OPENAI_ENDPOINT_VIDEO, "
        "AZURE_OPENAI_DEPLOYMENT_NAME_VIDEO, and "
        "AZURE_OPENAI_API_KEY_VIDEO in .env"
    )

# This API requires a supported Azure OpenAI endpoint.
if not endpoint.endswith(".openai.azure.com"):
    raise ValueError(
        "Your configured endpoint is not the documented "
        "Azure OpenAI endpoint for this video API.\n"
        "Current endpoint: " + endpoint + "\n"
        "Check Keys and Endpoint in Azure portal and use "
        "the actual supported endpoint. Do not simply "
        "change the hostname manually."
    )

api_version = "preview"

headers = {
    "api-key": api_key,
    "Content-Type": "application/json"
}

os.makedirs("videos", exist_ok=True)



def generate_video(prompt, video_number):
    import time
    import requests

    create_url = f"{endpoint}/openai/v1/videos?api-version=preview"

    payload = {
        "model": deployment_name,
        "prompt": prompt,
        "size": "1280x720",
        "seconds": "8"
    }

    try:
        # 1. Create video
        response = requests.post(
            create_url,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()

        video = response.json()
        video_id = video["id"]

        print("Video ID:", video_id)
        print("Status:", video.get("status"))

        # 2. Poll video status
        status_url = (
            f"{endpoint}/openai/v1/videos/"
            f"{video_id}?api-version=preview"
        )

        deadline = time.monotonic() + 600

        while True:
            if time.monotonic() >= deadline:
                print("Timed out. Video ID:", video_id)
                return

            time.sleep(5)

            status_response = requests.get(
                status_url,
                headers=headers,
                timeout=60
            )
            status_response.raise_for_status()

            video = status_response.json()
            status = video.get("status", "unknown")

            print("Video status:", status)

            if status in ("completed", "failed"):
                break

        if status != "completed":
            print("Video generation failed:", video.get("error"))
            return

        # 3. Download generated MP4
        content_url = (
            f"{endpoint}/openai/v1/videos/"
            f"{video_id}/content?api-version=preview"
        )

        download_response = requests.get(
            content_url,
            headers={"api-key": api_key},
            timeout=180
        )
        download_response.raise_for_status()

        os.makedirs("videos", exist_ok=True)
        file_path = f"videos/output_{video_number}.mp4"

        with open(file_path, "wb") as f:
            f.write(download_response.content)

        print("Video saved:", file_path)

    except requests.RequestException as ex:
        print("API error:", ex)

        if ex.response is not None:
            print("Response:", ex.response.text)

    print("\nSubmitting video generation request...")

    create_url = (
        f"{endpoint}/openai/v1/video/generations/jobs"
        f"?api-version={api_version}"
    )

    payload = {
        "prompt": prompt,
        "model": deployment_name,
        "width": 1280,
        "height": 720,
        "n_seconds": 8
    }

    try:
        # Step 1: Create the video-generation job
        response = requests.post(
            create_url,
            headers=headers,
            json=payload,
            timeout=60
        )

        if not response.ok:
            print("HTTP status:", response.status_code)
            print("API response:", response.text)
            response.raise_for_status()

        job = response.json()
        job_id = job["id"]

        print("Job ID:", job_id)
        print("Initial status:", job.get("status"))

        # Step 2: Poll the job status
        status_url = (
            f"{endpoint}/openai/v1/video/generations/jobs/"
            f"{job_id}?api-version={api_version}"
        )

        terminal_statuses = {
            "succeeded",
            "failed",
            "cancelled"
        }

        deadline = time.monotonic() + 600

        while True:
            if time.monotonic() >= deadline:
                print("Timed out waiting for video generation.")
                print("Save this job ID to check later:", job_id)
                return

            time.sleep(5)

            status_response = requests.get(
                status_url,
                headers=headers,
                timeout=60
            )
            status_response.raise_for_status()

            job = status_response.json()
            status = job.get("status", "unknown")

            print("Video status:", status)

            if status in terminal_statuses:
                break

        # Step 3: Check completion
        if status != "succeeded":
            print("Video generation did not succeed.")
            print("Failure reason:", job.get("failure_reason"))
            return

        generations = job.get("generations", [])

        if not generations:
            print("No generated videos were returned.")
            return

        generation_id = generations[0].get("id")

        if not generation_id:
            print("The response did not contain a generation ID.")
            return

        # Step 4: Download the generated MP4
        download_url = (
            f"{endpoint}/openai/v1/video/generations/"
            f"{generation_id}/content/video"
            f"?api-version={api_version}"
        )

        video_response = requests.get(
            download_url,
            headers={"api-key": api_key},
            timeout=180
        )
        video_response.raise_for_status()

        file_path = f"videos/output_{video_number}.mp4"

        with open(file_path, "wb") as video_file:
            video_file.write(video_response.content)

        print("Video saved successfully:", file_path)

    except requests.RequestException as ex:
        print("API request failed:", ex)

        if ex.response is not None:
            print("Response details:", ex.response.text)

    except (KeyError, IndexError, ValueError) as ex:
        print("Unexpected API response:", ex)


def main():
    video_count = 0

    print("Sora 2 Video Generation Demo")
    print("Enter 'quit' to exit.")

    while True:
        prompt = input(
            "\nEnter your video prompt: "
        ).strip()

        if prompt.lower() == "quit":
            print("Exiting...")
            break

        if not prompt:
            print("Please enter a valid prompt.")
            continue

        video_count += 1
        generate_video(prompt, video_count)


if __name__ == "__main__":
    main()

#A cinematic aerial shot of a futuristic city at sunset, with flying vehicles gliding between glass skyscrapers, warm golden light reflecting off the buildings, gentle camera movement, atmospheric clouds, a wide landscape composition, smooth motion, and realistic lighting.