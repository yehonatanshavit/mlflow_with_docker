import numpy as np
import mlflow


def lambda_handler(event, context):

    # For remote server only (AWS)
    remote_server_uri = "http://ec2-13-53-187-91.eu-north-1.compute.amazonaws.com:5000/"
    mlflow.set_tracking_uri(remote_server_uri)

    experiment_name = 'my-experiment-3'
    exp = mlflow.get_experiment_by_name(name=experiment_name)
    if not exp:
        experiment_id = mlflow.create_experiment(name=experiment_name,
                                                 artifact_location=remote_server_uri)
    else:
        experiment_id = exp.experiment_id

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

