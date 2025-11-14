"""
Unit tests for Data Access Object (DAO) layer.

This module tests all DAO classes to ensure they work correctly with async
database sessions and maintain proper data access patterns.
"""

import pytest
import json
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import event
from sqlalchemy.engine import Engine

from model.file import File
from model.directory import Directory
from model.search_history import SearchHistory
from model.user_settings import UserSettings
from model.tag import Tag
from model.file_tag import FileTag
from dao.base import BaseDAO
from dao.file_dao import FileDAO
from dao.directory_dao import DirectoryDAO
from dao.search_history_dao import SearchHistoryDAO
from dao.tag_dao import TagDAO
from dao.user_settings_dao import UserSettingsDAO
from db.base import Base


# Use async in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="function")
async def async_db_session():
    """Create a test async database session."""
    # Create async engine
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False
    )

    # Enable foreign key constraints for SQLite
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create async session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.fixture
def sample_file_data():
    """Sample file data for testing."""
    return {
        "path": "/test/documents/report.pdf",
        "filename": "report.pdf",
        "extension": "pdf",
        "size": 1024000,
        "mime_type": "application/pdf",
        "content_type": "document",
        "content_text": "This is a test PDF report about machine learning.",
        "content_hash": "abc123def456",
        "search_score": 0.85,
        "access_count": 5,
        "is_processed": True,
        "processing_status": "completed",
        "metadata_json": json.dumps({"author": "John Doe", "pages": 10})
    }


@pytest.fixture
def sample_directory_data():
    """Sample directory data for testing."""
    return {
        "path": "/test/documents",
        "name": "documents",
        "scan_depth": 5,
        "exclude_patterns": "*.tmp,*.log",
        "is_indexed": True,
        "scan_status": "pending"
    }


@pytest.fixture
def sample_tag_data():
    """Sample tag data for testing."""
    return {
        "name": "machine-learning",
        "description": "Related to machine learning content",
        "color": "#FF5733",
        "category": "content",
        "is_system_tag": True
    }


@pytest.fixture
def sample_search_history_data():
    """Sample search history data for testing."""
    return {
        "query_text": "machine learning tutorials",
        "query_type": "text",
        "search_mode": "hybrid",
        "limit": 20,
        "result_count": 15,
        "search_time_ms": 250,
        "results_json": json.dumps([1, 2, 3, 4, 5])
    }


@pytest.fixture
def sample_user_settings_data():
    """Sample user settings data for testing."""
    return {
        "key": "max_search_results",
        "value": "50",
        "description": "Maximum number of search results to display",
        "category": "search",
        "data_type": "integer"
    }


