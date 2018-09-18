from ..internal.DeadHoster import DeadHoster


class AuroravidTo(DeadHoster):
    __name__ = "AuroravidTo"
    __type__ = "hoster"
    __version__ = "0.01"
    __status__ = "testing"

    __pattern__ = r'https?://(?:www\.)?(?:auroravid|cloudtime)\.to/video/'
    __description__ = """Auroravid.to hoster plugin"""
    __license__ = "GPLv3"
    __authors__ = [("igel", None)]

