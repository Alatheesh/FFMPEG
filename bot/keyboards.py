from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton


class Keyboards:

    # ==================================================
    # Common
    # ==================================================

    @staticmethod
    def back(callback="home"):

        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data=callback
                )
            ]
        ])

    @staticmethod
    def close():

        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "❌ Close",
                    callback_data="close"
                )
            ]
        ])

    @staticmethod
    def confirm(
        yes="confirm",
        no="cancel"
    ):

        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "✅ Yes",
                    callback_data=yes
                ),
                InlineKeyboardButton(
                    "❌ No",
                    callback_data=no
                )
            ]
        ])

    # ==================================================
    # Home
    # ==================================================

    @staticmethod
    def home():

        return InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🎵 Audio",
                    callback_data="menu:audio"
                ),
                InlineKeyboardButton(
                    "💬 Subtitle",
                    callback_data="menu:subtitle"
                )
            ],

            [
                InlineKeyboardButton(
                    "🎬 Video",
                    callback_data="menu:video"
                ),
                InlineKeyboardButton(
                    "🖼 Thumbnail",
                    callback_data="menu:thumbnail"
                )
            ],

            [
                InlineKeyboardButton(
                    "📝 Metadata",
                    callback_data="menu:metadata"
                ),
                InlineKeyboardButton(
                    "📦 Export",
                    callback_data="menu:export"
                )
            ],

            [
                InlineKeyboardButton(
                    "📋 Workspace",
                    callback_data="menu:workspace"
                ),
                InlineKeyboardButton(
                    "⚙ Settings",
                    callback_data="menu:settings"
                )
            ]
        ])

    # ==================================================
    # Audio
    # ==================================================

    @staticmethod
    def audio():

        return InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "➕ Merge",
                    callback_data="audio:merge"
                ),
                InlineKeyboardButton(
                    "🔄 Replace",
                    callback_data="audio:replace"
                )
            ],

            [
                InlineKeyboardButton(
                    "❌ Remove",
                    callback_data="audio:remove"
                ),
                InlineKeyboardButton(
                    "🔀 Swap",
                    callback_data="audio:swap"
                )
            ],

            [
                InlineKeyboardButton(
                    "✏ Rename",
                    callback_data="audio:rename"
                ),
                InlineKeyboardButton(
                    "⭐ Default",
                    callback_data="audio:default"
                )
            ],

            [
                InlineKeyboardButton(
                    "📤 Extract",
                    callback_data="audio:extract"
                )
            ],

            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="home"
                )
            ]
        ])

    # ==================================================
    # Subtitle
    # ==================================================

    @staticmethod
    def subtitle():

        return InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "➕ Add",
                    callback_data="subtitle:add"
                ),
                InlineKeyboardButton(
                    "🔄 Replace",
                    callback_data="subtitle:replace"
                )
            ],

            [
                InlineKeyboardButton(
                    "❌ Remove",
                    callback_data="subtitle:remove"
                ),
                InlineKeyboardButton(
                    "🔥 Burn",
                    callback_data="subtitle:burn"
                )
            ],

            [
                InlineKeyboardButton(
                    "✏ Rename",
                    callback_data="subtitle:rename"
                )
            ],

            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="home"
                )
            ]
        ])
    # ==================================================
    # Video
    # ==================================================

    @staticmethod
    def video():

        return InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "✂ Trim",
                    callback_data="video:trim"
                ),
                InlineKeyboardButton(
                    "✂ Crop",
                    callback_data="video:crop"
                )
            ],

            [
                InlineKeyboardButton(
                    "📏 Resize",
                    callback_data="video:resize"
                ),
                InlineKeyboardButton(
                    "🔄 Rotate",
                    callback_data="video:rotate"
                )
            ],

            [
                InlineKeyboardButton(
                    "🗜 Compress",
                    callback_data="video:compress"
                ),
                InlineKeyboardButton(
                    "⚡ Speed",
                    callback_data="video:speed"
                )
            ],

            [
                InlineKeyboardButton(
                    "🎬 Merge",
                    callback_data="video:merge"
                ),
                InlineKeyboardButton(
                    "📦 Convert",
                    callback_data="video:convert"
                )
            ],

            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="home"
                )
            ]
        ])

    # ==================================================
    # Thumbnail
    # ==================================================

    @staticmethod
    def thumbnail():

        return InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🖼 Replace",
                    callback_data="thumbnail:replace"
                ),
                InlineKeyboardButton(
                    "📤 Extract",
                    callback_data="thumbnail:extract"
                )
            ],

            [
                InlineKeyboardButton(
                    "❌ Remove",
                    callback_data="thumbnail:remove"
                )
            ],

            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="home"
                )
            ]
        ])

    # ==================================================
    # Metadata
    # ==================================================

    @staticmethod
    def metadata():

        return InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🏷 Title",
                    callback_data="metadata:title"
                ),
                InlineKeyboardButton(
                    "👤 Author",
                    callback_data="metadata:author"
                )
            ],

            [
                InlineKeyboardButton(
                    "📝 Description",
                    callback_data="metadata:description"
                ),
                InlineKeyboardButton(
                    "💬 Comment",
                    callback_data="metadata:comment"
                )
            ],

            [
                InlineKeyboardButton(
                    "© Copyright",
                    callback_data="metadata:copyright"
                ),
                InlineKeyboardButton(
                    "⚙ Encoder",
                    callback_data="metadata:encoder"
                )
            ],

            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="home"
                )
            ]
        ])

    # ==================================================
    # Export
    # ==================================================

    @staticmethod
    def export():

        return InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🚀 Export",
                    callback_data="export:start"
                )
            ],

            [
                InlineKeyboardButton(
                    "📋 Summary",
                    callback_data="export:summary"
                ),
                InlineKeyboardButton(
                    "🔍 Preview",
                    callback_data="export:preview"
                )
            ],

            [
                InlineKeyboardButton(
                    "🗑 Clear Queue",
                    callback_data="export:clear"
                ),
                InlineKeyboardButton(
                    "❌ Cancel",
                    callback_data="export:cancel"
                )
            ],

            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="home"
                )
            ]
        ])

    # ==================================================
    # Workspace
    # ==================================================

    @staticmethod
    def workspace():

        return InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "📂 Assets",
                    callback_data="workspace:assets"
                ),
                InlineKeyboardButton(
                    "📜 History",
                    callback_data="workspace:history"
                )
            ],

            [
                InlineKeyboardButton(
                    "📋 Queue",
                    callback_data="workspace:queue"
                ),
                InlineKeyboardButton(
                    "🧹 Clear",
                    callback_data="workspace:clear"
                )
            ],

            [
                InlineKeyboardButton(
                    "ℹ Info",
                    callback_data="workspace:info"
                )
            ],

            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="home"
                )
            ]
        ])

    # ==================================================
    # Settings
    # ==================================================

    @staticmethod
    def settings():

        return InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "⚙ Output",
                    callback_data="settings:output"
                ),
                InlineKeyboardButton(
                    "🎞 Codec",
                    callback_data="settings:codec"
                )
            ],

            [
                InlineKeyboardButton(
                    "🌐 Language",
                    callback_data="settings:language"
                ),
                InlineKeyboardButton(
                    "📊 Progress",
                    callback_data="settings:progress"
                )
            ],

            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="home"
                )
            ]
        ])
    # ==================================================
    # Dynamic Audio Tracks
    # ==================================================

    @staticmethod
    def audio_tracks(streams):

        rows=[]

        if not streams:
            rows.append([
                InlineKeyboardButton(
                    "No Audio Tracks",
                    callback_data="ignore"
                )
            ])
        else:

            for stream in streams:

                language=(
                    stream.get("tags",{})
                    .get("language","und")
                    .upper()
                )

                title=(
                    stream.get("tags",{})
                    .get("title","Audio")
                )

                index=stream.get("index",0)

                rows.append([
                    InlineKeyboardButton(
                        f"🎵 {language} • {title}",
                        callback_data=f"audio:track:{index}"
                    )
                ])

        rows.append([
            InlineKeyboardButton(
                "⬅ Back",
                callback_data="menu:audio"
            )
        ])

        return InlineKeyboardMarkup(rows)

    # ==================================================
    # Dynamic Subtitle Tracks
    # ==================================================

    @staticmethod
    def subtitle_tracks(streams):

        rows=[]

        if not streams:
            rows.append([
                InlineKeyboardButton(
                    "No Subtitle Tracks",
                    callback_data="ignore"
                )
            ])
        else:

            for stream in streams:

                language=(
                    stream.get("tags",{})
                    .get("language","und")
                    .upper()
                )

                title=(
                    stream.get("tags",{})
                    .get("title","Subtitle")
                )

                index=stream.get("index",0)

                rows.append([
                    InlineKeyboardButton(
                        f"💬 {language} • {title}",
                        callback_data=f"subtitle:track:{index}"
                    )
                ])

        rows.append([
            InlineKeyboardButton(
                "⬅ Back",
                callback_data="menu:subtitle"
            )
        ])

        return InlineKeyboardMarkup(rows)

    # ==================================================
    # Pending Operations
    # ==================================================

    @staticmethod
    def queue(operations):

        rows=[]

        if not operations:

            rows.append([
                InlineKeyboardButton(
                    "Queue Empty",
                    callback_data="ignore"
                )
            ])

        else:

            for item in operations:

                rows.append([
                    InlineKeyboardButton(
                        f"📝 {item.operation}",
                        callback_data=f"queue:view:{item.id}"
                    )
                ])

        rows.append([
            InlineKeyboardButton(
                "🚀 Export",
                callback_data="export:start"
            )
        ])

        rows.append([
            InlineKeyboardButton(
                "🗑 Clear Queue",
                callback_data="workspace:clear"
            )
        ])

        rows.append([
            InlineKeyboardButton(
                "⬅ Back",
                callback_data="home"
            )
        ])

        return InlineKeyboardMarkup(rows)

    # ==================================================
    # Yes / No
    # ==================================================

    @staticmethod
    def yes_no(
        yes_callback,
        no_callback
    ):

        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "✅ Yes",
                    callback_data=yes_callback
                ),
                InlineKeyboardButton(
                    "❌ No",
                    callback_data=no_callback
                )
            ]
        ])

    # ==================================================
    # Processing
    # ==================================================

    @staticmethod
    def processing():

        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "❌ Cancel",
                    callback_data="export:cancel"
                )
            ]
        ])

    # ==================================================
    # Completed
    # ==================================================

    @staticmethod
    def completed():

        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📥 Download",
                    callback_data="export:download"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 Home",
                    callback_data="home"
                )
            ]
        ])

    # ==================================================
    # Empty Keyboard
    # ==================================================

    @staticmethod
    def empty():

        return InlineKeyboardMarkup([])
