"""
publisher_service.py — Instagram Publishing Microservice
Supports carousel uploads, session persistence, and 2FA authentication.
"""

import json
import base64
import urllib.request
import urllib.parse
from pathlib import Path
from typing import List, Dict, Any, Optional
from config.settings import settings

def _upload_to_imgbb(image_path: str) -> Optional[str]:
    """Uploads image to ImgBB to get a public URL for Instagram Graph API."""
    if not settings.IMGBB_API_KEY:
        return None
    try:
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        url = "https://api.imgbb.com/1/upload"
        data = urllib.parse.urlencode({"key": settings.IMGBB_API_KEY, "image": b64}).encode("utf-8")
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=12) as r:
            res = json.loads(r.read())
            return res.get("data", {}).get("url")
    except Exception as e:
        print(f"⚠️ ImgBB upload error: {e}")
        return None


def publish_to_instagram(slides: List[str], caption: str, verification_code: Optional[str] = None) -> Dict[str, Any]:
    """
    Publishes a 4-slide carousel to Instagram @finpulse.daily.
    Uses saved 2FA session or username/password login.
    """
    try:
        from instagrapi import Client
        cl = Client()
        session_file = settings.SESSIONS_DIR / "finpulse_session.json"
        
        # Load saved session
        if session_file.exists():
            try:
                cl.load_settings(str(session_file))
                cl.get_timeline_feed()
            except Exception:
                pass

        if not cl.user_id:
            user = settings.INSTAGRAM_USERNAME
            pwd = settings.INSTAGRAM_PASSWORD
            if not user or not pwd:
                return {"success": False, "error": "Instagram credentials missing in .env"}
            
            if verification_code:
                cl.login(user, pwd, verification_code=verification_code)
            else:
                cl.login(user, pwd)
                
            cl.dump_settings(str(session_file))

        # Upload Carousel
        paths = [Path(p) for p in slides if Path(p).exists()]
        if len(paths) != len(slides):
            return {"success": False, "error": "Some slide image files are missing"}

        media = cl.album_upload(paths, caption=caption)
        return {
            "success": True,
            "media_id": str(media.pk),
            "media_code": str(media.code),
            "post_url": f"https://www.instagram.com/p/{media.code}/",
            "slide_count": len(paths)
        }
    except Exception as e:
        err_msg = str(e)
        if "two-factor" in err_msg.lower() or "verification" in err_msg.lower():
            return {"success": False, "error": "TWO_FACTOR_REQUIRED", "message": err_msg}
        return {"success": False, "error": err_msg}
