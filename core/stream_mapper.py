from __future__ import annotations

from copy import deepcopy


class StreamMapper:

    """
    Handles FFmpeg stream mapping.

    Responsible for

    • Keeping stream order
    • Removing streams
    • Adding streams
    • Replacing streams
    • Default tracks
    • Languages
    • Titles
    """

    def __init__(self,media):

        self.media=media

        metadata=getattr(
            media,
            "metadata",
            {}
        )

        self.streams=deepcopy(
            metadata.get(
                "streams",
                []
            )
        )

        self.extra_inputs=[]

    # ==================================================
    # Helpers
    # ==================================================

    def stream(
        self,
        index:int
    ):

        return self.streams[index]

    def streams_by_type(
        self,
        codec_type:str
    ):

        return [

            stream

            for stream in self.streams

            if stream.get(
                "codec_type"
            )==codec_type

        ]

    def video(self):

        return self.streams_by_type(
            "video"
        )

    def audio(self):

        return self.streams_by_type(
            "audio"
        )

    def subtitle(self):

        return self.streams_by_type(
            "subtitle"
        )

    def attachment(self):

        return self.streams_by_type(
            "attachment"
        )

    # ==================================================
    # Remove
    # ==================================================

    def remove_audio(
        self,
        stream_index:int
    ):

        self._remove(
            "audio",
            stream_index
        )

    def remove_subtitle(
        self,
        stream_index:int
    ):

        self._remove(
            "subtitle",
            stream_index
        )

    def remove_video(
        self,
        stream_index:int
    ):

        self._remove(
            "video",
            stream_index
        )

    def _remove(
        self,
        codec_type,
        stream_index
    ):

        counter=-1

        remaining=[]

        for stream in self.streams:

            if stream.get(
                "codec_type"
            )!=codec_type:

                remaining.append(stream)

                continue

            counter+=1

            if counter==stream_index:
                continue

            remaining.append(stream)

        self.streams=remaining

    # ==================================================
    # Add
    # ==================================================

    def add_audio(
        self,
        input_index:int
    ):

        self.extra_inputs.append({

            "type":"audio",

            "input":input_index,

            "stream":0

        })

    def add_subtitle(
        self,
        input_index:int
    ):

        self.extra_inputs.append({

            "type":"subtitle",

            "input":input_index,

            "stream":0

        })

    def add_attachment(
        self,
        input_index:int
    ):

        self.extra_inputs.append({

            "type":"attachment",

            "input":input_index,

            "stream":0

        })
    # ==================================================
    # Replace
    # ==================================================

    def replace_audio(
        self,
        stream_index:int,
        input_index:int
    ):

        self.remove_audio(
            stream_index
        )

        self.extra_inputs.append({

            "type":"audio",
            "input":input_index,
            "stream":0,
            "replace":stream_index

        })

    def replace_subtitle(
        self,
        stream_index:int,
        input_index:int
    ):

        self.remove_subtitle(
            stream_index
        )

        self.extra_inputs.append({

            "type":"subtitle",
            "input":input_index,
            "stream":0,
            "replace":stream_index

        })

    # ==================================================
    # Default Track
    # ==================================================

    def set_default_audio(
        self,
        stream_index:int
    ):

        counter=-1

        for stream in self.streams:

            if stream.get("codec_type")!="audio":
                continue

            counter+=1

            disposition=stream.setdefault(
                "disposition",
                {}
            )

            disposition["default"]=(
                1 if counter==stream_index else 0
            )

    def set_default_subtitle(
        self,
        stream_index:int
    ):

        counter=-1

        for stream in self.streams:

            if stream.get("codec_type")!="subtitle":
                continue

            counter+=1

            disposition=stream.setdefault(
                "disposition",
                {}
            )

            disposition["default"]=(
                1 if counter==stream_index else 0
            )

    # ==================================================
    # Language
    # ==================================================

    def set_audio_language(
        self,
        stream_index:int,
        language:str
    ):

        self._set_tag(
            "audio",
            stream_index,
            "language",
            language
        )

    def set_subtitle_language(
        self,
        stream_index:int,
        language:str
    ):

        self._set_tag(
            "subtitle",
            stream_index,
            "language",
            language
        )

    # ==================================================
    # Title
    # ==================================================

    def set_audio_title(
        self,
        stream_index:int,
        title:str
    ):

        self._set_tag(
            "audio",
            stream_index,
            "title",
            title
        )

    def set_subtitle_title(
        self,
        stream_index:int,
        title:str
    ):

        self._set_tag(
            "subtitle",
            stream_index,
            "title",
            title
        )

    # ==================================================
    # Internal Helpers
    # ==================================================

    def _set_tag(
        self,
        codec_type:str,
        stream_index:int,
        key:str,
        value:str
    ):

        counter=-1

        for stream in self.streams:

            if stream.get("codec_type")!=codec_type:
                continue

            counter+=1

            if counter!=stream_index:
                continue

            tags=stream.setdefault(
                "tags",
                {}
            )

            tags[key]=value
            return

        raise IndexError(
            f"{codec_type} stream {stream_index} not found."
        )

    # ==================================================
    # Information
    # ==================================================

    def stream_count(
        self,
        codec_type:str
    ):

        return len(
            self.streams_by_type(codec_type)
        )

    def has_video(self):

        return self.stream_count(
            "video"
        )>0

    def has_audio(self):

        return self.stream_count(
            "audio"
        )>0

    def has_subtitles(self):

        return self.stream_count(
            "subtitle"
        )>0
    # ==================================================
    # FFmpeg Map Builder
    # ==================================================

    def build(self):

        maps=[]

        video_index=0
        audio_index=0
        subtitle_index=0
        attachment_index=0

        for stream in self.streams:

            codec_type=stream.get("codec_type")

            if codec_type=="video":

                maps.append(
                    f"0:v:{video_index}"
                )

                video_index+=1

            elif codec_type=="audio":

                maps.append(
                    f"0:a:{audio_index}"
                )

                audio_index+=1

            elif codec_type=="subtitle":

                maps.append(
                    f"0:s:{subtitle_index}"
                )

                subtitle_index+=1

            elif codec_type=="attachment":

                maps.append(
                    f"0:t:{attachment_index}"
                )

                attachment_index+=1

        for item in self.extra_inputs:

            stream_type=item["type"]

            if stream_type=="audio":

                maps.append(
                    f"{item['input']}:a:{item['stream']}"
                )

            elif stream_type=="subtitle":

                maps.append(
                    f"{item['input']}:s:{item['stream']}"
                )

            elif stream_type=="attachment":

                maps.append(
                    f"{item['input']}:t:{item['stream']}"
                )

            elif stream_type=="video":

                maps.append(
                    f"{item['input']}:v:{item['stream']}"
                )

        return maps

    # ==================================================
    # Export Metadata
    # ==================================================

    def metadata(self):

        metadata=[]

        video=0
        audio=0
        subtitle=0

        for stream in self.streams:

            stream_type=stream.get("codec_type")

            if stream_type=="video":

                index=video
                video+=1

            elif stream_type=="audio":

                index=audio
                audio+=1

            elif stream_type=="subtitle":

                index=subtitle
                subtitle+=1

            else:
                continue

            tags=stream.get("tags",{})

            for key,value in tags.items():

                metadata.append({
                    "stream":stream_type,
                    "index":index,
                    "key":key,
                    "value":value
                })

        return metadata

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):

        self.extra_inputs.clear()

    # ==================================================
    # Serialization
    # ==================================================

    def to_dict(self):

        return {
            "streams":self.streams,
            "extra_inputs":self.extra_inputs
        }

    # ==================================================
    # Magic Methods
    # ==================================================

    def __len__(self):

        return len(self.streams)

    def __iter__(self):

        return iter(self.streams)

    def __getitem__(
        self,
        index
    ):

        return self.streams[index]

    def __repr__(self):

        return (
            "<StreamMapper "
            f"streams={len(self.streams)} "
            f"extra_inputs={len(self.extra_inputs)}>"
        )
