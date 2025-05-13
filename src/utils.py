import os
import json
import logging
import requests
import duckdb
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_request(url, headers, params=None):
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()

def get_project_name(project_id, headers, base_url):
    url = f"{base_url}/projects/{project_id}"
    return make_request(url, headers)['name_with_namespace']

def get_incremental_merged_mrs_with_approvals(
    project_id, project_name, headers, base_url, output_path,
    order_by='updated_at', sort='desc', per_page=100
):
    latest = get_latest_updated_at_from_jsonl(output_path)
    logger.info(f"Latest saved MR: {latest}")

    with open(output_path, 'a', encoding='utf-8') as out:
        page, new_items = 1, 0

        while True:
            url = f"{base_url}/projects/{project_id}/merge_requests"
            params = {
                'state': 'merged', 'per_page': per_page, 'page': page,
                'order_by': order_by, 'sort': sort
            }
            mrs = make_request(url, headers, params)
            if not mrs: break

            for mr in mrs:
                updated_at = mr.get('updated_at')
                if not updated_at: continue
                if latest and datetime.fromisoformat(updated_at.replace("Z", "+00:00")) <= latest:
                    logger.info(f"Stopping at already-saved MR: {updated_at}")
                    return

                mr.update({'project_id': project_id, 'project_name': project_name})

                try:
                    approval_url = f"{base_url}/projects/{project_id}/merge_requests/{mr['iid']}/approvals"
                    mr['approvals'] = make_request(approval_url, headers)
                except Exception as e:
                    logger.warning(f"Approval fetch failed for MR {mr['iid']}: {e}")
                    mr['approvals'] = None

                out.write(json.dumps(mr, ensure_ascii=False) + '\n')
                new_items += 1

            logger.info(f"Page {page}: {len(mrs)} MRs")
            page += 1

    logger.info(f"Done. {new_items} new MRs written to {output_path}")

def get_latest_updated_at_from_jsonl(path):
    if not os.path.exists(path):
        return None
    try:
        result = duckdb.sql(f"""
            SELECT MAX(updated_at) AS latest
            FROM read_ndjson('{path}', auto_detect=true, ignore_errors=true, maximum_object_size=50000000)
        """).fetchone()
        return datetime.fromisoformat(result[0].replace("Z", "+00:00")) if result and result[0] else None
    except Exception as e:
        logger.warning(f"Could not read latest timestamp from {path}: {e}")
        return None
