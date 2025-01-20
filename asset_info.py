# Description: This script extracts media information using ffprobe and python-magic.
import os
import subprocess
import json
import magic

def get_media_info(filepath):
    """Extracts media information using ffprobe and python-magic."""

    try:
        # Use ffprobe for detailed media information
        ffprobe_command = [
            "ffprobe",
            "-v", "error",
            "-show_format",
            "-show_streams",
            "-of", "json",
            filepath
        ]
        ffprobe_output = subprocess.check_output(ffprobe_command).decode("utf-8")
        media_info = json.loads(ffprobe_output)

        # Use python-magic for mime type
        mime = magic.from_file(filepath, mime=True)
        media_info['mime_type'] = mime

        # Extract relevant information
        extracted_info = {
            "file_path": filepath,
            "mime_type": media_info.get('mime_type'),
            "format": media_info.get("format", {}).get("format_name"),
            "streams": []
        }

        for stream in media_info.get("streams", []):
            stream_info = {
                "codec_type": stream.get("codec_type"),
                "codec_name": stream.get("codec_name"),
            }
            if stream.get("codec_type") == "video":
                stream_info["width"] = stream.get("width")
                stream_info["height"] = stream.get("height")
                stream_info["display_aspect_ratio"] = stream.get("display_aspect_ratio")
                stream_info["pix_fmt"] = stream.get("pix_fmt")
                stream_info["r_frame_rate"] = stream.get("r_frame_rate")
            elif stream.get("codec_type") == "audio":
                stream_info['sample_rate'] = stream.get('sample_rate')
                stream_info['channels'] = stream.get('channels')
            extracted_info["streams"].append(stream_info)
        return extracted_info

    except subprocess.CalledProcessError as e:
        print(f"Error processing {filepath}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for {filepath}: {e}")
        print(f"ffprobe output was: {ffprobe_output}") #print the output for debugging
        return None
    except magic.MagicException as e:
        print(f"Error detecting MIME type for {filepath}: {e}")
        return None
    except FileNotFoundError:
        print("ffprobe not found. Please install it (e.g., using apt-get install ffmpeg).")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def crawl_directory(root_dir):
    """Crawls the directory and processes media files."""

    media_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            filepath = os.path.join(root, file)
            info = get_media_info(filepath)
            if info:
                media_files.append(info)
    return media_files


if __name__ == "__main__":
    root_folder = "."  # Current directory
    media_information = crawl_directory(root_folder)

    if media_information:
        # Save to JSON or print
        import json
        with open("media_info.json", "w") as f:
            json.dump(media_information, f, indent=4)
        print("Media information saved to media_info.json")
        #Or print directly to console
        #print(json.dumps(media_information, indent=4))
    else:
        print("No media files found or errors occurred.")