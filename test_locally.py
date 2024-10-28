import os
import sys
from training import main
os.environ['WANDB_MODE'] = 'offline'

if __name__ == "__main__":
    sys.argv = [sys.argv[0], "--job_name", "test_run"]
    main()