import argparse
import logging
from pathlib import Path

"""
Music album metadata tagger from MusicBrainz database
"""



def setup_logging(level=logging.INFO):
    """Configure logging for the application."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Tag your album with MusicBrainz metadata information'
    )
    parser.add_argument(
        'musicbrainz_url',
        help='MusicBrainz release URL'
    )
    parser.add_argument(
        '--music-dir',
        type=Path,
        default=Path.home() / 'Music',
        help='Directory to search for music files'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        help='Output directory for tagged files'
    )
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Remove existing metadata before tagging'
    )
    return parser.parse_args()


def main():
    """Main application entry point."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    args = parse_arguments()
    logger.info(f'Starting tagger for release: {args.musicbrainz_url}')
    
    # TODO: Implement core functionality
    logger.info('Application complete')


if __name__ == '__main__':
    main()