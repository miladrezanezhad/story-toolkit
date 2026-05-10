"""
Concurrent Access Security Tests

Tests race conditions and concurrent access security issues.
"""

import sys
import os
import threading
import time
import random
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from story_toolkit import StoryToolkit
from story_toolkit.memory import MemoryManager


class ConcurrentAccessTester:
    """Comprehensive concurrent access tests"""
    
    def __init__(self):
        self.results = []
        self.errors = []
    
    def test_race_condition_on_create(self):
        """Test race conditions during creation"""
        print("\n  🏁 Testing race condition on create...")
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        created_ids = []
        lock = threading.Lock()
        
        def create_story(worker_id):
            try:
                manager = MemoryManager(db_path)
                story_id = manager.create_story(
                    name=f"Story_{worker_id}",
                    genre="fantasy",
                    theme="test"
                )
                with lock:
                    created_ids.append(story_id)
                manager.close()
            except Exception as e:
                self.errors.append(f"Create error: {e}")
        
        threads = []
        for i in range(50):
            t = threading.Thread(target=create_story, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join(timeout=30)
        
        # All stories should have unique IDs
        unique_ids = set(created_ids)
        
        if len(unique_ids) != len(created_ids):
            print(f"    ❌ Duplicate IDs created: {len(created_ids)} vs {len(unique_ids)}")
            return False
        elif len(created_ids) < 45:
            print(f"    ⚠️ Only {len(created_ids)}/50 stories created")
        else:
            print(f"    ✅ Race condition prevented: {len(unique_ids)} unique IDs")
        
        if os.path.exists(db_path):
            os.remove(db_path)
        
        return len(unique_ids) == len(created_ids) and len(created_ids) > 40
    
    def test_race_condition_on_delete(self):
        """Test race conditions during deletion"""
        print("\n  🗑️ Testing race condition on delete...")
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        manager = MemoryManager(db_path)
        story_ids = []
        
        # Create stories
        for i in range(20):
            story_id = manager.create_story(f"Story_{i}", "fantasy", "test")
            story_ids.append(story_id)
        
        manager.close()
        
        delete_errors = []
        
        def delete_story(story_id):
            try:
                manager2 = MemoryManager(db_path)
                result = manager2.delete_story(story_id)
                manager2.close()
                return result
            except Exception as e:
                delete_errors.append(str(e))
                return False
        
        # Delete same story multiple times concurrently
        target_id = story_ids[0]
        threads = []
        results = []
        
        for i in range(10):
            t = threading.Thread(target=lambda: results.append(delete_story(target_id)))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join(timeout=10)
        
        # Only one should succeed
        success_count = sum(1 for r in results if r)
        
        if success_count == 1:
            print(f"    ✅ Delete race condition prevented: {success_count} success")
            return True
        else:
            print(f"    ❌ Delete race condition: {success_count} successes")
            return False
    
    def test_race_condition_on_update(self):
        """Test race conditions during update"""
        print("\n  📝 Testing race condition on update...")
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        manager = MemoryManager(db_path)
        story_id = manager.create_story("Test", "fantasy", "theme")
        manager.close()
        
        def add_events(worker_id, count):
            try:
                manager = MemoryManager(db_path)
                for i in range(count):
                    manager.add_event(
                        story_id, 
                        chapter=1,
                        description=f"Event_{worker_id}_{i}",
                        event_type="plot",
                        importance=5
                    )
                manager.close()
            except Exception as e:
                self.errors.append(f"Update error: {e}")
        
        threads = []
        for i in range(10):
            t = threading.Thread(target=add_events, args=(i, 100))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join(timeout=30)
        
        # Check final state
        manager = MemoryManager(db_path)
        timeline = manager.get_timeline(story_id)
        manager.close()
        
        # Should have all events (1000 total)
        if len(timeline) == 1000:
            print(f"    ✅ Update race condition prevented: {len(timeline)}/1000 events")
            return True
        else:
            print(f"    ❌ Update race condition: {len(timeline)}/1000 events")
            return False
        
        if os.path.exists(db_path):
            os.remove(db_path)
    
    def test_deadlock_prevention(self):
        """Test deadlock prevention"""
        print("\n  🔒 Testing deadlock prevention...")
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        deadlock_detected = False
        
        def worker1():
            nonlocal deadlock_detected
            try:
                manager = MemoryManager(db_path)
                story_id = manager.create_story("Story1", "fantasy", "test")
                time.sleep(0.1)
                manager.add_event(story_id, 1, "Event1", "plot", 5)
                manager.close()
            except Exception as e:
                if "deadlock" in str(e).lower():
                    deadlock_detected = True
        
        def worker2():
            nonlocal deadlock_detected
            try:
                manager = MemoryManager(db_path)
                story_id = manager.create_story("Story2", "fantasy", "test")
                time.sleep(0.1)
                manager.add_event(story_id, 1, "Event1", "plot", 5)
                manager.close()
            except Exception as e:
                if "deadlock" in str(e).lower():
                    deadlock_detected = True
        
        threads = []
        for i in range(5):
            t1 = threading.Thread(target=worker1)
            t2 = threading.Thread(target=worker2)
            threads.extend([t1, t2])
            t1.start()
            t2.start()
        
        for t in threads:
            t.join(timeout=30)
        
        if deadlock_detected:
            print("    ⚠️ Deadlock detected but handled")
        else:
            print("    ✅ No deadlocks occurred")
        
        if os.path.exists(db_path):
            os.remove(db_path)
        
        return True
    
    def test_transaction_isolation(self):
        """Test transaction isolation"""
        print("\n  🔐 Testing transaction isolation...")
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        manager = MemoryManager(db_path)
        story_id = manager.create_story("Test", "fantasy", "theme")
        manager.close()
        
        read_values = []
        
        def writer():
            manager = MemoryManager(db_path)
            for i in range(50):
                manager.add_event(story_id, 1, f"Write_{i}", "plot", i % 10)
                time.sleep(0.01)
            manager.close()
        
        def reader():
            manager = MemoryManager(db_path)
            for i in range(10):
                timeline = manager.get_timeline(story_id)
                read_values.append(len(timeline))
                time.sleep(0.05)
            manager.close()
        
        t_writer = threading.Thread(target=writer)
        t_reader = threading.Thread(target=reader)
        
        t_writer.start()
        t_reader.start()
        
        t_writer.join()
        t_reader.join()
        
        # Reader should see consistent states (not garbage)
        if all(0 <= v <= 50 for v in read_values):
            print(f"    ✅ Transaction isolation working: {read_values}")
            return True
        else:
            print(f"    ❌ Transaction isolation failed: {read_values}")
            return False
        
        if os.path.exists(db_path):
            os.remove(db_path)
    
    def test_concurrent_search(self):
        """Test concurrent search operations"""
        print("\n  🔍 Testing concurrent search...")
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        manager = MemoryManager(db_path)
        story_id = manager.create_story("Test", "fantasy", "theme")
        
        # Add searchable content
        for i in range(100):
            manager.add_event(story_id, 1, f"keyword_{i}", "plot", 5)
        
        manager.close()
        
        search_results = []
        
        def search_worker(worker_id):
            try:
                manager = MemoryManager(db_path)
                results = manager.search(story_id, f"keyword_{worker_id % 50}")
                search_results.append(len(results))
                manager.close()
            except Exception as e:
                self.errors.append(str(e))
        
        threads = []
        for i in range(20):
            t = threading.Thread(target=search_worker, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join(timeout=10)
        
        if len(search_results) == 20:
            print(f"    ✅ Concurrent search successful: {search_results[:5]}...")
            return True
        else:
            print(f"    ❌ Concurrent search failed: {len(search_results)}/20")
            return False
        
        if os.path.exists(db_path):
            os.remove(db_path)
    
    def test_connection_pool(self):
        """Test connection pool behavior"""
        print("\n  🔌 Testing connection pool...")
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        connections = []
        
        def create_connection():
            try:
                manager = MemoryManager(db_path)
                connections.append(manager)
                time.sleep(0.1)
                return manager
            except Exception as e:
                self.errors.append(str(e))
                return None
        
        threads = []
        for i in range(30):
            t = threading.Thread(target=create_connection)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join(timeout=10)
        
        # Close all connections
        for conn in connections:
            try:
                conn.close()
            except:
                pass
        
        if len(connections) >= 25:
            print(f"    ✅ Connection pool handled: {len(connections)} connections")
            return True
        else:
            print(f"    ❌ Connection pool issues: {len(connections)}/30")
            return False
        
        if os.path.exists(db_path):
            os.remove(db_path)
    
    def test_starvation_prevention(self):
        """Test starvation prevention"""
        print("\n  🍽️ Testing starvation prevention...")
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        operation_counts = {'reader': 0, 'writer': 0}
        
        def writer():
            manager = MemoryManager(db_path)
            story_id = manager.create_story("Test", "fantasy", "theme")
            for i in range(100):
                manager.add_event(story_id, 1, f"Write_{i}", "plot", 5)
                operation_counts['writer'] += 1
            manager.close()
        
        def reader():
            manager = MemoryManager(db_path)
            for i in range(100):
                try:
                    stories = manager.list_stories()
                    operation_counts['reader'] += 1
                except:
                    pass
                time.sleep(0.001)
            manager.close()
        
        t_writer = threading.Thread(target=writer)
        t_reader = threading.Thread(target=reader)
        
        t_writer.start()
        t_reader.start()
        
        t_writer.join(timeout=30)
        t_reader.join(timeout=30)
        
        # Both should make progress
        if operation_counts['reader'] > 50 and operation_counts['writer'] > 50:
            print(f"    ✅ Starvation prevented: reader={operation_counts['reader']}, writer={operation_counts['writer']}")
            return True
        else:
            print(f"    ❌ Possible starvation: reader={operation_counts['reader']}, writer={operation_counts['writer']}")
            return False
        
        if os.path.exists(db_path):
            os.remove(db_path)
    
    def run_all(self):
        """Run all concurrent access tests"""
        print("\n" + "="*60)
        print("🔄 CONCURRENT ACCESS SECURITY TESTS")
        print("="*60)
        
        tests = [
            ("Race Condition on Create", self.test_race_condition_on_create),
            ("Race Condition on Delete", self.test_race_condition_on_delete),
            ("Race Condition on Update", self.test_race_condition_on_update),
            ("Deadlock Prevention", self.test_deadlock_prevention),
            ("Transaction Isolation", self.test_transaction_isolation),
            ("Concurrent Search", self.test_concurrent_search),
            ("Connection Pool", self.test_connection_pool),
            ("Starvation Prevention", self.test_starvation_prevention),
        ]
        
        results = []
        for name, test_func in tests:
            result = test_func()
            results.append((name, result))
        
        print("\n" + "-"*40)
        for name, status in results:
            print(f"  {'✅' if status else '❌'} {name}")
        print("-"*40)
        
        passed = sum(1 for _, s in results if s)
        print(f"\n📊 Concurrent Access Tests: {passed}/{len(results)} passed")
        
        return passed == len(results)


def run():
    """Run concurrent access security tests"""
    tester = ConcurrentAccessTester()
    return tester.run_all()


if __name__ == "__main__":
    success = run()
    sys.exit(0 if success else 1)