import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from utils import get_incremental_merged_mrs_with_approvals, get_project_name

# Config
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    api_key = os.getenv("GITLAB_API_KEY")
    project_ids = os.getenv("PROJECT_IDS", "").split(',')

    if not api_key or not project_ids:
        raise EnvironmentError("GITLAB_API_KEY and PROJECT_IDS must be set")

    headers = {'PRIVATE-TOKEN': api_key}
    base_url = 'https://gitlab.com/api/v4'

    for project_id in map(str.strip, project_ids):
        if not project_id:
            continue

        logger.info(f"Fetching MRs for project {project_id}")
        project_name = get_project_name(project_id, headers, base_url).replace(" ", "_").replace("/", "_")
        output_path = OUTPUT_DIR / f"{project_name}_merged_mrs_with_approvals.jsonl"

        get_incremental_merged_mrs_with_approvals(
            project_id=project_id,
            project_name=project_name,
            headers=headers,
            base_url=base_url,
            output_path=output_path
        )

if __name__ == "__main__":
    main()
