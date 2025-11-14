"""
Unit tests for database models.

This module tests all database models to ensure they work correctly
with SQLAlchemy and maintain proper relationships.
"""

import pytest
import json
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from model.file import File
from model.directory import Directory
from model.search_history import SearchHistory
from model.user_settings import UserSettings
from model.tag import Tag
from model.file_tag import FileTag
from db.base import Base


# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_session():
    """Create a test database session."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    yield session

    session.close()


@pytest.fixture
def sample_directory(db_session: Session):
    """Create a sample directory for testing."""
    directory = Directory(
        path="/test/documents",
        name="documents",
        scan_depth=5,
        exclude_patterns="*.tmp,*.log",
        is_indexed=True
    )
    db_session.add(directory)
    db_session.commit()
    db_session.refresh(directory)
    return directory


@pytest.fixture
def sample_file(db_session: Session, sample_directory):
    """Create a sample file for testing."""
    file_obj = File(
        path="/test/documents/report.pdf",
        filename="report.pdf",
        extension="pdf",
        size=1024000,
        mime_type="application/pdf",
        content_type="document",
        content_text="This is a test PDF report about machine learning.",
        content_hash="abc123def456",
        search_score=0.85,
        access_count=5,
        directory_id=sample_directory.id,
        is_processed=True,
        processing_status="completed",
        metadata_json=json.dumps({"author": "John Doe", "pages": 10})
    )
    db_session.add(file_obj)
    db_session.commit()
    db_session.refresh(file_obj)
    return file_obj


@pytest.fixture
def sample_tags(db_session: Session):
    """Create sample tags for testing."""
    tags = [
        Tag(
            name="machine-learning",
            description="Related to machine learning content",
            color="#FF5733",
            category="content",
            is_system_tag=True
        ),
        Tag(
            name="important",
            description="Important documents",
            color="#28A745",
            category="priority"
        ),
        Tag(
            name="work",
            description="Work related files",
            color="#007BFF",
            category="context"
        )
    ]

    for tag in tags:
        db_session.add(tag)

    db_session.commit()

    # Refresh to get IDs
    for tag in tags:
        db_session.refresh(tag)

    return tags


class TestDirectory:
    """Test cases for Directory model."""

    def test_create_directory(self, db_session: Session):
        """Test creating a new directory."""
        directory = Directory(
            path="/test/projects",
            name="projects",
            scan_depth=3,
            is_indexed=False,
            scan_status="pending"
        )

        db_session.add(directory)
        db_session.commit()

        assert directory.id is not None
        assert directory.path == "/test/projects"
        assert directory.name == "projects"
        assert directory.scan_depth == 3
        assert directory.is_indexed is False
        assert directory.scan_status == "pending"
        assert directory.created_at is not None
        assert directory.modified_at is not None

    def test_directory_self_relationship(self, db_session: Session):
        """Test directory self-referential relationship."""
        # Create parent directory
        parent = Directory(
            path="/test",
            name="test",
            scan_depth=10
        )
        db_session.add(parent)
        db_session.commit()

        # Create child directory
        child = Directory(
            path="/test/subdir",
            name="subdir",
            parent_id=parent.id
        )
        db_session.add(child)
        db_session.commit()

        # Test relationship
        assert child.parent_id == parent.id
        assert child.parent == parent

    def test_directory_unique_path(self, db_session: Session):
        """Test that directory paths must be unique."""
        dir1 = Directory(
            path="/test/unique",
            name="unique1"
        )
        db_session.add(dir1)
        db_session.commit()

        # Try to create another directory with same path
        dir2 = Directory(
            path="/test/unique",
            name="unique2"
        )
        db_session.add(dir2)

        with pytest.raises(Exception):  # Should raise integrity error
            db_session.commit()

    def test_directory_repr(self, sample_directory):
        """Test directory string representation."""
        repr_str = repr(sample_directory)
        assert "Directory" in repr_str
        assert str(sample_directory.id) in repr_str
        assert sample_directory.name in repr_str
        assert sample_directory.path in repr_str


class TestFile:
    """Test cases for File model."""

    def test_create_file(self, db_session: Session, sample_directory):
        """Test creating a new file."""
        file_obj = File(
            path="/test/doc.txt",
            filename="doc.txt",
            extension="txt",
            size=1024,
            mime_type="text/plain",
            content_type="text",
            directory_id=sample_directory.id
        )

        db_session.add(file_obj)
        db_session.commit()

        assert file_obj.id is not None
        assert file_obj.path == "/test/doc.txt"
        assert file_obj.filename == "doc.txt"
        assert file_obj.extension == "txt"
        assert file_obj.size == 1024
        assert file_obj.mime_type == "text/plain"
        assert file_obj.content_type == "text"
        assert file_obj.created_at is not None
        assert file_obj.indexed_at is not None

    def test_file_directory_relationship(self, sample_file, sample_directory):
        """Test file-directory relationship."""
        assert sample_file.directory_id == sample_directory.id
        assert sample_file.directory == sample_directory
        assert sample_file in sample_directory.files

    def test_file_unique_path(self, db_session: Session, sample_directory):
        """Test that file paths must be unique."""
        file1 = File(
            path="/test/unique.txt",
            filename="unique.txt",
            extension="txt",
            size=100,
            directory_id=sample_directory.id
        )
        db_session.add(file1)
        db_session.commit()

        # Try to create another file with same path
        file2 = File(
            path="/test/unique.txt",
            filename="unique.txt",
            extension="txt",
            size=200,
            directory_id=sample_directory.id
        )
        db_session.add(file2)

        with pytest.raises(Exception):  # Should raise integrity error
            db_session.commit()

    def test_file_json_fields(self, db_session: Session, sample_directory):
        """Test JSON field handling."""
        test_metadata = {"author": "Test Author", "version": "1.0", "tags": ["test", "sample"]}

        file_obj = File(
            path="/test/metadata.json",
            filename="metadata.json",
            extension="json",
            size=500,
            directory_id=sample_directory.id,
            metadata_json=json.dumps(test_metadata),
            image_tags=json.dumps(["screenshot", "diagram"])
        )

        db_session.add(file_obj)
        db_session.commit()

        # Test JSON serialization
        assert json.loads(file_obj.metadata_json) == test_metadata
        assert json.loads(file_obj.image_tags) == ["screenshot", "diagram"]

    def test_file_search_relevance(self, db_session: Session, sample_directory):
        """Test search relevance fields."""
        file_obj = File(
            path="/test/popular.pdf",
            filename="popular.pdf",
            extension="pdf",
            size=2000,
            search_score=0.95,
            access_count=100,
            directory_id=sample_directory.id
        )

        db_session.add(file_obj)
        db_session.commit()

        assert file_obj.search_score == 0.95
        assert file_obj.access_count == 100
        assert file_obj.last_accessed is None  # Should be None initially

    def test_file_processing_status(self, db_session: Session, sample_directory):
        """Test file processing status fields."""
        file_obj = File(
            path="/test/processing.docx",
            filename="processing.docx",
            extension="docx",
            size=1500,
            directory_id=sample_directory.id,
            is_processed=False,
            processing_status="pending"
        )

        db_session.add(file_obj)
        db_session.commit()

        assert file_obj.is_processed is False
        assert file_obj.processing_status == "pending"

    def test_file_repr(self, sample_file):
        """Test file string representation."""
        repr_str = repr(sample_file)
        assert "File" in repr_str
        assert str(sample_file.id) in repr_str
        assert sample_file.filename in repr_str
        assert sample_file.path in repr_str


class TestTag:
    """Test cases for Tag model."""

    def test_create_tag(self, db_session: Session):
        """Test creating a new tag."""
        tag = Tag(
            name="test-tag",
            description="A test tag",
            color="#FF0000",
            category="test",
            is_system_tag=False
        )

        db_session.add(tag)
        db_session.commit()

        assert tag.id is not None
        assert tag.name == "test-tag"
        assert tag.description == "A test tag"
        assert tag.color == "#FF0000"
        assert tag.category == "test"
        assert tag.is_system_tag is False
        assert tag.usage_count == 0
        assert tag.created_at is not None

    def test_tag_unique_name(self, db_session: Session):
        """Test that tag names must be unique."""
        tag1 = Tag(name="unique-tag")
        db_session.add(tag1)
        db_session.commit()

        tag2 = Tag(name="unique-tag")
        db_session.add(tag2)

        with pytest.raises(Exception):  # Should raise integrity error
            db_session.commit()

    def test_tag_system_defaults(self, db_session: Session):
        """Test tag default values."""
        tag = Tag(name="default-test")
        db_session.add(tag)
        db_session.commit()

        assert tag.color == "#007bff"  # Default color
        assert tag.is_system_tag is False  # Default value
        assert tag.usage_count == 0  # Default value

    def test_tag_repr(self, db_session: Session):
        """Test tag string representation."""
        tag = Tag(
            name="repr-test",
            category="test"
        )
        db_session.add(tag)
        db_session.commit()

        repr_str = repr(tag)
        assert "Tag" in repr_str
        assert str(tag.id) in repr_str
        assert tag.name in repr_str
        assert tag.category in repr_str


class TestFileTag:
    """Test cases for FileTag model."""

    def test_create_file_tag(self, db_session: Session, sample_file, sample_tags):
        """Test creating a file-tag relationship."""
        file_tag = FileTag(
            file_id=sample_file.id,
            tag_id=sample_tags[0].id,
            confidence=95,
            source="ai_system"
        )

        db_session.add(file_tag)
        db_session.commit()

        assert file_tag.id is not None
        assert file_tag.file_id == sample_file.id
        assert file_tag.tag_id == sample_tags[0].id
        assert file_tag.confidence == 95
        assert file_tag.source == "ai_system"
        assert file_tag.created_at is not None

    def test_file_tag_defaults(self, db_session: Session, sample_file, sample_tags):
        """Test FileTag default values."""
        file_tag = FileTag(
            file_id=sample_file.id,
            tag_id=sample_tags[1].id
        )

        db_session.add(file_tag)
        db_session.commit()

        assert file_tag.confidence == 100  # Default confidence
        assert file_tag.source == "manual"  # Default source

    def test_file_tag_relationships(self, db_session: Session, sample_file, sample_tags):
        """Test FileTag relationships to File and Tag."""
        file_tag = FileTag(
            file_id=sample_file.id,
            tag_id=sample_tags[0].id
        )

        db_session.add(file_tag)
        db_session.commit()

        assert file_tag.file == sample_file
        assert file_tag.tag == sample_tags[0]
        assert file_tag in sample_file.file_tags
        assert file_tag in sample_tags[0].tag_files

    def test_multiple_tags_per_file(self, db_session: Session, sample_file, sample_tags):
        """Test assigning multiple tags to a file."""
        file_tags = []
        for tag in sample_tags:
            file_tag = FileTag(
                file_id=sample_file.id,
                tag_id=tag.id,
                confidence=80 + len(file_tags) * 5
            )
            file_tags.append(file_tag)
            db_session.add(file_tag)

        db_session.commit()

        assert len(sample_file.file_tags) == 3
        assert len(file_tags) == 3

        # Check different confidence values
        confidences = [ft.confidence for ft in file_tags]
        assert confidences == [80, 85, 90]

    def test_multiple_files_per_tag(self, db_session: Session, sample_directory, sample_tags):
        """Test assigning a tag to multiple files."""
        files = []
        for i in range(3):
            file_obj = File(
                path=f"/test/file{i}.txt",
                filename=f"file{i}.txt",
                extension="txt",
                size=100 * (i + 1),
                directory_id=sample_directory.id
            )
            files.append(file_obj)
            db_session.add(file_obj)

        db_session.commit()

        # Refresh to get IDs
        for file_obj in files:
            db_session.refresh(file_obj)

        # Assign same tag to all files
        for file_obj in files:
            file_tag = FileTag(
                file_id=file_obj.id,
                tag_id=sample_tags[0].id
            )
            db_session.add(file_tag)

        db_session.commit()

        assert len(sample_tags[0].tag_files) == 3

    def test_file_tag_repr(self, db_session: Session, sample_file, sample_tags):
        """Test FileTag string representation."""
        file_tag = FileTag(
            file_id=sample_file.id,
            tag_id=sample_tags[0].id
        )

        db_session.add(file_tag)
        db_session.commit()

        repr_str = repr(file_tag)
        assert "FileTag" in repr_str
        assert str(sample_file.id) in repr_str
        assert str(sample_tags[0].id) in repr_str


class TestSearchHistory:
    """Test cases for SearchHistory model."""

    def test_create_search_history(self, db_session: Session):
        """Test creating a new search history entry."""
        search = SearchHistory(
            query_text="machine learning tutorials",
            query_type="text",
            search_mode="hybrid",
            limit=20,
            result_count=15,
            search_time_ms=250,
            results_json=json.dumps([1, 2, 3, 4, 5])
        )

        db_session.add(search)
        db_session.commit()

        assert search.id is not None
        assert search.query_text == "machine learning tutorials"
        assert search.query_type == "text"
        assert search.search_mode == "hybrid"
        assert search.limit == 20
        assert search.result_count == 15
        assert search.search_time_ms == 250
        assert json.loads(search.results_json) == [1, 2, 3, 4, 5]
        assert search.created_at is not None

    def test_search_history_defaults(self, db_session: Session):
        """Test SearchHistory default values."""
        search = SearchHistory(
            query_text="test query"
        )

        db_session.add(search)
        db_session.commit()

        assert search.query_type == "text"  # Default
        assert search.limit == 20  # Default
        assert search.search_mode == "hybrid"  # Default
        assert search.result_count == 0  # Default

    def test_search_history_json_fields(self, db_session: Session):
        """Test JSON field handling in SearchHistory."""
        filters = {
            "content_type": ["document", "image"],
            "size_range": {"min": 1000, "max": 100000},
            "date_range": {"start": "2024-01-01", "end": "2024-12-31"}
        }

        results = [10, 20, 30, 40, 50]

        search = SearchHistory(
            query_text="advanced search",
            filters_json=json.dumps(filters),
            results_json=json.dumps(results)
        )

        db_session.add(search)
        db_session.commit()

        assert json.loads(search.filters_json) == filters
        assert json.loads(search.results_json) == results

    def test_search_history_different_types(self, db_session: Session):
        """Test different search query types."""
        types_data = [
            ("text", "text search query"),
            ("voice", "voice search query"),
            ("image", "image search query")
        ]

        for query_type, query_text in types_data:
            search = SearchHistory(
                query_text=query_text,
                query_type=query_type,
                query_embedding=f"vector_ref_{query_type}"
            )
            db_session.add(search)

        db_session.commit()

        searches = db_session.query(SearchHistory).all()
        assert len(searches) == 3

        for search in searches:
            assert search.query_type in ["text", "voice", "image"]
            assert search.query_embedding is not None

    def test_search_history_repr(self, db_session: Session):
        """Test SearchHistory string representation."""
        search = SearchHistory(
            query_text="test search query",
            query_type="text"
        )

        db_session.add(search)
        db_session.commit()

        repr_str = repr(search)
        assert "SearchHistory" in repr_str
        assert str(search.id) in repr_str
        assert search.query_text in repr_str
        assert search.query_type in repr_str


class TestUserSettings:
    """Test cases for UserSettings model."""

    def test_create_user_setting(self, db_session: Session):
        """Test creating a new user setting."""
        setting = UserSettings(
            key="max_search_results",
            value="50",
            description="Maximum number of search results to display",
            category="search",
            data_type="integer"
        )

        db_session.add(setting)
        db_session.commit()

        assert setting.id is not None
        assert setting.key == "max_search_results"
        assert setting.value == "50"
        assert setting.description == "Maximum number of search results to display"
        assert setting.category == "search"
        assert setting.data_type == "integer"
        assert setting.created_at is not None
        assert setting.updated_at is not None

    def test_user_setting_defaults(self, db_session: Session):
        """Test UserSettings default values."""
        setting = UserSettings(
            key="test_setting",
            value="test_value"
        )

        db_session.add(setting)
        db_session.commit()

        assert setting.data_type == "string"  # Default
        assert setting.description is None
        assert setting.category is None

    def test_user_setting_unique_key(self, db_session: Session):
        """Test that setting keys must be unique."""
        setting1 = UserSettings(
            key="unique_key",
            value="value1"
        )
        db_session.add(setting1)
        db_session.commit()

        setting2 = UserSettings(
            key="unique_key",
            value="value2"
        )
        db_session.add(setting2)

        with pytest.raises(Exception):  # Should raise integrity error
            db_session.commit()

    def test_user_setting_categories(self, db_session: Session):
        """Test different setting categories."""
        categories_data = [
            ("search", "max_results", "20"),
            ("indexing", "scan_interval", "3600"),
            ("ui", "theme", "dark"),
            ("ai", "model_name", "bge-large"),
            ("advanced", "debug_mode", "true")
        ]

        for category, key, value in categories_data:
            setting = UserSettings(
                key=key,
                value=value,
                category=category,
                data_type="string"
            )
            db_session.add(setting)

        db_session.commit()

        settings = db_session.query(UserSettings).all()
        assert len(settings) == 5

        categories = {s.category for s in settings}
        expected_categories = {"search", "indexing", "ui", "ai", "advanced"}
        assert categories == expected_categories

    def test_user_setting_timestamps(self, db_session: Session):
        """Test timestamp handling."""
        setting = UserSettings(
            key="timestamp_test",
            value="initial"
        )

        db_session.add(setting)
        db_session.commit()

        original_created = setting.created_at
        original_updated = setting.updated_at

        # Wait a bit and update
        import time
        time.sleep(0.01)

        setting.value = "updated"
        db_session.commit()

        # Created should not change, updated should
        assert setting.created_at == original_created
        assert setting.updated_at > original_updated

    def test_user_setting_repr(self, db_session: Session):
        """Test UserSettings string representation."""
        setting = UserSettings(
            key="test_repr",
            value="test_value",
            category="test"
        )

        db_session.add(setting)
        db_session.commit()

        repr_str = repr(setting)
        assert "UserSettings" in repr_str
        assert setting.key in repr_str
        assert setting.value in repr_str
        assert setting.category in repr_str


class TestModelIntegration:
    """Integration tests for model relationships."""

    def test_complete_file_tag_relationship(self, db_session: Session, sample_directory):
        """Test complete relationship: Directory -> File -> Tag -> FileTag."""
        # Create file
        file_obj = File(
            path="/test/integration.pdf",
            filename="integration.pdf",
            extension="pdf",
            size=5000,
            directory_id=sample_directory.id
        )
        db_session.add(file_obj)
        db_session.commit()

        # Create tags
        tag1 = Tag(name="integration-test-1", category="test")
        tag2 = Tag(name="integration-test-2", category="test")

        db_session.add(tag1)
        db_session.add(tag2)
        db_session.commit()

        # Create file-tag relationships
        file_tag1 = FileTag(file_id=file_obj.id, tag_id=tag1.id)
        file_tag2 = FileTag(file_id=file_obj.id, tag_id=tag2.id)

        db_session.add(file_tag1)
        db_session.add(file_tag2)
        db_session.commit()

        # Test relationships
        assert len(file_obj.file_tags) == 2
        assert len(tag1.tag_files) == 1
        assert len(tag2.tag_files) == 1
        assert file_obj.directory == sample_directory
        assert file_obj in sample_directory.files

    def test_cascade_delete_behavior(self, db_session: Session, sample_directory):
        """Test cascade delete behavior."""
        # Create file
        file_obj = File(
            path="/test/cascade.txt",
            filename="cascade.txt",
            extension="txt",
            size=100,
            directory_id=sample_directory.id
        )
        db_session.add(file_obj)
        db_session.commit()

        # Create tag and relationship
        tag = Tag(name="cascade-test")
        db_session.add(tag)
        db_session.commit()

        file_tag = FileTag(file_id=file_obj.id, tag_id=tag.id)
        db_session.add(file_tag)
        db_session.commit()

        file_id = file_obj.id
        tag_id = tag.id

        # Manual cascade: first delete the file-tag relationship
        db_session.delete(file_tag)
        db_session.commit()

        # Then delete the file
        db_session.delete(file_obj)
        db_session.commit()

        # Check that file-tag relationship is deleted
        remaining_file_tags = db_session.query(FileTag).filter(
            FileTag.file_id == file_id
        ).all()

        assert len(remaining_file_tags) == 0

        # Tag should still exist
        remaining_tag = db_session.query(Tag).filter(Tag.id == tag_id).first()
        assert remaining_tag is not None

        # Verify file is deleted
        remaining_file = db_session.query(File).filter(File.id == file_id).first()
        assert remaining_file is None