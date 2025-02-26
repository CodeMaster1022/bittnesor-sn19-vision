from validation.db import constants as cst


##### Insert


def insert_reward_data() -> str:
    return f"""
    INSERT INTO {cst.TABLE_REWARD_DATA} (
        {cst.COLUMN_ID}, {cst.COLUMN_TASK}, {cst.COLUMN_AXON_UID},
        {cst.COLUMN_QUALITY_SCORE}, {cst.COLUMN_VALIDATOR_HOTKEY},
        {cst.COLUMN_MINER_HOTKEY}, {cst.COLUMN_SYNTHETIC_QUERY},
        {cst.COLUMN_SPEED_SCORING_FACTOR}, {cst.COLUMN_RESPONSE_TIME}, {cst.COLUMN_VOLUME}
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """


def insert_uid_record() -> str:
    return f"""
    INSERT INTO {cst.TABLE_UID_RECORDS} (
        {cst.COLUMN_AXON_UID}, {cst.COLUMN_MINER_HOTKEY}, {cst.COLUMN_VALIDATOR_HOTKEY}, {cst.COLUMN_TASK},
        {cst.COLUMN_DECLARED_VOLUME}, {cst.COLUMN_CONSUMED_VOLUME}, {cst.COLUMN_TOTAL_REQUESTS_MADE},
        {cst.COLUMN_REQUESTS_429}, {cst.COLUMN_REQUESTS_500}, {cst.COLUMN_PERIOD_SCORE}
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """


def insert_task() -> str:
    return f"""
    INSERT INTO {cst.TABLE_TASKS} ({cst.COLUMN_TASK_NAME}, {cst.COLUMN_CHECKING_DATA}, {cst.COLUMN_MINER_HOTKEY}) VALUES (?, ?, ?)
    """


##### Delete stuff
def delete_task_by_hotkey() -> str:
    return f"""
    DELETE FROM {cst.TABLE_TASKS} WHERE {cst.COLUMN_MINER_HOTKEY} = ?
    """


def delete_reward_data_by_hotkey() -> str:
    return f"""
    DELETE FROM {cst.TABLE_REWARD_DATA} WHERE {cst.COLUMN_MINER_HOTKEY} = ?
    """


def delete_uid_data_by_hotkey() -> str:
    return f"""
    DELETE FROM {cst.TABLE_UID_RECORDS} WHERE {cst.COLUMN_MINER_HOTKEY} = ?
    """


def delete_task_data_older_than() -> str:
    return f"""
    DELETE FROM {cst.TABLE_TASKS} WHERE {cst.COLUMN_CREATED_AT} < ?
    """


def delete_reward_data_older_than() -> str:
    return f"""
    DELETE FROM {cst.TABLE_REWARD_DATA} WHERE {cst.COLUMN_CREATED_AT} < ?
    """


def delete_uid_data_older_than() -> str:
    return f"""
    DELETE FROM {cst.TABLE_UID_RECORDS} WHERE {cst.COLUMN_CREATED_AT} < ?
    """


def delete_oldest_rows_from_tasks(limit: int = 10) -> str:
    return f"""
    DELETE FROM {cst.TABLE_TASKS}
    WHERE {cst.COLUMN_ID} IN (
        SELECT {cst.COLUMN_ID} FROM {cst.TABLE_TASKS} ORDER BY {cst.COLUMN_CREATED_AT} ASC LIMIT {limit}
    )
    """


def delete_specific_task() -> str:
    return f"""
    DELETE FROM {cst.TABLE_TASKS} WHERE {cst.COLUMN_TASK_NAME} = ? AND {cst.COLUMN_CHECKING_DATA} = ?
    """


#### Select
def select_tasks_and_number_of_results() -> str:
    return f"""
    SELECT {cst.COLUMN_TASK_NAME}, COUNT(*) FROM {cst.TABLE_TASKS} GROUP BY {cst.COLUMN_TASK_NAME}
    """

def select_number_of_rewards_for_each_task() -> str:
    return f"""
    SELECT {cst.TABLE_TASKS}.{cst.COLUMN_TASK_NAME},
           COUNT({cst.TABLE_REWARD_DATA}.{cst.COLUMN_ID}) AS reward_count
    FROM {cst.TABLE_TASKS}
    LEFT JOIN {cst.TABLE_REWARD_DATA}
    ON {cst.TABLE_TASKS}.{cst.COLUMN_TASK_NAME} = {cst.TABLE_REWARD_DATA}.{cst.COLUMN_TASK}
    GROUP BY {cst.TABLE_TASKS}.{cst.COLUMN_TASK_NAME}
    """


def select_count_of_rows_in_tasks() -> str:
    return f"""
    SELECT COUNT(*) FROM {cst.TABLE_TASKS}
    """


def select_count_rows_of_task_stored_for_scoring() -> str:
    return f"""
    SELECT COUNT(*) FROM {cst.TABLE_TASKS} WHERE {cst.COLUMN_TASK_NAME} = ?
    """

def select_task_for_deletion() -> str:
    return f"""
    SELECT t.{cst.COLUMN_CHECKING_DATA}, t.{cst.COLUMN_MINER_HOTKEY}
    FROM {cst.TABLE_TASKS} t
    LEFT JOIN (
        SELECT {cst.COLUMN_MINER_HOTKEY}, COUNT(*) as reward_count
        FROM {cst.TABLE_REWARD_DATA}
        WHERE {cst.COLUMN_TASK} = ?
        GROUP BY {cst.COLUMN_MINER_HOTKEY}
    ) r ON t.{cst.COLUMN_MINER_HOTKEY} = r.{cst.COLUMN_MINER_HOTKEY}
    WHERE t.{cst.COLUMN_TASK_NAME} = ?
    ORDER BY COALESCE(r.reward_count, 0) ASC
    LIMIT 1
    """



def select_recent_reward_data_for_a_task():
    return f"""
    SELECT * FROM {cst.TABLE_REWARD_DATA}
    WHERE {cst.COLUMN_TASK} = ?
    AND {cst.COLUMN_CREATED_AT} > ?
    AND {cst.COLUMN_MINER_HOTKEY} = ?
    ORDER BY {cst.COLUMN_CREATED_AT} DESC
    """


def select_recent_reward_data():
    return f"""
    SELECT
        id,
        task,
        axon_uid,
        quality_score,
        validator_hotkey,
        miner_hotkey,
        synthetic_query,
        speed_scoring_factor,
        response_time,
        volume,
        created_at
    FROM {cst.TABLE_REWARD_DATA}
    WHERE {cst.COLUMN_CREATED_AT} > ?
    AND {cst.COLUMN_MINER_HOTKEY} = ?
    ORDER BY {cst.COLUMN_CREATED_AT} DESC
    LIMIT ?
    """


def select_uid_period_scores_for_task():
    return f"""
    SELECT
        {cst.COLUMN_PERIOD_SCORE},
        {cst.COLUMN_CONSUMED_VOLUME},
        {cst.COLUMN_CREATED_AT}
    FROM {cst.TABLE_UID_RECORDS}
    WHERE {cst.COLUMN_TASK} = ?
    AND {cst.COLUMN_MINER_HOTKEY} = ?
    """
