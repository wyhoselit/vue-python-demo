import mlflow

def init_mlflow_tracking(experiment_name: str = "RAG_Pipeline_Experiment", tracking_uri: str = "./mlruns"):
    """
    Initializes MLflow tracking for experiments.

    Args:
        experiment_name: The name of the MLflow experiment.
        tracking_uri: The URI where MLflow tracking data will be stored.
    """
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)
    print(f"MLflow tracking initialized for experiment '{experiment_name}' at '{tracking_uri}'")

def log_embedding_model_params(model_name: str):
    """
    Logs embedding model parameters to MLflow.
    """
    with mlflow.start_run():
        mlflow.log_param("embedding_model_name", model_name)
        print(f"Logged embedding model: {model_name}")

def log_rag_params(chunk_size: int, chunk_overlap: int, n_results: int):
    """
    Logs RAG pipeline parameters to MLflow.
    """
    with mlflow.start_run():
        mlflow.log_param("chunk_size", chunk_size)
        mlflow.log_param("chunk_overlap", chunk_overlap)
        mlflow.log_param("n_results", n_results)
        print(f"Logged RAG parameters: chunk_size={chunk_size}, chunk_overlap={chunk_overlap}, n_results={n_results}")

def log_llm_metrics(model: str, usage: dict, finish_reason: str):
    """
    Logs LLM generation metrics to MLflow.
    """
    with mlflow.start_run():
        mlflow.log_param("llm_model", model)
        mlflow.log_metric("prompt_tokens", usage.get("prompt_tokens"))
        mlflow.log_metric("completion_tokens", usage.get("completion_tokens"))
        mlflow.log_metric("total_tokens", usage.get("total_tokens"))
        mlflow.log_param("finish_reason", finish_reason)
        print(f"Logged LLM metrics for model {model}")

def register_rag_model(run_id: str, model_name: str, model_path: str = "model"):
    """
    Registers a model in MLflow Model Registry.
    
    Args:
        run_id: The MLflow run ID containing the model.
        model_name: Name to register the model under.
        model_path: Path to the model artifact within the run.
    """
    model_uri = f"runs:/{run_id}/{model_path}"
    mlflow.register_model(model_uri, model_name)
    print(f"Registered model '{model_name}' from run {run_id}")

def register_rag_components(
    embedding_model_name: str,
    chroma_persist_directory: str,
    chunk_size: int,
    chunk_overlap: int,
    n_results: int
):
    """
    Registers RAG pipeline components (embedding model config, vector store config, retrieval params) as MLflow artifacts.
    
    This creates a run that logs all the RAG configuration as parameters and tags.
    """
    with mlflow.start_run() as run:
        mlflow.log_param("embedding_model", embedding_model_name)
        mlflow.log_param("chroma_persist_directory", chroma_persist_directory)
        mlflow.log_param("chunk_size", chunk_size)
        mlflow.log_param("chunk_overlap", chunk_overlap)
        mlflow.log_param("n_results", n_results)
        
        # Tag as RAG pipeline configuration
        mlflow.set_tag("type", "rag_pipeline_config")
        mlflow.set_tag("version", "1.0")
        
        print(f"Registered RAG components in run {run.info.run_id}")
        return run.info.run_id