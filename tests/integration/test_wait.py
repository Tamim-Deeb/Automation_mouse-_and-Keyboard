"""Integration tests for wait module"""
import time
import pytest
from src.automation.wait import WaitModule


def test_wait_sleep_minimum_duration():
    """Test that minimum 50ms delay is enforced"""
    wait = WaitModule()
    
    # Request 10ms (below minimum)
    start = time.time()
    wait.sleep(10)
    elapsed_ms = (time.time() - start) * 1000
    
    # Should enforce minimum 50ms
    assert elapsed_ms >= 45  # Allow some tolerance


def test_wait_sleep_normal_duration():
    """Test normal sleep duration"""
    wait = WaitModule()
    
    # Request 100ms
    start = time.time()
    wait.sleep(100)
    elapsed_ms = (time.time() - start) * 1000
    
    # Should be approximately 100ms (allow some tolerance)
    assert 90 <= elapsed_ms <= 150


def test_wait_sleep_longer_duration():
    """Test longer sleep duration"""
    wait = WaitModule()
    
    # Request 500ms
    start = time.time()
    wait.sleep(500)
    elapsed_ms = (time.time() - start) * 1000
    
    # Should be approximately 500ms (allow some tolerance)
    assert 450 <= elapsed_ms <= 600


def test_wait_sleep_zero_duration():
    """Test that zero duration enforces minimum"""
    wait = WaitModule()
    
    # Request 0ms
    start = time.time()
    wait.sleep(0)
    elapsed_ms = (time.time() - start) * 1000
    
    # Should enforce minimum 50ms
    assert elapsed_ms >= 45


def test_wait_get_min_delay():
    """Test getting minimum delay"""
    min_delay = WaitModule.get_min_delay()
    
    assert min_delay == 50


def test_wait_validate_duration_valid():
    """Test validating a valid duration"""
    assert WaitModule.validate_duration(50) is True
    assert WaitModule.validate_duration(100) is True
    assert WaitModule.validate_duration(1000) is True


def test_wait_validate_duration_invalid():
    """Test validating an invalid duration"""
    assert WaitModule.validate_duration(0) is False
    assert WaitModule.validate_duration(10) is False
    assert WaitModule.validate_duration(49) is False
    assert WaitModule.validate_duration(-100) is False


def test_wait_multiple_sleeps():
    """Test multiple consecutive sleeps"""
    wait = WaitModule()
    
    start = time.time()
    wait.sleep(50)
    wait.sleep(50)
    wait.sleep(50)
    elapsed_ms = (time.time() - start) * 1000
    
    # Should be approximately 150ms (allow some tolerance)
    assert 130 <= elapsed_ms <= 200


def test_wait_sleep_negative_duration():
    """Test that negative duration enforces minimum"""
    wait = WaitModule()
    
    # Request negative duration
    start = time.time()
    wait.sleep(-100)
    elapsed_ms = (time.time() - start) * 1000
    
    # Should enforce minimum 50ms
    assert elapsed_ms >= 45


def test_wait_sleep_exactly_minimum():
    """Test sleeping exactly the minimum duration"""
    wait = WaitModule()
    
    # Request exactly 50ms
    start = time.time()
    wait.sleep(50)
    elapsed_ms = (time.time() - start) * 1000
    
    # Should be approximately 50ms (allow some tolerance)
    assert 40 <= elapsed_ms <= 80