class TestBaseDAO:
    """Test cases for BaseDAO class."""

    @pytest.fixture
    def base_dao(self):
        """Create a BaseDAO instance for testing."""
        return BaseDAO(File)

    async def test_get_by_id(self, async_db_session, base_dao):
        """Test getting an object by ID."""
        # Create a test file
        file_data = {
            "path": "/test/test.txt",
            "filename": "test.txt",
            "extension": "txt",
            "size": 100,
            "content_type": "text"
        }
        created_file = await base_dao.create(async_db_session, obj_in=file_data)

        # Test getting by ID
        retrieved_file = await base_dao.get(async_db_session, obj_id=created_file.id)

        assert retrieved_file is not None
        assert retrieved_file.id == created_file.id
        assert retrieved_file.filename == "test.txt"

    async def test_get_nonexistent(self, async_db_session, base_dao):
        """Test getting a non-existent object."""
        result = await base_dao.get(async_db_session, obj_id=99999)
        assert result is None

    async def test_get_multi(self, async_db_session, base_dao):
        """Test getting multiple objects with pagination."""
        # Create test files
        file_ids = []
        for i in range(5):
            file_data = {
                "path": f"/test/file{i}.txt",
                "filename": f"file{i}.txt",
                "extension": "txt",
                "size": 100 * (i + 1),
                "content_type": "text"
            }
            created_file = await base_dao.create(async_db_session, obj_in=file_data)
            file_ids.append(created_file.id)

        # Test getting multiple objects
        files = await base_dao.get_multi(async_db_session, skip=1, limit=3)

        assert len(files) == 3
        # Should be ordered by ID by default
        assert files[0].id == file_ids[1]

    async def test_get_multi_with_filters(self, async_db_session, base_dao):
        """Test getting multiple objects with filters."""
        # Create test files with different extensions
        for i, ext in enumerate(["txt", "pdf", "txt", "doc", "txt"]):
            file_data = {
                "path": f"/test/file{i}.{ext}",
                "filename": f"file{i}.{ext}",
                "extension": ext,
                "size": 100,
                "content_type": "text"
            }
            await base_dao.create(async_db_session, obj_in=file_data)

        # Test filtering by extension
        txt_files = await base_dao.get_multi(
            async_db_session,
            filters={"extension": "txt"}
        )

        assert len(txt_files) == 3
        assert all(f.extension == "txt" for f in txt_files)

    async def test_get_multi_with_list_filter(self, async_db_session, base_dao):
        """Test getting multiple objects with list filters."""
        # Create test files
        for ext in ["txt", "pdf", "doc"]:
            file_data = {
                "path": f"/test/test.{ext}",
                "filename": f"test.{ext}",
                "extension": ext,
                "size": 100,
                "content_type": "text"
            }
            await base_dao.create(async_db_session, obj_in=file_data)

        # Test filtering by list of extensions
        files = await base_dao.get_multi(
            async_db_session,
            filters={"extension": ["txt", "pdf"]}
        )

        assert len(files) == 2
        extensions = {f.extension for f in files}
        assert extensions == {"txt", "pdf"}

    async def test_create(self, async_db_session, base_dao):
        """Test creating a new object."""
        file_data = {
            "path": "/test/new_file.txt",
            "filename": "new_file.txt",
            "extension": "txt",
            "size": 500,
            "content_type": "text"
        }

        created_file = await base_dao.create(async_db_session, obj_in=file_data)

        assert created_file is not None
        assert created_file.id is not None
        assert created_file.filename == "new_file.txt"
        assert created_file.size == 500

    async def test_update(self, async_db_session, base_dao):
        """Test updating an existing object."""
        # Create a file
        file_data = {
            "path": "/test/update_test.txt",
            "filename": "update_test.txt",
            "extension": "txt",
            "size": 100,
            "content_type": "text"
        }
        created_file = await base_dao.create(async_db_session, obj_in=file_data)

        # Update the file
        update_data = {"size": 200, "search_score": 0.9}
        updated_file = await base_dao.update(
            async_db_session,
            db_obj=created_file,
            obj_in=update_data
        )

        assert updated_file.size == 200
        assert updated_file.search_score == 0.9
        assert updated_file.filename == "update_test.txt"  # Unchanged

    async def test_remove(self, async_db_session, base_dao):
        """Test removing an object."""
        # Create a file
        file_data = {
            "path": "/test/delete_test.txt",
            "filename": "delete_test.txt",
            "extension": "txt",
            "size": 100,
            "content_type": "text"
        }
        created_file = await base_dao.create(async_db_session, obj_in=file_data)
        file_id = created_file.id

        # Delete the file
        deleted_file = await base_dao.remove(async_db_session, obj_id=file_id)

        assert deleted_file is not None
        assert deleted_file.id == file_id

        # Verify file is deleted
        result = await base_dao.get(async_db_session, obj_id=file_id)
        assert result is None

    async def test_count(self, async_db_session, base_dao):
        """Test counting objects."""
        # Create test files
        for i in range(3):
            file_data = {
                "path": f"/test/count_file{i}.txt",
                "filename": f"count_file{i}.txt",
                "extension": "txt",
                "size": 100,
                "content_type": "text"
            }
            await base_dao.create(async_db_session, obj_in=file_data)

        # Test counting all files
        count = await base_dao.count(async_db_session)
        assert count == 3

        # Test counting with filters
        filtered_count = await base_dao.count(
            async_db_session,
            filters={"extension": "txt"}
        )
        assert filtered_count == 3

    async def test_exists(self, async_db_session, base_dao):
        """Test checking if an object exists."""
        # Create a file
        file_data = {
            "path": "/test/exists_test.txt",
            "filename": "exists_test.txt",
            "extension": "txt",
            "size": 100,
            "content_type": "text"
        }
        created_file = await base_dao.create(async_db_session, obj_in=file_data)

        # Test existence
        assert await base_dao.exists(async_db_session, obj_id=created_file.id)
        assert not await base_dao.exists(async_db_session, obj_id=99999)

    async def test_bulk_create(self, async_db_session, base_dao):
        """Test bulk creating objects."""
        # Prepare file data
        file_data_list = [
            {
                "path": f"/test/bulk_file{i}.txt",
                "filename": f"bulk_file{i}.txt",
                "extension": "txt",
                "size": 100 * (i + 1),
                "content_type": "text"
            }
            for i in range(3)
        ]

        # Bulk create
        created_files = await base_dao.bulk_create(async_db_session, obj_list=file_data_list)

        assert len(created_files) == 3
        assert all(f.id is not None for f in created_files)
        assert [f.filename for f in created_files] == [
            "bulk_file0.txt", "bulk_file1.txt", "bulk_file2.txt"
        ]

    async def test_search_text(self, async_db_session, base_dao):
        """Test text search functionality."""
        # Create test files
        search_terms = ["machine learning", "artificial intelligence", "data science"]
        for i, term in enumerate(search_terms):
            file_data = {
                "path": f"/test/search_file{i}.txt",
                "filename": f"search_file{i}.txt",
                "extension": "txt",
                "size": 100,
                "content_type": "text",
                "content_text": f"This file is about {term}"
            }
            await base_dao.create(async_db_session, obj_in=file_data)

        # Test search
        results = await base_dao.search_text(
            async_db_session,
            search_term="machine",
            fields=["filename", "content_text"]
        )

        assert len(results) == 1
        assert "machine" in results[0].content_text

    async def test_ordering(self, async_db_session, base_dao):
        """Test ordering functionality."""
        # Create test files with different sizes
        sizes = [300, 100, 200]
        for i, size in enumerate(sizes):
            file_data = {
                "path": f"/test/order_file{i}.txt",
                "filename": f"order_file{i}.txt",
                "extension": "txt",
                "size": size,
                "content_type": "text"
            }
            await base_dao.create(async_db_session, obj_in=file_data)

        # Test ascending order
        files_asc = await base_dao.get_multi(async_db_session, order_by="size")
        assert [f.size for f in files_asc] == [100, 200, 300]

        # Test descending order
        files_desc = await base_dao.get_multi(async_db_session, order_by="-size")
        assert [f.size for f in files_desc] == [300, 200, 100]


