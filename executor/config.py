# Notes:
    # python code instead of dictionaries
    # have a verified code in that case
    # 
# MLOS optimizer details
MLOS = {
    'input_simple_hypergrid' : {
        'name' : '',
        'dimension' : '',
    },

    'output_simple_hypergrid' : {
        'name' : '',
        'dimension' : '',
        'objective' : '',
    }, 

    'bayesian_optimizer_config' : {
        'start' : 'default', # start from the default configuration
        'random_suggestions_fraction' : 0.1,
        'random_forest' : 'homogeneous_random_forest_regression_model_config', # random forest surrogate model
        'random_forest_refit_sample' : 1,
        'random_forest_splitter' : '',
        'random_forest_samples_fraction_per_estimator' : 0.9,
        'random_forest_n_estimators' : 10,
        'random_forest_confidence_bound' : 0.1,

    }, 

    'iteration_count' : 100
}

# Deployments

# Local Batch details
LOCAL = {
    'master_node_ip_address' : '',
    'instance_type' : {
        'name': 'local',
        # Storage-related vars
        'disk_mount_point' : '',
        'disk_backup_mount_point' : '',
        'mem_backup_mount_point' : '',
        # Container isolation / restriction vars
        'cpuset_cpus_driver': 0-3,
        'cpuset_cpus_workload': 4-7,
        'mem_limit_driver': '8G',
        'mem_limit_workload': '8G',
        'deploy_dir': ''
    }
}
  
# Azure Storage account/Batch details
AZURE_BATCH = {
    '_BATCH_ACCOUNT_NAME' : '',  # Your batch account name
    '_BATCH_ACCOUNT_KEY' : '',  # Your batch account key
    '_BATCH_ACCOUNT_URL' : '',  # Your batch account URL
    '_STORAGE_ACCOUNT_NAME' : '',  # Your storage account name
    '_STORAGE_ACCOUNT_KEY' : '',  # Your storage account key
    '_POOL_ID' : '',  # Your Pool ID
    '_POOL_NODE_COUNT' : 2,  # Pool node count
    '_POOL_VM_SIZE' : '',  # VM Type/Size
    '_JOB_ID' : '',  # Job ID
    '_STANDARD_OUT_FILE_NAME' : ''  # Standard Output file
}

CLOUD_LAB = {
    'master_node_ip_address': '10.10.1.1',
    'instance_type': '',

    'user': '',
    'user_dir': '',
    'deploy_dir': '',

    # Needed by fabric deployment script
    'private_key_filepath' : '',
    'linux_packages' : {},
    'framework_packages' : {},
    'python_packages' : {}
}
