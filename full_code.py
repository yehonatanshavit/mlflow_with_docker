import os
import mlflow
import numpy as np


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


def lambda_handler(event, context):
    experiment_id, experiment_name, run_name, run_id = run_mlflow_code()
    return {
        "experiment_id": experiment_id,
        "experiment_name": experiment_name,
        "run_name": run_name,
        "run_id": run_id,
    }
