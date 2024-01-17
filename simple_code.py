import os

import numpy as np
import mlflow


def lambda_handler(event, context):

    # determine if the outputs should be saved in a remote server based on input / default
    if "save_in_remote" in event.keys():
        save_in_remote = event['save_in_remote']
    else:
        save_in_remote = False

    # set remote URL of AWS (if required)
    if save_in_remote:
        remote_server_uri = os.environ['remote_server_uri']
        mlflow.set_tracking_uri(remote_server_uri)

    # set experiment name, create and set it. experiment's ID would be set automatically
    experiment_name = 'Default'
    exp = mlflow.get_experiment_by_name(name=experiment_name)
    if not exp:
        if save_in_remote:
            experiment_id = mlflow.create_experiment(name=experiment_name,
                                                     artifact_location=remote_server_uri)
        else:
            experiment_id = mlflow.create_experiment(name=experiment_name)

    else:
        experiment_id = exp.experiment_id
    # important! else, that data will be saved in "default" which is mlruns/0
    mlflow.set_experiment(experiment_name=experiment_name)

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

    return {'statusCode': 200,
            'body': "you have just used Mlflow with lambda",
            'experiment_name': experiment_name,
            'experiment_id': experiment_id,
            'run_name': run_name,
            'run_id': run_id,
            'alpha': alpha,
            'l1_ratio': l1_ratio,
            'rmse': rmse,
            'r2': r2,
            'mae': mae}