class TestFileDAO:
    """Test cases for FileDAO class."""

    @pytest.fixture
    def file_dao(self):
        """Create a FileDAO instance for testing."""
        return FileDAO()

    async def test_get_by_path(self, async_db_session, file_dao, sample_file_data):
        """Test getting a file by path."""
        # Create a file
        created_file = await file_dao.create(async_db_session, obj_in=sample_file_data)

        # Test getting by path
        found_file = await file_dao.get_by_path(
            async_db_session,
            path=sample_file_data["path"]
        )

        assert found_file is not None
        assert found_file.id == created_file.id
        assert found_file.path == sample_file_data["path"]

    async def test_get_by_hash(self, async_db_session, file_dao, sample_file_data):
        """Test getting a file by content hash."""
        # Create a file
        await file_dao.create(async_db_session, obj_in=sample_file_data)

        # Test getting by hash
        found_file = await file_dao.get_by_hash(
            async_db_session,
            content_hash=sample_file_data["content_hash"]
        )

        assert found_file is not None
        assert found_file.content_hash == sample_file_data["content_hash"]

    async def test_get_by_directory(self, async_db_session, file_dao, sample_file_data):
        """Test getting files by directory."""
        # Create a directory first
        dir_data = {
            "path": "/test/documents",
            "name": "documents"
        }
        directory_dao = DirectoryDAO()
        created_dir = await directory_dao.create(async_db_session, obj_in=dir_data)

        # Create files in that directory
        file_data_1 = {**sample_file_data, "path": "/test/documents/file1.txt", "filename": "file1.txt", "directory_id": created_dir.id}
        file_data_2 = {**sample_file_data, "path": "/test/documents/file2.txt", "filename": "file2.txt", "directory_id": created_dir.id}

        await file_dao.create(async_db_session, obj_in=file_data_1)
        await file_dao.create(async_db_session, obj_in=file_data_2)

        # Test getting files by directory
        files = await file_dao.get_by_directory(async_db_session, directory_id=created_dir.id)

        assert len(files) == 2
        assert all(f.directory_id == created_dir.id for f in files)

    async def test_get_by_extension(self, async_db_session, file_dao, sample_file_data):
        """Test getting files by extension."""
        # Create files with different extensions
        extensions = ["pdf", "txt", "doc"]
        for ext in extensions:
            file_data = {
                **sample_file_data,
                "extension": ext,
                "filename": f"test.{ext}",
                "path": f"/test/documents/test.{ext}"
            }
            await file_dao.create(async_db_session, obj_in=file_data)

        # Test getting files by extension
        pdf_files = await file_dao.get_by_extension(async_db_session, extensions=["pdf"])

        assert len(pdf_files) == 1
        assert pdf_files[0].extension == "pdf"

    async def test_get_recent_files(self, async_db_session, file_dao, sample_file_data):
        """Test getting recently modified files."""
        # Create a file with recent modification
        recent_file_data = {**sample_file_data, "path": "/test/recent.txt", "filename": "recent.txt"}
        await file_dao.create(async_db_session, obj_in=recent_file_data)

        # Test getting recent files
        recent_files = await file_dao.get_recent_files(async_db_session, days=7)

        assert len(recent_files) >= 1
        assert all(not f.is_deleted for f in recent_files)

    async def test_get_popular_files(self, async_db_session, file_dao, sample_file_data):
        """Test getting popular files by access count."""
        # Create files with different access counts
        for i, access_count in enumerate([10, 5, 20]):
            file_data = {
                **sample_file_data,
                "path": f"/test/popular{i}.txt",
                "filename": f"popular{i}.txt",
                "access_count": access_count
            }
            await file_dao.create(async_db_session, obj_in=file_data)

        # Test getting popular files
        popular_files = await file_dao.get_popular_files(async_db_session, limit=3)

        assert len(popular_files) >= 3
        # Should be ordered by access count descending
        access_counts = [f.access_count for f in popular_files[:3]]
        assert access_counts == sorted(access_counts, reverse=True)

    async def test_search_files(self, async_db_session, file_dao, sample_file_data):
        """Test searching files by text content."""
        # Create files with different content
        contents = ["Machine learning is great", "Python programming", "Data analysis tools"]
        for i, content in enumerate(contents):
            file_data = {
                **sample_file_data,
                "path": f"/test/search{i}.txt",
                "filename": f"search{i}.txt",
                "content_text": content
            }
            await file_dao.create(async_db_session, obj_in=file_data)

        # Test searching
        results = await file_dao.search_files(async_db_session, query="machine")

        assert len(results) == 1
        assert "machine" in results[0].content_text.lower()

    async def test_update_access_count(self, async_db_session, file_dao, sample_file_data):
        """Test updating file access count."""
        # Create a file
        created_file = await file_dao.create(async_db_session, obj_in=sample_file_data)
        original_count = created_file.access_count

        # Update access count
        updated_file = await file_dao.update_access_count(async_db_session, file_id=created_file.id)

        assert updated_file.access_count == original_count + 1
        assert updated_file.last_accessed is not None

    async def test_mark_as_processed(self, async_db_session, file_dao, sample_file_data):
        """Test marking a file as processed."""
        # Create an unprocessed file
        file_data = {**sample_file_data, "is_processed": False, "processing_status": "pending"}
        created_file = await file_dao.create(async_db_session, obj_in=file_data)

        # Mark as processed
        updated_file = await file_dao.mark_as_processed(async_db_session, file_id=created_file.id)

        assert updated_file.is_processed is True
        assert updated_file.processing_status == "completed"

    async def test_soft_delete(self, async_db_session, file_dao, sample_file_data):
        """Test soft deleting a file."""
        # Create a file
        created_file = await file_dao.create(async_db_session, obj_in=sample_file_data)

        # Soft delete
        deleted_file = await file_dao.soft_delete(async_db_session, file_id=created_file.id)

        assert deleted_file.is_deleted is True

        # Should not appear in normal queries
        remaining_files = await file_dao.get_multi(async_db_session, filters={"is_deleted": False})
        assert deleted_file not in remaining_files

    async def test_get_storage_stats(self, async_db_session, file_dao, sample_file_data):
        """Test getting storage statistics."""
        # Create files with different content types
        content_types = ["document", "image", "text"]
        sizes = [1000, 2000, 1500]

        for content_type, size in zip(content_types, sizes):
            file_data = {
                **sample_file_data,
                "path": f"/test/stats_{content_type}.txt",
                "filename": f"stats_{content_type}.txt",
                "content_type": content_type,
                "size": size
            }
            await file_dao.create(async_db_session, obj_in=file_data)

        # Get storage stats
        stats = await file_dao.get_storage_stats(async_db_session)

        assert stats["total_files"] >= 3
        assert stats["total_size_bytes"] >= sum(sizes)
        assert "by_content_type" in stats
        assert len(stats["by_content_type"]) >= 3


