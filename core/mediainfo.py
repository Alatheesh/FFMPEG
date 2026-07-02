from pymediainfo import MediaInfo


def analyze_media(file_path: str):
    """
    Analyze a media file and return structured information.
    """

    media_info = MediaInfo.parse(file_path)

    result = {
        "general": {},
        "video": [],
        "audio": [],
        "subtitles": []
    }

    for track in media_info.tracks:

        if track.track_type == "General":
            result["general"] = {
                "format": track.format,
                "duration": track.duration,
                "file_size": track.file_size,
                "overall_bit_rate": track.overall_bit_rate
            }

        elif track.track_type == "Video":
            result["video"].append({
                "id": track.track_id,
                "format": track.format,
                "codec": track.codec_id,
                "width": track.width,
                "height": track.height,
                "fps": track.frame_rate,
                "language": track.language,
                "default": track.default
            })

        elif track.track_type == "Audio":
            result["audio"].append({
                "id": track.track_id,
                "format": track.format,
                "codec": track.codec_id,
                "channels": track.channel_s,
                "language": track.language,
                "title": track.title,
                "default": track.default
            })

        elif track.track_type == "Text":
            result["subtitles"].append({
                "id": track.track_id,
                "format": track.format,
                "language": track.language,
                "title": track.title,
                "default": track.default
            })

    return result
