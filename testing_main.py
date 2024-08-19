from datetime import datetime
from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest
from main import app, validate_dates

client = TestClient(app)

# Cases for Date Validation.
def test_dates_valid():
    start_date = "2023-05-01"
    end_date = "2023-05-15"

    result = validate_dates(start_date, end_date)

    assert len(result) == 2
    assert result[0] == datetime.strptime(start_date, "%Y-%m-%d")
    assert result[1] == datetime.strptime(end_date, "%Y-%m-%d")

def test_invalid_dates():
    start_date = "2023-05-15"
    end_date = "2023-05-01"

    with pytest.raises(HTTPException) as execution:
        validate_dates(start_date, end_date)

    assert execution.value.status_code == 400
    assert execution.value.detail == "End date must be later than start date."

def test_invalid_dates_format():
    start_date = "01-05-2023"
    end_date = "2023-05-15"

    with pytest.raises(HTTPException) as execution:
        validate_dates(start_date, end_date)
    
    assert execution.value.status_code == 400
    assert execution.value.detail == "Invalid date format. Use YYYY-MM-DD."

# Cases for endpoint resources.
def test_sync_files_two_dates_invalid():
    start_date = "2023-05-01"
    end_date = "2023-05-21"
    
    response = client.get(f"/syncTwoDates?start_date={start_date}&end_date={end_date}")
    
    assert response.status_code == 404
    assert response.text == '{"detail":"dms-responses/2023-05-21.jsonl >> File Not Found"}'
    
def test_sync_files_two_dates_valid():
    start_date = "2023-05-01"
    end_date = "2023-05-02"
    
    response = client.get(f"/syncTwoDates?start_date={start_date}&end_date={end_date}")

    assert response.status_code == 200