class TestDirectoryDAO:
    """Test cases for DirectoryDAO class."""

    @pytest.fixture
    def directory_dao(self):
        """Create a DirectoryDAO instance for testing."""
        return DirectoryDAO()

    async def test_get_by_path(self, async_db_session, directory_dao, sample_directory_data):
        """Test getting a directory by path."""
        # Create a directory
        created_dir = await directory_dao.create(async_db_session, obj_in=sample_directory_data)

        # Test getting by path
        found_dir = await directory_dao.get_by_path(
            async_db_session,
            path=sample_directory_data["path"]
        )

        assert found_dir is not None
        assert found_dir.id == created_dir.id
        assert found_dir.path == sample_directory_data["path"]

    async def test_get_root_directories(self, async_db_session, directory_dao):
        """Test getting root directories."""
        # Create root directories
        root_dirs = [
            {"path": "/documents", "name": "documents", "parent_id": None},
            {"path": "/downloads", "name": "downloads", "parent_id": None}
        ]

        for dir_data in root_dirs:
            await directory_dao.create(async_db_session, obj_in=dir_data)

        # Create a child directory
        parent_dir = await directory_dao.get_by_path(async_db_session, path="/documents")
        child_data = {"path": "/documents/projects", "name": "projects", "parent_id": parent_dir.id}
        await directory_dao.create(async_db_session, obj_in=child_data)

        # Test getting root directories
        roots = await directory_dao.get_root_directories(async_db_session)

        assert len(roots) == 2
        assert all(r.parent_id is None for r in roots)

    async def test_get_child_directories(self, async_db_session, directory_dao):
        """Test getting child directories."""
        # Create parent directory
        parent_data = {"path": "/test", "name": "test"}
        parent = await directory_dao.create(async_db_session, obj_in=parent_data)

        # Create child directories
        child_names = ["child1", "child2", "child3"]
        for name in child_names:
            child_data = {
                "path": f"/test/{name}",
                "name": name,
                "parent_id": parent.id
            }
            await directory_dao.create(async_db_session, obj_in=child_data)

        # Test getting child directories
        children = await directory_dao.get_child_directories(async_db_session, parent_id=parent.id)

        assert len(children) == 3
        assert all(c.parent_id == parent.id for c in children)
        child_names_result = [c.name for c in children]
        assert set(child_names_result) == set(child_names)

    async def test_update_scan_status(self, async_db_session, directory_dao, sample_directory_data):
        """Test updating directory scan status."""
        # Create a directory
        created_dir = await directory_dao.create(async_db_session, obj_in=sample_directory_data)

        # Update scan status
        updated_dir = await directory_dao.update_scan_status(
            async_db_session,
            directory_id=created_dir.id,
            scan_status="completed",
            file_count=50,
            total_size=1024000
        )

        assert updated_dir.scan_status == "completed"
        assert updated_dir.file_count == 50
        assert updated_dir.total_size == 1024000
        assert updated_dir.last_scanned is not None

    async def test_get_scan_statistics(self, async_db_session, directory_dao):
        """Test getting scan statistics."""
        # Create directories with different scan statuses
        scan_statuses = ["completed", "pending", "failed"]
        file_counts = [100, 50, 25]

        for status, count in zip(scan_statuses, file_counts):
            dir_data = {
                "path": f"/test/scan_{status}",
                "name": f"scan_{status}",
                "scan_status": status,
                "file_count": count,
                "is_indexed": True
            }
            await directory_dao.create(async_db_session, obj_in=dir_data)

        # Get scan statistics
        stats = await directory_dao.get_scan_statistics(async_db_session)

        assert "total_indexed_directories" in stats
        assert "scan_status_distribution" in stats
        assert "total_files" in stats
        assert stats["total_files"] == sum(file_counts)

    async def test_create_directory_hierarchy(self, async_db_session, directory_dao):
        """Test creating directory hierarchy."""
        # Create a deep directory path
        path = "/projects/ai/ml/models"

        # Create hierarchy
        final_dir = await directory_dao.create_directory_hierarchy(async_db_session, path=path)

        assert final_dir is not None
        assert final_dir.path == path
        assert final_dir.name == "models"

        # Verify all directories in the path were created
        parent_path = "/projects/ai/ml"
        parent_dir = await directory_dao.get_by_path(async_db_session, path=parent_path)
        assert parent_dir is not None

        root_path = "/projects"
        root_dir = await directory_dao.get_by_path(async_db_session, path=root_path)
        assert root_dir is not None


