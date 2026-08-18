import pytest
from unittest.mock import MagicMock, patch, call

import mlflow
import mlflow.tracking

from app.modules.llm.rag.mlflow_tracker import (
    init_mlflow_tracking,
    log_embedding_model_params,
    log_rag_params,
    log_llm_metrics,
    register_rag_model,
    register_rag_components
)

# --- Test MLflow Tracking ---

@patch('mlflow.set_tracking_uri')
@patch('mlflow.set_experiment')
def test_init_mlflow_tracking(mock_set_experiment, mock_set_tracking_uri):
    init_mlflow_tracking("TestExperiment", "./test_mlruns")
    
    mock_set_tracking_uri.assert_called_once_with("./test_mlruns")
    mock_set_experiment.assert_called_once_with("TestExperiment")

@patch('mlflow.log_param')
@patch('mlflow.start_run')
def test_log_embedding_model_params(mock_start_run, mock_log_param):
    mock_start_run.return_value.__enter__.return_value = MagicMock()
    
    log_embedding_model_params("all-MiniLM-L6-v2")
    
    mock_start_run.assert_called_once()
    mock_log_param.assert_called_once_with("embedding_model_name", "all-MiniLM-L6-v2")

@patch('mlflow.log_param')
@patch('mlflow.start_run')
def test_log_rag_params(mock_start_run, mock_log_param):
    mock_start_run.return_value.__enter__.return_value = MagicMock()
    
    log_rag_params(1000, 200, 5)
    
    mock_start_run.assert_called_once()
    mock_log_param.assert_any_call("chunk_size", 1000)
    mock_log_param.assert_any_call("chunk_overlap", 200)
    mock_log_param.assert_any_call("n_results", 5)

@patch('mlflow.log_param')
@patch('mlflow.log_metric')
@patch('mlflow.start_run')
def test_log_llm_metrics(mock_start_run, mock_log_metric, mock_log_param):
    mock_start_run.return_value.__enter__.return_value = MagicMock()
    
    usage = {"prompt_tokens": 50, "completion_tokens": 10, "total_tokens": 60}
    log_llm_metrics("gpt-3.5-turbo", usage, "stop")
    
    mock_start_run.assert_called_once()
    mock_log_param.assert_any_call("llm_model", "gpt-3.5-turbo")
    mock_log_param.assert_any_call("finish_reason", "stop")
    mock_log_metric.assert_any_call("prompt_tokens", 50)
    mock_log_metric.assert_any_call("completion_tokens", 10)
    mock_log_metric.assert_any_call("total_tokens", 60)

@patch('mlflow.register_model')
def test_register_rag_model(mock_register_model):
    register_rag_model("run_123", "my-rag-model", "model")
    
    mock_register_model.assert_called_once_with("runs:/run_123/model", "my-rag-model")

@patch('mlflow.set_tag')
@patch('mlflow.log_param')
@patch('mlflow.start_run')
def test_register_rag_components(mock_start_run, mock_log_param, mock_set_tag):
    mock_run = MagicMock()
    mock_run.info.run_id = "run_456"
    mock_start_run.return_value.__enter__.return_value = mock_run
    
    run_id = register_rag_components(
        embedding_model_name="all-MiniLM-L6-v2",
        chroma_persist_directory="./chroma_db",
        chunk_size=1000,
        chunk_overlap=200,
        n_results=5
    )
    
    assert run_id == "run_456"
    mock_start_run.assert_called_once()
    
    mock_log_param.assert_any_call("embedding_model", "all-MiniLM-L6-v2")
    mock_log_param.assert_any_call("chroma_persist_directory", "./chroma_db")
    mock_log_param.assert_any_call("chunk_size", 1000)
    mock_log_param.assert_any_call("chunk_overlap", 200)
    mock_log_param.assert_any_call("n_results", 5)
    
    mock_set_tag.assert_any_call("type", "rag_pipeline_config")
    mock_set_tag.assert_any_call("version", "1.0")

# --- Test MLflow Model Registry Operations ---

@patch('mlflow.tracking.MlflowClient')
def test_model_registry_operations(mock_client_class):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    
    from mlflow.tracking import MlflowClient
    client = MlflowClient()
    
    mock_client.create_registered_model.return_value = None
    mock_client.create_model_version.return_value = MagicMock(version="1")
    
    client.create_registered_model("test-model")
    version = client.create_model_version(
        name="test-model",
        source="runs:/run_123/model",
        run_id="run_123"
    )
    
    assert version.version == "1"
    mock_client.create_registered_model.assert_called_once_with("test-model")
    mock_client.create_model_version.assert_called_once()

# --- Integration Test: MLflow with RAG Pipeline ---

@patch('mlflow.register_model')
@patch('mlflow.set_tag')
@patch('mlflow.log_metric')
@patch('mlflow.log_param')
@patch('mlflow.set_tracking_uri')
@patch('mlflow.set_experiment')
@patch('mlflow.start_run')
def test_rag_pipeline_mlflow_integration(
    mock_start_run,
    mock_set_experiment,
    mock_set_tracking_uri,
    mock_log_param,
    mock_log_metric,
    mock_set_tag,
    mock_register_model
):
    mock_start_run.return_value.__enter__.return_value = MagicMock()
    
    init_mlflow_tracking("RAG_Pipeline_Experiment")
    
    log_embedding_model_params("all-MiniLM-L6-v2")
    
    log_rag_params(1000, 200, 5)
    
    log_llm_metrics("gpt-3.5-turbo", {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150}, "stop")
    
    run_id = register_rag_components(
        "all-MiniLM-L6-v2",
        "./chroma_db",
        1000, 200, 5
    )
    
    mock_set_tracking_uri.assert_called_once_with("./mlruns")
    mock_set_experiment.assert_called_once_with("RAG_Pipeline_Experiment")
    mock_log_param.assert_any_call("embedding_model_name", "all-MiniLM-L6-v2")
    mock_log_param.assert_any_call("chunk_size", 1000)
    mock_log_param.assert_any_call("chunk_overlap", 200)
    mock_log_param.assert_any_call("n_results", 5)
    mock_log_param.assert_any_call("llm_model", "gpt-3.5-turbo")
    mock_log_param.assert_any_call("finish_reason", "stop")
    mock_log_metric.assert_any_call("prompt_tokens", 100)
    mock_log_metric.assert_any_call("completion_tokens", 50)
    mock_log_metric.assert_any_call("total_tokens", 150)
    mock_set_tag.assert_any_call("type", "rag_pipeline_config")
    mock_set_tag.assert_any_call("version", "1.0")
    mock_register_model.assert_not_called()