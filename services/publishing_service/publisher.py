"""
services/publishing_service/publisher.py — Instagram Carousel Publishing Client
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from common.config import settings

def publish_carousel_to_instagram(slides: List[str], caption: str, verification_code: Optional[str] = None) -> Dict[str, Any]:
    """Publishes carousel to Instagram with session caching & 2FA support."""
    try:
        from instagrapi import Client
        cl = Client()
        session_file = settings.SESSIONS_DIR / "finpulse_session.json"

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