class TestTagDAO:
    """Test cases for TagDAO class."""

    @pytest.fixture
    def tag_dao(self):
        """Create a TagDAO instance for testing."""
        return TagDAO()

    async def test_get_by_name(self, async_db_session, tag_dao, sample_tag_data):
        """Test getting a tag by name."""
        # Create a tag
        created_tag = await tag_dao.create(async_db_session, obj_in=sample_tag_data)

        # Test getting by name
        found_tag = await tag_dao.get_by_name(async_db_session, name=sample_tag_data["name"])

        assert found_tag is not None
        assert found_tag.id == created_tag.id
        assert found_tag.name == sample_tag_data["name"]

    async def test_get_by_category(self, async_db_session, tag_dao):
        """Test getting tags by category."""
        # Create tags in different categories
        categories = ["content", "priority", "format"]
        for category in categories:
            tag_data = {
                "name": f"tag_{category}",
                "category": category,
                "usage_count": 10
            }
            await tag_dao.create(async_db_session, obj_in=tag_data)

        # Test getting by category
        content_tags = await tag_dao.get_by_category(async_db_session, category="content")

        assert len(content_tags) == 1
        assert content_tags[0].category == "content"

    async def test_get_popular_tags(self, async_db_session, tag_dao):
        """Test getting popular tags by usage count."""
        # Create tags with different usage counts
        usage_counts = [50, 10, 30, 20]
        for i, count in enumerate(usage_counts):
            tag_data = {
                "name": f"popular_tag_{i}",
                "usage_count": count,
                "category": "test"
            }
            await tag_dao.create(async_db_session, obj_in=tag_data)

        # Test getting popular tags
        popular_tags = await tag_dao.get_popular_tags(async_db_session, limit=4)

        assert len(popular_tags) == 4
        # Should be ordered by usage count descending
        usage_counts_result = [t.usage_count for t in popular_tags]
        assert usage_counts_result == sorted(usage_counts, reverse=True)


