from typing import List, Union, Dict

from pysyncobj import SyncObj
from pysyncobj.batteries import ReplQueue

SYNC_OBJ: SyncObj = None
TASKS_QUEUE = ReplQueue()


def create_sync_obj(raft_host: str, partners: List[str]):
    global SYNC_OBJ
    if SYNC_OBJ:
        return

    SYNC_OBJ = SyncObj(raft_host, partners, consumers=[get_distributed_queue()])
    SYNC_OBJ.waitBinded()
    SYNC_OBJ.waitReady()


def get_sync_obj() -> Union[SyncObj, None]:
    global SYNC_OBJ
    if SYNC_OBJ:
        return SYNC_OBJ

    raise Exception('Sync object is not created')


def get_distributed_queue() -> ReplQueue:
    return TASKS_QUEUE


def get_status() -> Dict:
    status = get_sync_obj().getStatus()
    status['self'] = status['self'].address

    if status['leader']:
        status['leader'] = status['leader'].address

    serializable_status = {
        **status,
        'is_leader': status['self'] == status['leader'],
    }
    return serializable_status


def is_leader() -> bool:
    return get_status().get('is_leader', False)
