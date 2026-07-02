from datetime import timedelta


class Messages:

    TITLE="🎬 Auto Media Editor"

    LINE="━━━━━━━━━━━━━━━━━━"

    # ==================================================
    # Helpers
    # ==================================================

    @staticmethod
    def _duration(seconds):

        try:
            seconds=int(float(seconds))
        except Exception:
            seconds=0

        return str(
            timedelta(seconds=seconds)
        )

    @staticmethod
    def _size(size):

        units=["B","KB","MB","GB","TB"]

        value=float(size or 0)

        for unit in units:

            if value<1024:
                return f"{value:.2f} {unit}"

            value/=1024

        return f"{value:.2f} PB"

    @staticmethod
    def _track_count(items):

        return len(items) if items else 0

    # ==================================================
    # Home
    # ==================================================

    @classmethod
    def home(cls,workspace):

        video=workspace.get_main_video()

        if video is None:

            return (
                f"{cls.TITLE}\n\n"
                "📂 No video loaded.\n\n"
                "Send a video to begin editing."
            )

        audio=cls._track_count(
            getattr(video,"audio_streams",[])
        )

        subtitles=cls._track_count(
            getattr(video,"subtitle_streams",[])
        )

        duration=cls._duration(
            getattr(video,"duration",0)
        )

        size=cls._size(
            getattr(video,"size",0)
        )

        pending=0

        if hasattr(workspace,"audio_manager"):
            pending+=workspace.audio_manager.pending_count()

        if hasattr(workspace,"media_manager"):
            pending+=workspace.media_manager.pending_count()

        return (
            f"{cls.TITLE}\n\n"
            f"{cls.LINE}\n"
            f"🎞 File : {video.name}\n"
            f"📦 Size : {size}\n"
            f"⏱ Duration : {duration}\n"
            f"🎵 Audio : {audio}\n"
            f"💬 Subtitle : {subtitles}\n"
            f"{cls.LINE}\n"
            f"📋 Pending Operations : {pending}\n"
            f"{cls.LINE}\n"
            "Choose an option below."
        )

    # ==================================================
    # Audio
    # ==================================================

    @classmethod
    def audio(cls,workspace):

        video=workspace.get_main_video()

        if video is None:
            return "❌ No video loaded."

        text=[
            cls.TITLE,
            "",
            cls.LINE,
            "🎵 Audio Tracks",
            ""
        ]

        streams=getattr(video,"audio_streams",[])

        if not streams:

            text.append("No audio tracks found.")

        else:

            for stream in streams:

                tags=stream.get("tags",{})

                language=tags.get(
                    "language",
                    "und"
                ).upper()

                title=tags.get(
                    "title",
                    "Unknown"
                )

                codec=stream.get(
                    "codec_name",
                    "?"
                )

                index=stream.get(
                    "index",
                    0
                )

                text.append(
                    f"{index}. {language} • {title} • {codec}"
                )

        text.extend([
            "",
            cls.LINE,
            "Select an audio operation."
        ])

        return "\n".join(text)

    # ==================================================
    # Subtitle
    # ==================================================

    @classmethod
    def subtitle(cls,workspace):

        video=workspace.get_main_video()

        if video is None:
            return "❌ No video loaded."

        text=[
            cls.TITLE,
            "",
            cls.LINE,
            "💬 Subtitle Tracks",
            ""
        ]

        streams=getattr(
            video,
            "subtitle_streams",
            []
        )

        if not streams:

            text.append(
                "No subtitle tracks found."
            )

        else:

            for stream in streams:

                tags=stream.get("tags",{})

                language=tags.get(
                    "language",
                    "und"
                ).upper()

                title=tags.get(
                    "title",
                    "Unknown"
                )

                codec=stream.get(
                    "codec_name",
                    "?"
                )

                index=stream.get(
                    "index",
                    0
                )

                text.append(
                    f"{index}. {language} • {title} • {codec}"
                )

        text.extend([
            "",
            cls.LINE,
            "Select a subtitle operation."
        ])

        return "\n".join(text)
    # ==================================================
    # Video
    # ==================================================

    @classmethod
    def video(cls,workspace):

        video=workspace.get_main_video()

        if video is None:
            return "❌ No video loaded."

        width=getattr(video,"width",0)
        height=getattr(video,"height",0)
        fps=getattr(video,"fps",0)
        codec=getattr(video,"video_codec","Unknown")
        bitrate=getattr(video,"bitrate",0)

        return (
            f"{cls.TITLE}\n\n"
            f"{cls.LINE}\n"
            "🎬 Video Information\n"
            f"{cls.LINE}\n"
            f"📺 Resolution : {width} × {height}\n"
            f"🎞 Codec : {codec}\n"
            f"⚡ FPS : {fps}\n"
            f"📦 Bitrate : {bitrate}\n\n"
            "Choose a video operation."
        )

    # ==================================================
    # Thumbnail
    # ==================================================

    @classmethod
    def thumbnail(cls,workspace):

        video=workspace.get_main_video()

        if video is None:
            return "❌ No video loaded."

        thumbnail=getattr(
            video,
            "thumbnail",
            None
        )

        return (
            f"{cls.TITLE}\n\n"
            f"{cls.LINE}\n"
            "🖼 Thumbnail\n"
            f"{cls.LINE}\n"
            f"Available : {'Yes' if thumbnail else 'No'}\n\n"
            "Choose a thumbnail operation."
        )

    # ==================================================
    # Metadata
    # ==================================================

    @classmethod
    def metadata(cls,workspace):

        video=workspace.get_main_video()

        if video is None:
            return "❌ No video loaded."

        metadata=getattr(
            video,
            "metadata",
            {}
        )

        title=metadata.get("title","-")
        author=metadata.get("author","-")
        comment=metadata.get("comment","-")
        description=metadata.get("description","-")

        return (
            f"{cls.TITLE}\n\n"
            f"{cls.LINE}\n"
            "📝 Metadata\n"
            f"{cls.LINE}\n"
            f"🏷 Title : {title}\n"
            f"👤 Author : {author}\n"
            f"💬 Comment : {comment}\n"
            f"📖 Description : {description}\n\n"
            "Choose a metadata operation."
        )

    # ==================================================
    # Workspace
    # ==================================================

    @classmethod
    def workspace(cls,workspace):

        assets=getattr(
            workspace,
            "assets",
            {}
        )

        asset_count=0

        try:
            asset_count=len(assets)
        except Exception:
            try:
                asset_count=len(assets.all())
            except Exception:
                asset_count=0

        audio_jobs=0
        media_jobs=0

        if hasattr(workspace,"audio_manager"):
            audio_jobs=workspace.audio_manager.pending_count()

        if hasattr(workspace,"media_manager"):
            media_jobs=workspace.media_manager.pending_count()

        return (
            f"{cls.TITLE}\n\n"
            f"{cls.LINE}\n"
            "📋 Workspace\n"
            f"{cls.LINE}\n"
            f"📁 Assets : {asset_count}\n"
            f"🎵 Audio Queue : {audio_jobs}\n"
            f"🎬 Media Queue : {media_jobs}\n"
            f"📦 Total Operations : {audio_jobs+media_jobs}\n\n"
            "Manage your workspace."
        )

    # ==================================================
    # Export
    # ==================================================

    @classmethod
    def export(cls,workspace):

        audio=0
        media=0

        if hasattr(workspace,"audio_manager"):
            audio=workspace.audio_manager.pending_count()

        if hasattr(workspace,"media_manager"):
            media=workspace.media_manager.pending_count()

        total=audio+media

        return (
            f"{cls.TITLE}\n\n"
            f"{cls.LINE}\n"
            "📦 Export Preview\n"
            f"{cls.LINE}\n"
            f"🎵 Audio Operations : {audio}\n"
            f"🎬 Media Operations : {media}\n"
            f"📋 Total Operations : {total}\n\n"
            "Press 🚀 Export to begin processing."
        )
    # ==================================================
    # Processing
    # ==================================================

    @classmethod
    def processing(
        cls,
        operation:str="Preparing",
        progress:float=0,
        speed:str="-",
        eta:str="-"
    ):

        progress=max(0,min(int(progress),100))

        bars=20
        filled=int(progress/100*bars)

        bar=(
            "█"*filled+
            "░"*(bars-filled)
        )

        return (
            f"{cls.TITLE}\n\n"
            f"{cls.LINE}\n"
            "⚙ Processing\n"
            f"{cls.LINE}\n"
            f"📌 Operation : {operation}\n"
            f"📊 Progress : {progress}%\n"
            f"{bar}\n"
            f"⚡ Speed : {speed}\n"
            f"⏳ ETA : {eta}\n\n"
            "Please wait..."
        )

    # ==================================================
    # Completed
    # ==================================================

    @classmethod
    def completed(
        cls,
        filename:str,
        elapsed:str,
        output_size:str
    ):

        return (
            f"{cls.TITLE}\n\n"
            "✅ Processing Completed\n\n"
            f"{cls.LINE}\n"
            f"📁 File : {filename}\n"
            f"📦 Size : {output_size}\n"
            f"⏱ Time : {elapsed}\n"
            f"{cls.LINE}\n"
            "Your file is ready."
        )

    # ==================================================
    # Error
    # ==================================================

    @classmethod
    def error(
        cls,
        message:str
    ):

        return (
            f"{cls.TITLE}\n\n"
            "❌ Processing Failed\n\n"
            f"{cls.LINE}\n"
            f"{message}\n"
            f"{cls.LINE}\n"
            "Please try again."
        )

    # ==================================================
    # Empty Workspace
    # ==================================================

    @classmethod
    def empty_workspace(cls):

        return (
            f"{cls.TITLE}\n\n"
            "📂 Workspace Empty\n\n"
            "Send a video to start editing."
        )

    # ==================================================
    # Help
    # ==================================================

    @classmethod
    def help(cls):

        return (
            f"{cls.TITLE}\n\n"
            "📖 Supported Features\n\n"
            "🎵 Audio\n"
            "• Replace\n"
            "• Merge\n"
            "• Remove\n"
            "• Swap\n"
            "• Rename\n"
            "• Default Track\n"
            "• Extract\n\n"
            "💬 Subtitle\n"
            "• Add\n"
            "• Replace\n"
            "• Remove\n"
            "• Burn\n\n"
            "🎬 Video\n"
            "• Trim\n"
            "• Crop\n"
            "• Resize\n"
            "• Rotate\n"
            "• Compress\n"
            "• Speed\n\n"
            "🖼 Thumbnail\n"
            "📝 Metadata\n"
            "📦 Container Conversion"
        )

    # ==================================================
    # About
    # ==================================================

    @classmethod
    def about(cls):

        return (
            f"{cls.TITLE}\n\n"
            "Telegram Media Editing Bot\n\n"
            "Powered by:\n"
            "• Pyrogram\n"
            "• FFmpeg\n"
            "• FFprobe\n"
            "• MongoDB\n"
            "• Backblaze B2\n"
            "• Hugging Face Spaces"
        )

    # ==================================================
    # Generic
    # ==================================================

    @classmethod
    def success(
        cls,
        message:str
    ):

        return (
            f"✅ Success\n\n{message}"
        )

    @classmethod
    def info(
        cls,
        message:str
    ):

        return (
            f"ℹ Information\n\n{message}"
        )

    @classmethod
    def warning(
        cls,
        message:str
    ):

        return (
            f"⚠ Warning\n\n{message}"
        )