class TestSearchHistoryDAO:
    """Test cases for SearchHistoryDAO class."""

    @pytest.fixture
    def search_history_dao(self):
        """Create a SearchHistoryDAO instance for testing."""
        return SearchHistoryDAO()

    async def test_get_recent_searches(self, async_db_session, search_history_dao, sample_search_history_data):
        """Test getting recent search history."""
        # Create search history entries
        for i in range(5):
            search_data = {
                **sample_search_history_data,
                "query_text": f"search query {i}",
                "created_at": datetime.utcnow() - timedelta(minutes=i)
            }
            await search_history_dao.create(async_db_session, obj_in=search_data)

        # Test getting recent searches
        recent_searches = await search_history_dao.get_recent_searches(async_db_session, limit=3)

        assert len(recent_searches) == 3
        # Should be ordered by created_at descending
        assert recent_searches[0].created_at >= recent_searches[1].created_at

    async def test_get_popular_searches(self, async_db_session, search_history_dao, sample_search_history_data):
        """Test getting popular searches by frequency."""
        # Create search history with repeated queries
        queries = ["machine learning", "python", "machine learning", "data science", "python"]
        search_times = [100, 150, 120, 200, 130]

        for query, search_time in zip(queries, search_times):
            search_data = {
                **sample_search_history_data,
                "query_text": query,
                "search_time_ms": search_time
            }
            await search_history_dao.create(async_db_session, obj_in=search_data)

        # Test getting popular searches
        popular_searches = await search_history_dao.get_popular_searches(async_db_session, days=30)

        assert len(popular_searches) >= 3
        # Should include "machine learning" and "python" with frequency 2
        ml_search = next((s for s in popular_searches if s["query_text"] == "machine learning"), None)
        python_search = next((s for s in popular_searches if s["query_text"] == "python"), None)

        assert ml_search is not None
        assert ml_search["frequency"] == 2
        assert python_search is not None
        assert python_search["frequency"] == 2


