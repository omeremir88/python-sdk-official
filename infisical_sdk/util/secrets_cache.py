from typing import Dict, Tuple, Any

from infisical_sdk.api_types import BaseSecret
import json
import time
import threading
from hashlib import sha256
import pickle

class SecretsCache:
    def __init__(self, ttl_seconds: int = 300) -> None:
      if ttl_seconds is None or ttl_seconds <= 0:
          self.enabled = False
          return
    
      self.enabled = True
      self.ttl = ttl_seconds
      self.cleanup_interval = 60

      self.cache: Dict[str, Tuple[bytes, float]] = {}

      self.lock = threading.RLock()

      self.stop_cleanup_thread = False
      self.cleanup_thread = threading.Thread(target=self._cleanup_worker, daemon=True)
      self.cleanup_thread.start()

    def compute_cache_key(self, operation_name: str, **kwargs) -> str:
      sorted_kwargs = sorted(kwargs.items())
      json_str = json.dumps(sorted_kwargs)

      print(f"Cache key: {operation_name}:{json_str}")

      return sha256(f"{operation_name}:{json_str}".encode()).hexdigest()
  
    def get(self, cache_key: str) -> Any:
      if not self.enabled:
        return None

      with self.lock:
          if cache_key in self.cache:
              serialized_value, timestamp = self.cache[cache_key]
              if time.time() - timestamp <= self.ttl:
                  print(f"Cache hit: {cache_key}")
                  return pickle.loads(serialized_value)
              else:
                  print(f"Cache miss (expired): {cache_key}")
                  del self.cache[cache_key]
                  return None
          else:
              print(f"Cache miss (not in cache): {cache_key}")
              return None
            
            
    def set(self, cache_key: str, value: Any) -> None:
      if not self.enabled:
        return

      with self.lock:
        serialized_value = pickle.dumps(value)
        self.cache[cache_key] = (serialized_value, time.time())

    def unset(self, cache_key: str) -> None:
      if not self.enabled:
        return

      with self.lock:
        del self.cache[cache_key]


    def _cleanup_expired_items(self) -> None:
      """Remove all expired items from the cache."""
      current_time = time.time()
      with self.lock:
          expired_keys = [
              key for key, (_, timestamp) in self.cache.items() 
              if current_time - timestamp > self.ttl
          ]
          for key in expired_keys:
              del self.cache[key]
  
    def _cleanup_worker(self) -> None:
      """Background worker that periodically cleans up expired items."""
      while not self.stop_cleanup_thread:
        time.sleep(self.cleanup_interval)
        self._cleanup_expired_items()

    def __del__(self) -> None:
      """Ensure thread is properly stopped when the object is garbage collected."""
      self.stop_cleanup_thread = True
      if self.enabled and self.cleanup_thread.is_alive():
        self.cleanup_thread.join(timeout=1.0)
        
        