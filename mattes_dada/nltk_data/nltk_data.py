import datetime
import os.path
import platform

import nltk.data

_data = {
    'punkt': 'tokenizers/punkt'
}

_locations = {
    'Darwin': '$HOME/Library/Mattes-dada',
    'Linux': '$HOME/.mattes-dada',
    'Windows': '%APPDATA%/Mattes-dada',
}

_location: str = None


def _init_location() -> None:
    """Select data directory based on operating system and add it to nltk search path."""
    system = platform.system()
    if system not in _locations:
        raise Exception('Unknown operating system:', system)
    else:
        global _location
        _location = os.path.expandvars(_locations[system])
    nltk.data.path.insert(0, _location)


def _is_file_expired(full_path, expiry: datetime.datetime) -> bool:
    """Check if given file was modified before 'expiry'

    :return: True if the file was modified before the expiry time, False otherwise
    """

    mod_time = os.stat(full_path).st_mtime
    return mod_time < expiry.timestamp()


def download(id_str: str) -> None:
    """Use nltk.download function to download data package identified by id_str.

    :param id_str: nltk data package name as per nltk_data index.xml
    """
    nltk.download(id_str, download_dir=_location, quiet=True, halt_on_error=False, raise_on_error=True)


def _update(id_str: str, path: str, expiry: datetime.datetime) -> None:
    """Check if the package has been downloaded and if its modification time is not before expiry time. If it's not, try downloading it

    :param id_str: package id
    :param path: relative package path, where nltk downloader unzips the package
    :param expiry: expiry time
     """
    full_path = os.path.join(_location, path)
    if not os.path.exists(full_path) or _is_file_expired(full_path, expiry):
        download(id_str)


def expiry_date(max_age_days: int) -> datetime.datetime:
    """Calculate expiry time, by subtracting max_age_days days from the current time.

    :param max_age_days: number of days
    """
    delta = datetime.timedelta(days=max_age_days)
    return datetime.datetime.utcnow() - delta


def init_nltk_data(max_age_days: int = 30) -> None:
    """Download nltk data packages or try updating them if they are old.

    :param max_age_days: if the file is older than this many days, it is considered old
    """
    _init_location()
    expiry = expiry_date(max_age_days)
    for id, path in _data.items():
        _update(id, path, expiry)
