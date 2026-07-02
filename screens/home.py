from bot.keyboards.main import main_menu
from core.media_summary import create_summary
from models.media_asset import MediaAsset


class HomeScreen:
    """
    Builds the main workspace screen.
    """

    @staticmethod
    def build(asset: MediaAsset, pending_count: int = 0):

        text = create_summary(asset)

        text += "\n\n━━━━━━━━━━━━━━━━━━"

        text += f"\n🛠 Pending Changes : {pending_count}"

        if pending_count == 0:
            text += "\nStatus : Ready"
        else:
            text += "\nStatus : Waiting for Export"

        return {
            "text": text,
            "reply_markup": main_menu()
        }
