"""Integration tests for Excel reader"""
import pytest
from src.excel.reader import ExcelReader


def test_excel_reader_load_and_list_sheets(sample_excel_file):
    """Test loading workbook and listing sheets"""
    with ExcelReader(sample_excel_file) as reader:
        sheet_names = reader.load_workbook()
        
        assert len(sheet_names) == 1
        assert "TestData" in sheet_names


def test_excel_reader_select_sheet_and_get_headers(sample_excel_file):
    """Test selecting sheet and extracting headers"""
    with ExcelReader(sample_excel_file) as reader:
        reader.load_workbook()
        reader.select_sheet("TestData")
        
        headers = reader.get_headers()
        
        assert len(headers) == 3
        assert headers == ["Name", "Email", "Age"]


def test_excel_reader_get_row_count(sample_excel_file):
    """Test getting row count"""
    with ExcelReader(sample_excel_file) as reader:
        reader.load_workbook()
        reader.select_sheet("TestData")
        
        row_count = reader.get_row_count()
        
        assert row_count == 5


def test_excel_reader_iterate_rows(sample_excel_file):
    """Test iterating over data rows"""
    with ExcelReader(sample_excel_file) as reader:
        reader.load_workbook()
        reader.select_sheet("TestData")
        
        rows = list(reader.iterate_rows())
        
        assert len(rows) == 5
        assert rows[0]["Name"] == "John Doe"
        assert rows[0]["Email"] == "john@example.com"
        assert rows[0]["Age"] == "30"
        
        assert rows[4]["Name"] == "Charlie Wilson"
        assert rows[4]["Email"] == "charlie@example.com"
        assert rows[4]["Age"] == "42"


def test_excel_reader_iterate_rows_with_start_row(sample_excel_file):
    """Test iterating with start row parameter"""
    with ExcelReader(sample_excel_file) as reader:
        reader.load_workbook()
        reader.select_sheet("TestData")
        
        rows = list(reader.iterate_rows(start_row=3))
        
        assert len(rows) == 3  # Rows 3, 4, 5
        assert rows[0]["Name"] == "Bob Johnson"
        assert rows[1]["Name"] == "Alice Brown"
        assert rows[2]["Name"] == "Charlie Wilson"


def test_excel_reader_iterate_rows_with_max_rows(sample_excel_file):
    """Test iterating with max rows parameter"""
    with ExcelReader(sample_excel_file) as reader:
        reader.load_workbook()
        reader.select_sheet("TestData")
        
        rows = list(reader.iterate_rows(max_rows=2))
        
        assert len(rows) == 2
        assert rows[0]["Name"] == "John Doe"
        assert rows[1]["Name"] == "Jane Smith"


def test_excel_reader_formatted_values(sample_excel_file):
    """Test that formatted values match Excel display"""
    # This test verifies that numbers, dates, and strings are formatted correctly
    with ExcelReader(sample_excel_file) as reader:
        reader.load_workbook()
        reader.select_sheet("TestData")
        
        rows = list(reader.iterate_rows())
        
        # Age should be formatted as string
        assert rows[0]["Age"] == "30"
        assert isinstance(rows[0]["Age"], str)
        
        # Name and Email should be strings
        assert isinstance(rows[0]["Name"], str)
        assert isinstance(rows[0]["Email"], str)


def test_excel_reader_empty_cells(sample_excel_file):
    """Test handling of empty cells"""
    # The sample file doesn't have empty cells, but we test the behavior
    with ExcelReader(sample_excel_file) as reader:
        reader.load_workbook()
        reader.select_sheet("TestData")
        
        rows = list(reader.iterate_rows())
        
        # All cells should have values in our sample
        for row in rows:
            assert "Name" in row
            assert "Email" in row
            assert "Age" in row


def test_excel_reader_invalid_sheet(sample_excel_file):
    """Test error handling for invalid sheet"""
    with ExcelReader(sample_excel_file) as reader:
        reader.load_workbook()
        
        with pytest.raises(ValueError, match="Sheet 'InvalidSheet' not found"):
            reader.select_sheet("InvalidSheet")


def test_excel_reader_invalid_start_row(sample_excel_file):
    """Test error handling for invalid start row"""
    with ExcelReader(sample_excel_file) as reader:
        reader.load_workbook()
        reader.select_sheet("TestData")
        
        with pytest.raises(ValueError, match="start_row must be between 1 and"):
            list(reader.iterate_rows(start_row=10))


def test_excel_reader_no_sheet_selected(sample_excel_file):
    """Test error handling when no sheet is selected"""
    with ExcelReader(sample_excel_file) as reader:
        reader.load_workbook()
        
        with pytest.raises(ValueError, match="No sheet selected"):
            list(reader.iterate_rows())
