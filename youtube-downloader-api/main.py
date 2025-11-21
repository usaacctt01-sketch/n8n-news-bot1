from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import yt_dlp
import os
import logging
from pathlib import Path
from typing import Optional
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="YouTube Downloader API")

# Download directory
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "/downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


class DownloadRequest(BaseModel):
    video_url: str
    video_id: Optional[str] = None


class CleanupRequest(BaseModel):
    file_path: str


def sanitize_filename(filename: str) -> str:
    """Remove unsafe characters from filename"""
    # Remove or replace unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    return filename


@app.get("/")
async def root():
    return {
        "status": "running",
        "service": "YouTube Downloader API",
        "endpoints": {
            "download": "/download (POST)",
            "get_file": "/get-file/{filename} (GET)",
            "cleanup": "/cleanup (POST)"
        }
    }


@app.post("/download")
async def download_video(request: DownloadRequest):
    """Download YouTube video and return file information"""
    try:
        logger.info(f"Downloading video: {request.video_url}")
        
        # Extract video ID if not provided
        video_id = request.video_id
        if not video_id:
            # Extract from URL
            if 'youtu.be/' in request.video_url:
                video_id = request.video_url.split('youtu.be/')[1].split('?')[0]
            elif 'youtube.com' in request.video_url:
                video_id = request.video_url.split('v=')[1].split('&')[0]
            else:
                video_id = "unknown"
        
        # Clean video_id for filename
        video_id = sanitize_filename(video_id)[:50]  # Limit length
        
        # Output template
        output_template = os.path.join(DOWNLOAD_DIR, f"{video_id}.%(ext)s")
        
        # yt-dlp options
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': output_template,
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }
        
        # Download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.video_url, download=True)
            
            # Get actual filename
            filename = f"{video_id}.mp4"
            file_path = os.path.join(DOWNLOAD_DIR, filename)
            
            # Check if file exists
            if not os.path.exists(file_path):
                # Try to find the actual file
                possible_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith(video_id)]
                if possible_files:
                    filename = possible_files[0]
                    file_path = os.path.join(DOWNLOAD_DIR, filename)
                else:
                    raise FileNotFoundError(f"Downloaded file not found: {file_path}")
            
            file_size = os.path.getsize(file_path)
            
            return {
                "status": "success",
                "video_id": video_id,
                "title": info.get('title', 'Unknown'),
                "filename": filename,
                "file_path": file_path,
                "file_size": file_size,
                "duration": info.get('duration', 0),
                "thumbnail": info.get('thumbnail', ''),
            }
            
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@app.get("/get-file/{filename}")
async def get_file(filename: str):
    """Serve downloaded video file"""
    try:
        # Sanitize filename to prevent directory traversal
        filename = sanitize_filename(filename)
        file_path = os.path.join(DOWNLOAD_DIR, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            file_path,
            media_type="video/mp4",
            filename=filename
        )
    except Exception as e:
        logger.error(f"File serving failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cleanup")
async def cleanup_file(request: CleanupRequest):
    """Delete video file after processing"""
    try:
        # Extract filename from path
        filename = os.path.basename(request.file_path)
        filename = sanitize_filename(filename)
        file_path = os.path.join(DOWNLOAD_DIR, filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted file: {file_path}")
            return {"status": "success", "message": f"File {filename} deleted"}
        else:
            return {"status": "warning", "message": "File not found"}
            
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "download_dir": DOWNLOAD_DIR,
        "download_dir_exists": os.path.exists(DOWNLOAD_DIR)
    }
