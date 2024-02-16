import logging as logger
from datetime import datetime
from time import sleep
from typing import Generator

from decorators import backoff, coroutine, create_session
from elastic.indexes import GenresIndex, Index, MoviesIndex, PersonsIndex
from repository import (BaseRepository, FilmWorkRepository, GenreRepository,
                        PersonRepository)
from states.redis_storage import RedisStorage
from states.state import State

STATE_KEY = 'last_{index}_updated'


def repository_index():
    return [
        {
            'repository': FilmWorkRepository,
            'index': MoviesIndex,
        },
        {
            'repository': GenreRepository,
            'index': GenresIndex,
        },
        {
            'repository': PersonRepository,
            'index': PersonsIndex,
        },
    ]


@coroutine
@create_session
@backoff(start_sleep_time=0.1, factor=2, border_sleep_time=100)
def fetch_changed_objects(next_node: Generator,
                          session) -> Generator[None, datetime, None]:
    '''
    checks if there any updated movies
    '''
    while data := (yield):
        last_modified = data['last_modified']
        repository: BaseRepository = data['repository']
        with session:
            records_per_page = 100
            offset = 0
            while True:
                query = repository.last_updateds(
                    limit=records_per_page, offset=offset, updated_at=last_modified)
                result = session.execute(query)
                objects = result.mappings().all()
                # break the loop if there is no data
                if not result or not objects:
                    break
                data['objects'] = objects
                data['modified'] = str(objects[-1]['modified'])
                offset += records_per_page
                next_node.send(data)


@coroutine
@backoff(start_sleep_time=0.1, factor=2, border_sleep_time=100)
def save_data(next_node: Generator) -> Generator[None, list, None]:
    '''
    saves the updated objects to ES

    '''
    while data := (yield):
        objects = data['objects']
        index: Index = data['index']
        index.put_data(data=objects)
        logger.info(f'Received for saving {len(objects)} movies')
        next_node.send(data)


@coroutine
@backoff(start_sleep_time=0.1, factor=2, border_sleep_time=100)
def save_state(state: State) -> Generator[None, list, None]:
    '''
    saves the modified field into state
    '''
    while data := (yield):
        modified = data['modified']
        index = data['index']
        logger.info(f'Recived for saving last updated at: {modified} to state')
        state.set_state(STATE_KEY.format(index=index), modified)


@backoff(start_sleep_time=0.1, factor=2, border_sleep_time=100)
def main():
    state = State(RedisStorage())
    repo_ind = repository_index()
    state_saver_coro: Generator = save_state(state)
    movies_saver_coro: Generator = save_data(next_node=state_saver_coro)
    fetcher_coro: Generator = fetch_changed_objects(
        next_node=movies_saver_coro)
    while True:
        for data in repo_ind:
            data['last_modified'] = state.get_state(
                STATE_KEY.format(
                    index=data['index'])) or str(
                datetime.min)
            fetcher_coro.send(data)
        sleep(15)


if __name__ == "__main__":
    main()
