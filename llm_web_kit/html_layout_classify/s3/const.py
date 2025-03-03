SUCCESS_MARK_FILE = '_SUCCESS'
SUCCESS_MARK_FILE2 = '.SUCCESS'

FAILURE_MARK_FILE = '_FAILURE'
RESERVE_MARK_FILE = '_RESERVE'
SUMMARY_MARK_FILE = '_SUMMARY'
DELETED_MARK_FILE = '_DELETED'

FIELD_ID = 'id'
FIELD_SUB_PATH = 'sub_path'


def is_flag_field(f: str):
    return f.startswith('is_') or f.startswith('has_')


def is_acc_field(f: str):
    return f.startswith('acc_')
