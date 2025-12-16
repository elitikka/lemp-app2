from app import app
from unittest.mock import patch, MagicMock

def test_health():
    """Test health endpoint without requiring real database"""
    client = app.test_client()
    
    # Mock the database connection
    with patch('app.get_db_connection') as mock_db:
        # Create a mock connection that succeeds
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        
        response = client.get("/api/health")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"
        assert data["db"] == "healthy"

def test_health_db_failure():
    """Test health endpoint when database fails"""
    client = app.test_client()
    
    # Mock database connection to raise an error
    with patch('app.get_db_connection') as mock_db:
        mock_db.side_effect = Exception("Database connection failed")
        
        response = client.get("/api/health")
        
        assert response.status_code == 500
        data = response.get_json()
        assert data["status"] == "Failed"