import os
import mlflow
import numpy as np
from paramiko import SSHClient, AutoAddPolicy, RSAKey


def run_mlflow_code():
    """
    run a simple mlflow code that logs some random params values, and assign the outputs to:
        1. EC2 instance - results server (which connected to s3 bucket) and mlruns output
        2. S3 bucket - artifacts
    """

    # set mlflow's server as EC2
    mlflow.set_tracking_uri(os.environ['remote_server_uri'])

    # create / get experiment based on experiment name (experiment ID) will be set automatically
    experiment_name = 'Default'
    exp = mlflow.get_experiment_by_name(name=experiment_name)
    if not exp:
        experiment_id = mlflow.create_experiment(name=experiment_name,
                                                 artifact_location=os.environ['remote_server_uri'])
    else:
        experiment_id = exp.experiment_id
    mlflow.set_experiment(experiment_name=experiment_name)

    # generate random values to some parameters, and log them
    # run mlflow code and log results
    with mlflow.start_run():
        alpha, l1_ratio, rmse, r2, mae = np.random.uniform(0., 1., 5)
        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)
        run_name = mlflow.active_run().info.run_name
        run_id = mlflow.active_run().info.run_id

    return experiment_id, experiment_name, run_name, run_id


def copy_from_ec2_to_s3():
    """
    copy mlruns directory from ec2 to s3 bucket
    """

    # Connect to EC2 instance
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    private_key = RSAKey(filename=os.environ['ec2_private_key_path'])
    stdout = []

    try:
        # connect
        ssh.connect(os.environ['ec2_instance_ip'], username=os.environ['ec2_username'], pkey=private_key)
        # run linux command - copy mlruns directory from ec2 to s3
        copy_command = "aws s3 sync {} s3://{}/{}".format(os.environ['ec2_path'],
                                                          os.environ['s3_name'],
                                                          os.environ['s3_path'])
        # get output
        _, stdout, _ = ssh.exec_command(copy_command)
        stdout = stdout.read().decode().split("\n")

    finally:
        ssh.close()

    return stdout


def lambda_handler(event, context):
    experiment_id, experiment_name, run_name, run_id = run_mlflow_code()
    copy_output = copy_from_ec2_to_s3()
    return {"experiment_id": experiment_id,
            "experiment_name": experiment_name,
            "run_name": run_name,
            "run_id": run_id,
            "copy_output": copy_output}
