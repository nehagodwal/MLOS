from logging import getLogger
from pprint import pformat
from user_application.utils.shell_commands import run_cmd2
import uuid, time, subprocess
import pandas as pd

logger = getLogger(__name__)


class Job:
    """
    Represents a full experiment run and kicks off the
    driver/jobManagerTask using the configs setup by the notebook.
    """

    def __init__(self, storage_client, compute_pool):
        """Initializes the job with id and compute pool
        """
        # initializing the job class with storage and compute pool objects
        self.storage_client = storage_client
        self.compute_pool = compute_pool

        # creating a job id
        self.job_id = uuid.uuid4().hex
        
        # setup job dir for configs and output
        self.job_path = self.storage_client.setup_job_dir(self.job_id)

        # uploading configs for the job
        self.storage_client.upload_config(self.job_id)

        # stopping condition for the job
        self.config = self.storage_client.read_job_config_yaml(self.job_id)
        self.stopping_condition = self.config['MLOS']['stopping_condition']

        self.create_env_file()

    def get_job_id(self):
        return self.job_id

    def get_start_time(self):
        return self.job_start_time

    def get_job_runtime(self):
        return time.time() - self.job_start_time
    
    def get_consolidated_results(self):
        return pd.read_csv('MLOS_executor_dir/job_1/output/user_task_consolidated_results.csv')

    def status(self):
        """Get the status of the job
        """
        f = subprocess.Popen(['tail','-F',"MLOS_executor_dir/job_1/output/driver.log"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        
        time = 0
        while time<10:
            line = f.stdout.readline()
            print(line)
            time=time+1

    def worker_task_status(self):
        """Get the status of the job
        """
        f1 = subprocess.Popen(['tail','-F',"MLOS_executor_dir/job_1/worker_1/output/celery.log"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)                                                                                                                                                       
        time1 = 0
        while time1<10:
            line1 = f1.stdout.readline()
            print(line1)
            time1=time1+1

    def user_task_status(self):
        """Get the status of the job
        """
        f2 = subprocess.Popen(['tail','-F',"MLOS_executor_dir/job_1/output/user_task.log"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)                                                       
        time2 = 0
        while time2<10:
            line2 = f2.stdout.readline()
            print(line2)
            time2=time2+1

    def create_env_file(self):
        local_ip_address = self.config[self.config['deployment']]['local_node_ip_address']
        with open(".env", "w") as f:
            f.write("MASTER_CONTAINER_NAME=driver_container\n")
            f.write(f'HOST_NAME={local_ip_address}\n')
            f.write("MASTER_CONTEXT=/home/azureuser/executor\n")
            f.write("WORKER_CONTAINER_NAME=worker_executor\n")
            f.write("WORKER_HOST_NAME=10.0.0.4\n")
            f.write(f'JOB_MOUNT_DIR={self.job_path}\n')

    def run_setup(self):
        # build the driver container
        self._build_driver()
        # build the master container
        self._build_worker()

    def start_job(self):
        self._build_driver()
        self._build_worker()
        # launch the worker container
        self._launch_worker()
        # launch the driver container
        self._launch_driver()
        #return self.get_job_id()
        
    def _build_driver(self):
        """
        Builds a driver container
        """
        driver_file = self.config['driver_setup']
        logger.info(f'Building driver using the file: {driver_file}')
        build_cmd_str = f'sudo docker-compose -f {driver_file} build'
        run_cmd2(build_cmd_str)
        logger.info('Driver build completed!')

    def _build_worker(self):
        """
        Builds a worker container
        """
        worker_file = self.config['worker_setup']
        logger.info(f'Building worker using the file: {worker_file}')
        build_cmd_str = f'sudo docker-compose -f {worker_file} build'
        run_cmd2(build_cmd_str)
        logger.info('Worker build completed!')

    def _launch_driver(self):
        """
        Launches driver container
        """
        driver_file = self.config['driver_setup']
        #driver_file = self.compute_pool.deployment['driver_setup']
        logger.info(f'Launching driver using the file: {driver_file}')
        launch_str = f'sudo docker-compose -f {driver_file} config && sudo docker-compose -f {driver_file} up --force-recreate -d'
        #run_cmd2(launch_str)
        subprocess.run(launch_str, shell=True, check=True)
        logger.info('Driver launched successfully!')

    def _launch_worker(self):
        """
        Launches a worker container
        """
        worker_file = self.config['worker_setup']   
        logger.info(f'Launching worker using the file: {worker_file}')
        launch_str = f'sudo docker-compose -f {worker_file} config && sudo docker-compose -f {worker_file} up --force-recreate -d'
        #run_cmd2(launch_str)
        subprocess.run(launch_str, shell=True, check=True)
        logger.info('Worker launched successfully!')

    def _shutdown_driver(self):
        """
        Shutdown a driver container
        """
        driver_file = self.config['driver_setup']
        logger.info(f'Shutting down driver using the file: {driver_file}')
        launch_str = f'sudo docker-compose -f {driver_file} down'
        #run_cmd2(launch_str)
        subprocess.run(launch_str, shell=True, check=True)
        logger.info('Driver shutdown successfully!')

    def _shutdown_worker(self):
        """
        Shutdown a worker container
        """
        worker_file = self.config['worker_setup']
        logger.info(f'Shutting down driver using the file: {worker_file}')
        launch_str = f'sudo docker-compose -f {worker_file} down'
        #run_cmd2(launch_str)
        subprocess.run(launch_str, shell=True, check=True)
        logger.info('Worker shutdown successfully!')

    # def set_environment(self):
    #     yml_fp = os.path.join(config.DOCKER['app_path'], config.DOCKER['master_yml_file'])
    #     with open(yml_fp) as f:
    #         doc = yaml.safe_load(f)
    #     doc['services']['driver']['environment']['JOB_STORAGE_PATH'] = self.job_path
    #     with open(yml_fp, 'w') as f:
    #         yaml.safe_dump(doc, f, default_flow_style=False)
