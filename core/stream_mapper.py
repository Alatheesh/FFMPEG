from copy import deepcopy


class StreamMapper:
    """
    Generates FFmpeg -map arguments based on the
    current media streams and queued operations.
    """

    def __init__(self, media_asset):

        self.asset = media_asset

        self.video = deepcopy(media_asset.video_streams)

        self.audio = deepcopy(media_asset.audio_streams)

        self.subtitle = deepcopy(media_asset.subtitle_streams)

        self.attachment = deepcopy(
            media_asset.attachment_streams
        )

    # --------------------------------------------------
    # AUDIO
    # --------------------------------------------------

    def remove_audio(self, stream_index):

        self.audio = [
            stream
            for stream in self.audio
            if stream["index"] != stream_index
        ]

    def swap_audio(
        self,
        first_stream,
        second_stream
    ):

        first = None
        second = None

        for stream in self.audio:

            if stream["index"] == first_stream:
                first = stream

            if stream["index"] == second_stream:
                second = stream

        if first and second:

            i = self.audio.index(first)
            j = self.audio.index(second)

            self.audio[i], self.audio[j] = (
                self.audio[j],
                self.audio[i]
            )

    # --------------------------------------------------
    # SUBTITLE
    # --------------------------------------------------

    def remove_subtitle(self, stream_index):

        self.subtitle = [
            stream
            for stream in self.subtitle
            if stream["index"] != stream_index
        ]

    # --------------------------------------------------
    # BUILD MAPS
    # --------------------------------------------------

    def build(self):

        maps = []

        # Video

        for stream in self.video:

            maps.append(
                f"0:{stream['index']}"
            )

        # Audio

        for stream in self.audio:

            maps.append(
                f"0:{stream['index']}"
            )

        # Subtitle

        for stream in self.subtitle:

            maps.append(
                f"0:{stream['index']}"
            )

        # Attachments

        for stream in self.attachment:

            maps.append(
                f"0:{stream['index']}"
            )

        return maps