class TestUserSettingsDAO:
    """Test cases for UserSettingsDAO class."""

    @pytest.fixture
    def user_settings_dao(self):
        """Create a UserSettingsDAO instance for testing."""
        return UserSettingsDAO()

    async def test_get_by_key(self, async_db_session, user_settings_dao, sample_user_settings_data):
        """Test getting a setting by key."""
        # Create a setting
        created_setting = await user_settings_dao.create(async_db_session, obj_in=sample_user_settings_data)

        # Test getting by key
        found_setting = await user_settings_dao.get_by_key(
            async_db_session,
            key=sample_user_settings_data["key"]
        )

        assert found_setting is not None
        assert found_setting.id == created_setting.id
        assert found_setting.key == sample_user_settings_data["key"]

    async def test_get_by_category(self, async_db_session, user_settings_dao):
        """Test getting settings by category."""
        # Create settings in different categories
        categories = ["search", "ui", "ai"]
        for category in categories:
            setting_data = {
                "key": f"{category}_setting",
                "value": f"value_{category}",
                "category": category
            }
            await user_settings_dao.create(async_db_session, obj_in=setting_data)

        # Test getting by category
        search_settings = await user_settings_dao.get_by_category(async_db_session, category="search")

        assert len(search_settings) == 1
        assert search_settings[0].category == "search"

    async def test_get_setting_value(self, async_db_session, user_settings_dao):
        """Test getting setting value with type parsing."""
        # Create different types of settings
        settings_data = [
            {"key": "string_setting", "value": "test_string", "data_type": "string"},
            {"key": "int_setting", "value": "42", "data_type": "integer"},
            {"key": "bool_setting_true", "value": "true", "data_type": "boolean"},
            {"key": "bool_setting_false", "value": "false", "data_type": "boolean"},
            {"key": "json_setting", "value": '{"key": "value"}', "data_type": "json"},
            {"key": "unknown_type", "value": "test_value", "data_type": "custom"}
        ]

        for setting_data in settings_data:
            await user_settings_dao.create(async_db_session, obj_in=setting_data)

        # Test getting values with proper type parsing
        assert await user_settings_dao.get_setting_value(async_db_session, key="string_setting") == "test_string"
        assert await user_settings_dao.get_setting_value(async_db_session, key="int_setting") == 42
        assert await user_settings_dao.get_setting_value(async_db_session, key="bool_setting_true") is True
        assert await user_settings_dao.get_setting_value(async_db_session, key="bool_setting_false") is False
        assert await user_settings_dao.get_setting_value(async_db_session, key="json_setting") == {"key": "value"}
        assert await user_settings_dao.get_setting_value(async_db_session, key="unknown_type") == "test_value"

        # Test default value
        assert await user_settings_dao.get_setting_value(async_db_session, key="nonexistent", default="default") == "default"

    async def test_set_setting(self, async_db_session, user_settings_dao):
        """Test setting a user setting."""
        # Create a new setting
        await user_settings_dao.set_setting(
            async_db_session,
            key="new_setting",
            value="new_value",
            description="A new test setting",
            category="test"
        )

        # Verify the setting was created
        setting = await user_settings_dao.get_by_key(async_db_session, key="new_setting")
        assert setting is not None
        assert setting.value == "new_value"
        assert setting.description == "A new test setting"
        assert setting.category == "test"

        # Update existing setting
        await user_settings_dao.set_setting(
            async_db_session,
            key="new_setting",
            value="updated_value"
        )

        # Verify the setting was updated
        updated_setting = await user_settings_dao.get_by_key(async_db_session, key="new_setting")
        assert updated_setting.value == "updated_value"
        assert updated_setting.updated_at > setting.created_at