import os
import hydra
import pandas as pd
from tqdm import tqdm
from omegaconf import DictConfig
from tqdm.contrib.logging import logging_redirect_tqdm

from src.utils import getLogger, createDirectory
from src.youtube_crawler import crawlYoutubeKey


@hydra.main(version_base="1.2", config_path="configs", config_name="keys.yaml")
def main(config: DictConfig = None) -> None:
    # set logger
    log = getLogger()
    log.propagate = False

    # check dir
    createDirectory(os.path.join(config.out_dir))
    createDirectory(os.path.join(config.input_dir))

    # load song.csv
    song_info_path = os.path.join(config.input_dir, config.songs_filename)
    log.info("Load song_info files to retrieve song_id from %s", song_info_path)
    song_info_df = pd.read_csv(song_info_path)[["SONG_ID", "SONG_TITLE", "ARTIST_NAME"]]

    log.info("Start song detail crawling ...")
    youtube_keys = []
    failed_crawling_song_ids = []
    for idx in tqdm(range(song_info_df.shape[0]), position=0, leave=True):
        id, title, artist = song_info_df.iloc[idx]
        with logging_redirect_tqdm():
            try:
                youtube_key = crawlYoutubeKey(id, title, artist, config.query_url, log)
                youtube_keys.append(youtube_key)
            except Exception as e:
                log.exception(e)
                failed_crawling_song_ids.append(id)

    if failed_crawling_song_ids:
        log.warn("Failed crawling song ids : %s", str(failed_crawling_song_ids))

    # save crwaling results
    csv_path = os.path.join(config.out_dir, config.keys_filename)
    log.info("Save concatencated song_info to %s", csv_path)
    youtube_keys_df = pd.DataFrame(youtube_keys)
    youtube_keys_df.to_csv(csv_path)


if __name__ == "__main__":
    main()
